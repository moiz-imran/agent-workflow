#!/usr/bin/env python3
"""Block `git push` and `gh pr create` until the exact code has passed the review loop.

No arguments: Claude Code PreToolUse hook on Bash (JSON on stdin).
receipt --ticket T: record the current working tree as CLEAN (run by the review controller).
guide --ticket T: render <scratch>/T/review-guide.json + the diff into review.html and pr.md,
                  and keep a copy of the ticket's evidence outside /tmp.
test: run the parser self-check.

Opt a repository in with `git config review-gate.enabled true`. Other repositories are never blocked.

Limits, on purpose:
- It reads the literal command. It follows `cd`, `git -C` and leading VAR=value, but a push
  inside a script, alias, subshell or another tool is not seen.
- It checks the tree of HEAD in the checkout being pushed, not every commit or ref sent.
- Receipts are local files. This keeps an honest agent on the process; it is not tamper-proof.
"""
import contextlib
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
import webbrowser
from pathlib import Path

STATE = Path(os.environ.get("AGENT_WORKFLOW_HOME", Path.home() / ".agent-workflow"))
SCRATCH = Path(os.environ.get("AGENT_WORKFLOW_SCRATCH", "/tmp"))
RECEIPTS = STATE / "receipts"
EVIDENCE = STATE / "evidence"
TICKET = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,79}")
DECISION = re.compile(r"[DF]\d{1,4}")


def git(cwd, *args, env=None):
    return subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True,
                          check=True, env=env).stdout.strip()


@contextlib.contextmanager
def snapshot_index(cwd):
    """Env for git commands against a throwaway index holding the whole working copy.

    Untracked files are included; the real index is never touched.
    """
    with tempfile.TemporaryDirectory() as d:
        env = {**os.environ, "GIT_INDEX_FILE": str(Path(d) / "index"), "GIT_LITERAL_PATHSPECS": "1"}
        git(cwd, "read-tree", "HEAD", env=env)
        git(cwd, "add", "-A", env=env)
        yield env


def working_tree(cwd):
    with snapshot_index(cwd) as env:
        return git(cwd, "write-tree", env=env)


def repo_id(cwd):
    try:
        return git(cwd, "remote", "get-url", "origin")
    except subprocess.CalledProcessError:
        return git(cwd, "rev-parse", "--show-toplevel")


def receipt_path(repo, tree):
    # Bound to the repository as well as the tree, so the same files in another repo don't pass.
    return RECEIPTS / hashlib.sha256(f"{repo}\n{tree}".encode()).hexdigest()


def gated_operations(command, cwd):
    """Return (cwd, skip_reason) for each push or PR creation in a shell command."""
    lex = shlex.shlex(command, posix=True, punctuation_chars=";&|\n")
    lex.whitespace, lex.whitespace_split = " \t\r", True
    try:
        tokens = list(lex)
    except ValueError:
        return []  # unbalanced quotes: the shell would reject it too
    segments, current = [], []
    for token in tokens:
        if token and set(token) <= set(";&|\n"):
            segments.append(current)
            current = []
        else:
            current.append(token)
    segments.append(current)

    found = []
    for argv in segments:
        skip = ""
        while argv and re.match(r"^[A-Za-z_]\w*=", argv[0]):
            name, _, value = argv.pop(0).partition("=")
            skip = value if name == "REVIEW_GATE_SKIP" else skip
        if not argv:
            continue
        if argv[0] == "cd" and len(argv) > 1:
            cwd = os.path.join(cwd, os.path.expanduser(argv[1]))
        elif argv[0] == "gh" and argv[1:3] == ["pr", "create"]:
            found.append((cwd, skip))
        elif argv[0] == "git":
            at, here = 1, cwd
            while at < len(argv) and argv[at].startswith("-"):
                if argv[at] == "-C" and at + 1 < len(argv):
                    here = os.path.join(here, os.path.expanduser(argv[at + 1]))
                    at += 1
                elif argv[at] == "-c":
                    at += 1
                at += 1
            rest = argv[at + 1:]
            if argv[at:at + 1] == ["push"] and not {"--delete", "-d", "--dry-run", "-n"} & set(rest):
                found.append((here, skip))
    return found


ROUND = re.compile(r"^## Round\b.*$", re.M | re.I)


def ledger_problem(text, tree):
    """Why a review ledger can't back a CLEAN receipt for tree, or None."""
    heads = ROUND.findall(text)
    if not heads:
        return "the ledger has no '## Round' sections"
    for h in heads:
        if not re.search(r"\b(full|delta)\b", h, re.I):
            return f"round heading is not labelled full or delta: {h}"
    if not re.search(r"\bfull\b", heads[-1], re.I):
        return f"the last round must be a full review: {heads[-1]}"
    if tree[:12] not in text[text.rindex(heads[-1]):]:
        return f"the last full round does not record snapshot tree {tree[:12]}"
    return None


def receipt(ticket):
    cwd = os.getcwd()
    repo, tree = repo_id(cwd), working_tree(cwd)
    folder = SCRATCH / ticket
    ledger = folder / f"{Path(git(cwd, 'rev-parse', '--show-toplevel')).name}-review-ledger.md"
    ledgers = sorted(folder.glob("*-review-ledger.md"))
    if not ledger.exists() and len(ledgers) == 1:
        ledger = ledgers[0]  # ponytail: the ledger's repo name may differ from the checkout folder
    why = ledger_problem(ledger.read_text(), tree) if ledger.exists() else f"no ledger at {ledger}"
    if why:
        sys.exit(f"No receipt: {why}. Label every round full or delta and end with a full review of this tree.")
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    receipt_path(repo, tree).write_text(json.dumps({
        "ticket": ticket, "repo": repo, "tree": tree, "head": git(cwd, "rev-parse", "HEAD"),
        "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}, indent=2))
    print(tree)


def problem(cwd, skip, command):
    """Reason to block, or None."""
    try:
        if git(cwd, "config", "--bool", "--get", "review-gate.enabled") != "true":
            return None
    except (subprocess.CalledProcessError, OSError):
        return None  # not a repo, or not opted in
    repo, tree = repo_id(cwd), git(cwd, "rev-parse", "HEAD^{tree}")
    if receipt_path(repo, tree).exists():
        return None
    if skip:
        STATE.mkdir(parents=True, exist_ok=True)
        with open(STATE / "gate-overrides.log", "a") as log:
            log.write(f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}\t{repo}\t{tree}\t{skip}\t{command}\n")
        return None
    return (f"Review gate: HEAD tree {tree[:12]} in {repo} has no CLEAN review receipt, so this exact code "
            "has not passed the review loop. Run the review on this snapshot and commit exactly what it reviewed. "
            'Only if the user explicitly approves skipping it, retry with REVIEW_GATE_SKIP="<their reason>" '
            "before the command.")


def hook():
    payload = json.load(sys.stdin)
    if payload.get("tool_name") != "Bash":
        return
    command = payload.get("tool_input", {}).get("command", "")
    for cwd, skip in gated_operations(command, payload.get("cwd") or os.getcwd()):
        reason = problem(cwd, skip, command)
        if reason:
            print(json.dumps({"hookSpecificOutput": {
                "hookEventName": "PreToolUse", "permissionDecision": "deny",
                "permissionDecisionReason": reason}}))
            return


def changed_files(cwd, base):
    """{path: that file's diff} for the working copy against base, in git's order.

    Paths come from NUL-separated output, so names with tabs, quotes or non-ASCII characters survive.
    """
    with snapshot_index(cwd) as env:
        out = git(cwd, "diff", "--cached", "-M", "--name-status", "-z", base, "--", env=env).split("\0")
        files, i = {}, 0
        while i < len(out) and out[i]:
            paths = out[i + 1:i + (3 if out[i][0] in "RC" else 2)]
            i += 1 + len(paths)
            files[paths[-1]] = subprocess.run(
                ["git", "-C", str(cwd), "diff", "--cached", "-M", base, "--", *paths],
                capture_output=True, text=True, errors="replace", check=True, env=env).stdout
        return files


def parse_decisions(text):
    """{D1: current text}. An entry marked SUPERSEDED gives way to the next entry with the same id."""
    out, last = {}, None
    for line in text.splitlines():
        m = re.match(r"\W*([DF]\d+)\W*\s(.*)", line)
        if m:
            last = m.group(1)
            if "SUPERSEDED" in line and last in out:
                continue
            out[last] = m.group(2)
            if "SUPERSEDED" in line:
                last = None
        elif last and line.strip() and not line.startswith("#"):
            out[last] += " " + line.strip()
    return out


def guide(ticket):
    """Render the reviewer's guide: the controller's review-guide.json + the real diff -> review.html and pr.md."""
    cwd, folder = os.getcwd(), SCRATCH / ticket
    g = json.loads((folder / "review-guide.json").read_text())
    git(cwd, "rev-parse", "--verify", "--quiet", f"{g['base']}^{{commit}}")  # fails loudly on a bad base
    files = changed_files(cwd, g["base"])
    log = folder / "decisions.md"
    logged = parse_decisions(log.read_text()) if log.exists() else {}
    used = {x for f in g.get("order", []) for x in f.get("decisions", [])}
    # The guide's own list scopes the page; decisions.md only fills in tagged ids it left out.
    decisions = g.get("decisions") or logged
    decisions = {**decisions, **{k: logged[k] for k in sorted(used - set(decisions)) if k in logged}}
    decisions = {k: v for k, v in decisions.items() if DECISION.fullmatch(k)}
    notes = {f["path"]: f for f in g.get("order", []) + g.get("skim", [])}
    skim = {f["path"] for f in g.get("skim", [])}
    paths = [p for p in notes if p in files and p not in skim] + [p for p in files if p not in notes] \
        + [p for p in notes if p in skim and p in files]
    data = {**g, "ticket": ticket, "decisions": decisions, "files": [
        {**notes.get(p, {"why": "Not in the guide."}), "path": p, "diff": files[p], "skim": p in skim}
        for p in paths]}
    for f in data["files"]:
        f["decisions"] = [k for k in f.get("decisions", []) if DECISION.fullmatch(k)]
    blob = json.dumps(data).replace("<", "\\u003c")  # no "<" at all, so nothing can end or comment out the script
    (folder / "review.html").write_text(GUIDE_HTML.replace("__DATA__", blob))

    pr = [f"## What changed\n\n{g['summary']}\n\n## Reading order\n"]
    pr += [f"{i}. `{f['path']}`: {f['why']}" for i, f in enumerate(g.get("order", []), 1)]
    if skim:
        pr.append("\nSkim: " + ", ".join(f"`{p}`" for p in skim))
    pr.append("\n## Design notes\n")
    pr += [f"- {t}" for k, t in decisions.items() if k in used or not used]
    pr.append("\n## Checks\n")
    pr += [f"- {c['cmd']}: {c['result']}" for c in g.get("checks", [])]
    if g.get("follow_ups"):
        pr.append("\n## Follow-ups\n")
        pr += [f"- {x}" for x in g["follow_ups"]]
    (folder / "pr.md").write_text("\n".join(pr) + "\n")

    # Lasting copy: /tmp gets wiped, so keep what was decided, checked and approved for this snapshot.
    repo, tree = repo_id(cwd), working_tree(cwd)
    keep = EVIDENCE / ticket / f"{Path(cwd).name}-{tree[:12]}"
    keep.mkdir(parents=True, exist_ok=True)
    for f in [*folder.glob("*-review-ledger.md"), *(folder / n for n in (
            "map.md", "decisions.md", "outcomes.csv", "review-guide.json", "review.html", "pr.md"))]:
        if f.is_file():
            shutil.copy2(f, keep)
    if receipt_path(repo, tree).exists():
        shutil.copy2(receipt_path(repo, tree), keep / "receipt.json")
    print(folder / "review.html", folder / "pr.md", keep, sep="\n")
    webbrowser.open((folder / "review.html").resolve().as_uri())


# Offline on purpose: the page holds your full diff, so it loads no remote code.
GUIDE_HTML = r"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Review guide</title>
<style>
:root{--bg:#fafaf9;--panel:#fff;--ink:#1c1917;--dim:#78716c;--line:#e7e5e4;--accent:#2563eb;--warn:#b45309;--warnbg:#fef3c7;--ok:#15803d;--add:#e6f4ea;--del:#fdecea}
@media (prefers-color-scheme:dark){:root{--bg:#0c0a09;--panel:#1c1917;--ink:#e7e5e4;--dim:#a8a29e;--line:#292524;--accent:#60a5fa;--warn:#fbbf24;--warnbg:#3a2a05;--ok:#4ade80;--add:#12301c;--del:#3a1614}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 system-ui,sans-serif}
header{padding:24px 16px 12px;max-width:1600px;margin:auto}h1{margin:0 0 4px;font-size:20px}
.dim{color:var(--dim)}.pills{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.pill{border:1px solid var(--line);border-radius:99px;padding:2px 10px;font-size:12px;background:var(--panel)}
.pill b{color:var(--ok)}.follow{margin-top:10px;padding:8px 12px;border-left:3px solid var(--warn);background:var(--warnbg)}
main{display:grid;grid-template-columns:minmax(0,1fr) 320px;gap:16px;padding:0 16px 40px;max-width:1600px;margin:auto}
@media (max-width:900px){main{grid-template-columns:minmax(0,1fr)}aside{order:-1}}
@media (min-width:901px){aside{position:sticky;top:12px;align-self:start;max-height:calc(100vh - 24px);overflow:auto}}
.card{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:12px;margin-bottom:12px}
.card h2{font-size:13px;text-transform:uppercase;letter-spacing:.05em;margin:0 0 8px;color:var(--dim)}
.dec{padding:6px;border-radius:6px;margin-bottom:4px}.dec.hot{background:var(--warnbg)}
.unseen{font-size:11px;color:var(--warn);font-weight:600}
.badge{display:inline-block;font:600 11px ui-monospace,monospace;color:var(--accent);border:1px solid currentColor;border-radius:4px;padding:0 5px;text-decoration:none;margin-right:3px;cursor:pointer}
.badge.on{background:var(--accent);color:var(--panel);border-color:var(--accent)}
details.file{background:var(--panel);border:1px solid var(--line);border-radius:8px;margin-bottom:12px}
details.file>summary{cursor:pointer;padding:10px 12px;display:flex;flex-wrap:wrap;gap:6px 10px;align-items:baseline}
.num{font:600 12px ui-monospace,monospace;color:var(--dim)}.path{font:600 13px ui-monospace,monospace;word-break:break-all}
.why{flex-basis:100%;color:var(--dim)}.flagnote{margin:0 12px 8px;padding:6px 10px;border-left:3px solid var(--warn);background:var(--warnbg);font-size:13px}
.flagnote.fixed{border-left-color:var(--ok);background:none}.done{font-size:11px;color:var(--ok);font-weight:600}
.dec a{color:var(--accent);font:600 12px ui-monospace,monospace}
.decnote{margin:0 12px 8px;padding:6px 10px;border-left:3px solid var(--accent);font-size:13px}
.diff{overflow:auto;border-top:1px solid var(--line);font:12px/1.45 ui-monospace,monospace}
.diff div{white-space:pre;padding:0 12px 0 0;display:flex}.diff i{font-style:normal;color:var(--dim);min-width:4.5em;text-align:right;padding-right:10px;user-select:none}
.diff .a{background:var(--add)}.diff .d{background:var(--del)}.diff .h{color:var(--dim);background:var(--bg)}
.diff .flag{outline:2px solid var(--warn);outline-offset:-2px}.diff .flag.fixed{outline:1px dashed var(--ok)}
.sep{margin:20px 0 8px;color:var(--dim);font-size:12px;text-transform:uppercase;letter-spacing:.05em}
</style></head><body>
<script type="application/json" id="data">__DATA__</script>
<header id="hd"></header><main><section id="files"></section><aside id="side"></aside></main>
<script>
const D=JSON.parse(document.getElementById('data').textContent);
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const used=new Set(D.files.flatMap(f=>f.decisions||[]));
document.title=D.ticket+' review';
hd.innerHTML=`<h1>${esc(D.ticket)} review guide</h1><div class="dim">${esc(D.summary)}</div>
<div class="pills"><span class="pill">base ${esc(D.base)}</span>${(D.checks||[]).map(c=>`<span class="pill">${esc(c.cmd)}: <b>${esc(c.result)}</b></span>`).join('')}</div>
${(D.follow_ups||[]).map(x=>`<div class="follow">Follow-up: ${esc(x)}</div>`).join('')}`;
side.innerHTML=`<div class="card"><h2>Decisions</h2>${Object.entries(D.decisions).map(([k,t])=>`<div class="dec" id="${esc(k)}">
<span class="badge">${esc(k)}</span>${used.has(k)?'':'<span class="unseen">NOT IN ANY FILE NOTE</span>'}<div>${esc(t)}</div></div>`).join('')}</div>
<div class="card"><h2>Where review pushed back</h2>${(D.pushback||[]).map(p=>`<div class="dec"><a href="#f-${D.files.findIndex(f=>f.path===p.path)}">${esc(String(p.path).split('/').pop())}:${esc(p.line)}</a>
${p.fixed?'<span class="done">FIXED</span>':'<span class="unseen">OPEN</span>'}<div>${esc(p.what)}</div></div>`).join('')||'<span class="dim">None</span>'}</div>`;
// One column: hunk headers reset the new-file line number, which is what pushback lines refer to.
// Lines before the first hunk (renames, mode changes, "Binary files differ") show as headers.
function rows(diff,flags){let n=0,hunk=false;return diff.split('\n').map(l=>{
 if(l.startsWith('@@')){hunk=true;n=+(/\+(\d+)/.exec(l)||[0,1])[1];return `<div class="h"><i></i>${esc(l)}</div>`}
 if(!hunk||l[0]==='\\')return l?`<div class="h"><i></i>${esc(l)}</div>`:'';
 const c=l[0];if(c==='-')return `<div class="d"><i></i>${esc(l)}</div>`;
 const f=flags.find(p=>+p.line===n),cls=(c==='+'?'a':'')+(f?' flag'+(f.fixed?' fixed':''):'');
 return `<div class="${cls}"><i>${n++}</i>${esc(l)}</div>`}).join('')}
let num=0,sep=false;D.files.forEach((f,i)=>{
 if(f.skim&&!sep){sep=true;files.insertAdjacentHTML('beforeend','<div class="sep">Skim</div>')}
 const flags=(D.pushback||[]).filter(p=>p.path===f.path);
 const el=document.createElement('details');el.className='file';el.id='f-'+i;el.open=!f.skim;
 el.innerHTML=`<summary><span class="num">${f.skim?'·':++num}</span><span class="path">${esc(f.path)}</span>
 ${(f.decisions||[]).map(k=>`<span class="badge" data-k="${esc(k)}">${esc(k)}</span>`).join('')}<span class="why">${esc(f.why)}</span></summary>
 <div class="decnotes"></div>${flags.map(p=>`<div class="flagnote${p.fixed?' fixed':''}">${p.fixed?'Fixed':'Open'}, line ${esc(p.line)}: ${esc(p.what)}</div>`).join('')}
 <div class="diff">${rows(f.diff,flags)}</div>`;
 files.append(el)});
// Click a badge: show that decision under the file and flash it in the sidebar.
document.addEventListener('click',e=>{const b=e.target.closest('summary .badge');if(!b)return;e.preventDefault();
 const k=b.dataset.k,box=b.closest('details').querySelector('.decnotes'),open=[...box.children].find(x=>x.dataset.k===k);
 b.classList.toggle('on',!open);if(open)return open.remove();
 const note=document.createElement('div');note.className='decnote';note.dataset.k=k;
 note.innerHTML=`<b>${esc(k)}</b> ${esc(D.decisions[k]||'Not in decisions.md')}`;box.append(note);
 const d=document.getElementById(k);if(d){d.classList.add('hot');setTimeout(()=>d.classList.remove('hot'),1500)}});
</script></body></html>"""


def selftest():
    cases = {
        "git status": 0, "git push": 1, "git push --dry-run": 0, "git push origin --delete x": 0,
        "git -C /r push origin b": 1, "git -c a=b push": 1, "gh pr create --fill": 1, "gh pr view": 0,
        "git commit -m 'then git push; done' && git push": 1, 'echo "git push"': 0,
        "cd /r && git push": 1, "git add . && git commit -m x; git push && gh pr create": 2,
        'REVIEW_GATE_SKIP="ok by user" git push': 1,
    }
    for command, count in cases.items():
        assert len(gated_operations(command, "/w")) == count, command
    assert gated_operations("cd /r && git push", "/w") == [("/r", "")]
    assert gated_operations('REVIEW_GATE_SKIP="ok by user" git push', "/w") == [("/w", "ok by user")]
    log = "# t\nD1. old\nD2. SUPERSEDED: was A\nD2. now B\n  because C\n"
    assert parse_decisions(log) == {"D1": "old", "D2": "now B because C"}
    assert TICKET.fullmatch("DOC-142") and not TICKET.fullmatch("../x")
    t = "abcdef1234567890"
    assert ledger_problem("## Round 1, d: full\n## Round 2, d: delta\n## Round 3, d: full\ntree abcdef123456\n", t) is None
    assert "not labelled" in ledger_problem("## Round 1\ntree abcdef123456\n", t)
    assert "last round" in ledger_problem("## Round 1: full\n## Round 2: delta abcdef123456\n", t)
    assert "snapshot" in ledger_problem("## Round 1: full\ntree 000\n", t)
    print("ok")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        hook()
    elif args == ["test"]:
        selftest()
    elif len(args) == 3 and args[:2] in (["receipt", "--ticket"], ["guide", "--ticket"]):
        if not TICKET.fullmatch(args[2]):
            sys.exit(f"Bad ticket name: {args[2]!r}")
        (receipt if args[0] == "receipt" else guide)(args[2])
    else:
        sys.exit(__doc__)
