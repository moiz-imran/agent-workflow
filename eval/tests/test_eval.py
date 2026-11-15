"""Offline harness checks; agent entry points must always resolve to fake_agent.py."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

EVAL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EVAL))
import run as harness  # noqa: E402
import reader  # noqa: E402


def options():
    return argparse.Namespace(live=False, max_reader_calls=12, codex_effort='medium',
                              codex_model=None, claude_model='fake', claude_effort='medium',
                              max_turns=10, minutes=1, quality_cmd=None, window=3, require_map=False)


class EvalTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def fixture(self, name='task-inventory'):
        case = next(c for c in harness.load_cases('all') if c['id'] == name)
        trial = self.root / name
        trial.mkdir()
        return case, trial, harness.stage(case, trial)

    def test_no_real_agents(self):
        for provider in ('claude', 'codex'):
            argv = harness.agent_bin(provider, options())
            self.assertEqual(argv, [sys.executable, str(EVAL / 'fake_agent.py'), provider])

    def test_usage_limit(self):
        with tempfile.TemporaryDirectory() as d:
            log = Path(d) / "x.jsonl"
            log.write_text('{"result": "ok"}')
            self.assertFalse(harness.hit_usage_limit(log))
            log.write_text('{"result": "You hit your 5-hour limit, resets 2am"}')
            self.assertTrue(harness.hit_usage_limit(Path(d) / "missing.jsonl", log))

    def test_score(self):
        g = dict(id='G1', path='app.py', start_line=10, end_line=10, severity='Blocking')
        f = {k: v for k, v in g.items() if k != 'id'}
        f['start_line'] = f['end_line'] = 13
        novel = dict(f, path='other.py')
        r = harness.score_review([f, f, novel, novel], [g], 3, {'2': 'real', '3': 'false'})
        self.assertEqual((r['caught'], r['duplicates'], r['novel_real'], r['false_alarms']), (1, 1, 1, 1))
        self.assertEqual(harness.score_review([f], [g], 2)['caught'], 0)
        self.assertEqual(harness.score_review([f], [])['unadjudicated'], 1)
        self.assertEqual(harness.score_review([], [])['caught'], 0)
        self.assertEqual(harness.score_review([f], [g, dict(g, id='G2')])['caught'], 1)
        also = dict(g, also=[dict(path='other.py', start_line=1, end_line=5)])
        self.assertEqual(harness.score_review([dict(f, path='other.py', start_line=4, end_line=4)], [also])['caught'], 1)

    def test_valid_findings(self):
        good = {'path': 'a.py', 'start_line': 2, 'end_line': 3, 'severity': 'Blocking', 'title': 't', 'evidence': 'e'}
        for value in ({}, [], {'findings': []}, {'findings': [{'path': 'x'}], 'covered': [], 'not_covered': []},
                      {'findings': [dict(good, start_line=5)], 'covered': [], 'not_covered': []},
                      {'findings': [dict(good, start_line=True)], 'covered': [], 'not_covered': []},
                      {'findings': [dict(good, title='')], 'covered': [], 'not_covered': []}):
            with self.assertRaises(ValueError):
                harness.valid_findings(value)
        self.assertEqual(harness.valid_findings({'findings': [good], 'covered': ['a.py'], 'not_covered': []})['findings'], [good])

    def test_usage(self):
        text = 'bad\n' + json.dumps({'type': 'turn.completed', 'usage': {'input_tokens': 3}})
        self.assertEqual(reader.usage_from_jsonl(text + '\n' + text), {'input_tokens': 6})
        self.assertIsNone(reader.usage_from_jsonl('bad'))
        self.assertIsNone(harness.claude_result('bad'))
        self.assertEqual(harness.claude_result(json.dumps({'type': 'result', 'usage': {'output_tokens': 4}}))['usage'], {'output_tokens': 4})
        self.assertEqual(harness.sum_usage([None, {'a': 2}, {'a': 3}]), {'a': 5})
        self.assertIsNone(harness.sum_usage([]))

    def test_grading_has_no_credentials(self):
        (self.root / 't').mkdir()
        (self.root / 't' / 'test_env.py').write_text(
            'import os, unittest\nclass T(unittest.TestCase):\n'
            ' def test_env(self): assert "CLAUDE_CODE_OAUTH_TOKEN" not in os.environ and "x-home" not in os.environ["HOME"]\n')
        with patch.dict(os.environ, {'CLAUDE_CODE_OAUTH_TOKEN': 'secret', 'HOME': '/x-home'}):
            result, code = harness.unittest_results(self.root / 't', 'python3 -B -m unittest -v')
        self.assertEqual((list(result.values()), code), (['ok'], 0))

    def test_new_failure_is_not_solved(self):
        case = {'id': 'c', 'dir': self.root / 'case', 'grade': 'python3 -B -m unittest discover -s tests_hidden -t . -v'}
        (case['dir'] / 'hidden' / 'tests_hidden').mkdir(parents=True)
        (case['dir'] / 'hidden' / 'tests_hidden' / '__init__.py').write_text('')
        (case['dir'] / 'hidden' / 'tests_hidden' / 'test_h.py').write_text(
            'import os, unittest\nclass T(unittest.TestCase):\n'
            ' def test_flag(self): assert os.path.exists("done")\n'
            ' if os.path.exists("done"):\n'
            '  def test_new(self): self.fail()\n')
        repo = self.root / 'trial' / 'repo'
        repo.mkdir(parents=True)
        harness.git(repo, 'init', '-q')
        (repo / 'a').write_text('a')
        harness.git(repo, 'add', '-A')
        harness.git(repo, '-c', 'user.name=t', '-c', 'user.email=t@localhost', 'commit', '-qm', 'base')
        harness.git(repo, 'tag', 'base')
        (repo / 'done').write_text('')
        g = harness.grade(case, repo, self.root / 'trial')
        self.assertEqual(g['fail_to_pass'], 1)
        self.assertFalse(g['solved'])
        self.assertIn('tests_hidden.test_h.T.test_new', g['failing'])

    def test_analyzer_failure_is_an_error(self):
        repo = self.root / 'trial' / 'repo'
        repo.mkdir(parents=True)
        harness.git(repo, 'init', '-q')
        (repo / 'a.py').write_text('x = 1\n')
        harness.git(repo, 'add', '-A')
        harness.git(repo, '-c', 'user.name=t', '-c', 'user.email=t@localhost', 'commit', '-qm', 'base')
        harness.git(repo, 'tag', 'base')
        self.assertIn('error', harness.quality(repo, 'exit 3'))
        self.assertIn('error', harness.quality(repo, 'true'))  # no output is not "no issues"
        self.assertEqual(harness.quality(repo, 'echo []')['new'], 0)
        self.assertIn('error', harness.quality(repo, 'echo \'[{"rule": null, "path": "a.py"}]\''))
        for bad in ('[null]', '[1]', '["x"]'):
            self.assertIn('error', harness.quality(repo, f"echo '{bad}'"))

    def test_unittest_parser(self):
        (self.root / 'test_sample.py').write_text('import unittest\nclass T(unittest.TestCase):\n def test_ok(self): pass\n def test_fail(self): self.fail()\n def test_error(self): raise ValueError()\n')
        result, code = harness.unittest_results(self.root, 'python3 -B -m unittest -v')
        self.assertEqual(sorted(result.values()), ['ERROR', 'FAIL', 'ok'])
        self.assertNotEqual(code, 0)

    def test_cases_and_grade(self):
        for case in harness.load_cases('all'):
            with self.subTest(case=case['id']):
                public = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-v'], cwd=case['dir'] / 'repo', capture_output=True)
                self.assertEqual(public.returncode, 0, public.stderr.decode())
                if case['kind'] != 'task':
                    continue
                trial = self.root / case['id']
                trial.mkdir()
                repo = harness.stage(case, trial)
                shutil.copytree(case['dir'] / 'fake' / 'solution', repo, dirs_exist_ok=True)
                r = harness.grade(case, repo, trial)
                self.assertGreater(r['fail_to_pass_total'], 0)
                self.assertEqual(r['fail_to_pass'], r['fail_to_pass_total'])
                self.assertEqual(r['pass_to_pass'], r['pass_to_pass_total'])
                self.assertTrue(r['solved'])

    def test_environment(self):
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'secret', 'OTHER_TOKEN': 'secret', 'CLAUDE_CODE_OAUTH_TOKEN': 'allowed'}):
            env = harness.child_env(self.root, options(), 'x')
        self.assertNotIn('OPENAI_API_KEY', env)
        self.assertNotIn('OTHER_TOKEN', env)
        self.assertEqual(env['CLAUDE_CODE_OAUTH_TOKEN'], 'allowed')
        self.assertEqual(env['HOME'], str(self.root / 'home'))

    @unittest.skipUnless(shutil.which('ruff'), 'ruff missing')
    def test_quality(self):
        _, _, repo = self.fixture()
        (repo / 'app.py').write_text('import os\n')
        self.assertEqual(harness.quality(repo)['new'], 1)
        harness.git(repo, 'add', '-A')
        harness.git(repo, 'commit', '-qm', 'test(fixture): seed lint')
        harness.git(repo, 'tag', '-f', 'base')
        (repo / 'app.py').write_text('value = 1\n')
        self.assertEqual(harness.quality(repo)['fixed'], 1)

    def test_timeout(self):
        marker = self.root / 'terminated'
        child = ("import signal,time,pathlib,sys; "
                 f"signal.signal(signal.SIGTERM, lambda *_: (pathlib.Path({str(marker)!r}).write_text('yes'), sys.exit(0))); "
                 "print('ready', flush=True); time.sleep(60)")
        parent = ("import subprocess,sys,time; "
                  f"p=subprocess.Popen([sys.executable, '-c', {child!r}], stdout=subprocess.PIPE); "
                  "p.stdout.readline(); time.sleep(60)")
        status, _ = harness.run_proc([sys.executable, '-c', parent], self.root,
                                     os.environ.copy(), '', 1, self.root / 'out', self.root / 'err')
        self.assertEqual(status, 'timeout')
        # A marker proves TERM reached the descendant, not just the group leader.
        self.assertEqual(marker.read_text(), 'yes')

    def test_reader_sessions_are_swept(self):
        (self.root / 'logs').mkdir()
        p = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)'], start_new_session=True)
        (self.root / 'logs' / 'reader-1.pgid').write_text(str(p.pid))
        harness.sweep_readers(self.root)
        self.assertEqual(p.wait(timeout=10), -9)

    def test_timeout_term_resistant_descendant(self):
        # F4: leader exit must not stop group cleanup.
        pidfile = self.root / 'child.pid'
        child = "import signal,time; signal.signal(signal.SIGTERM, signal.SIG_IGN); print('ready', flush=True); time.sleep(60)"
        parent = ("import subprocess,sys,time,pathlib; "
                  f"p=subprocess.Popen([sys.executable, '-c', {child!r}], stdout=subprocess.PIPE); "
                  f"p.stdout.readline(); pathlib.Path({str(pidfile)!r}).write_text(str(p.pid)); time.sleep(60)")
        harness.run_proc([sys.executable, '-c', parent], self.root, os.environ.copy(), '', 1,
                         self.root / 'out', self.root / 'err')
        pid = int(pidfile.read_text())
        try:
            with self.assertRaises(ProcessLookupError):
                os.kill(pid, 0)
        finally:
            try:
                os.kill(pid, 9)
            except ProcessLookupError:
                pass

    def test_rules(self):
        case, trial, repo = self.fixture()
        env = harness.child_env(trial, options(), case['id'])
        ticket = case['id']
        for snap, content in [('scratch-1', 'old'), ('scratch-final', 'replacement')]:
            folder = trial / 'logs' / snap / ticket
            folder.mkdir(parents=True)
            (folder / 'repo-review-ledger.md').write_text(content)
        (repo / 'extra').write_text('changed')
        harness.git(repo, 'add', '-A')
        harness.git(repo, 'commit', '-qm', 'test(fixture): change')
        harness.git(repo, 'push', 'origin', 'main')
        with patch.dict(os.environ, env):
            r = harness.rules(trial, repo, ticket)
        self.assertFalse(r['ledger_append_only'])
        self.assertFalse(r['push_had_receipt'])

    def test_end_to_end(self):
        result = subprocess.run([sys.executable, '-B', str(EVAL / 'run.py'), 'run', '--suite', 'all', '--repeats', '1', '--output', str(self.root)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        output = next(self.root.glob('*/results.jsonl'))
        self.assertEqual(list(output.parent.glob('*/logs/reader-*.pgid')), [])  # finished Reader calls leave no record
        self.assertTrue(list(output.parent.glob('*/logs/reader-1.jsonl')))
        rows = [json.loads(line) for line in output.read_text().splitlines()]
        kinds = [c['kind'] for c in harness.load_cases('all')]
        self.assertEqual(len(rows), kinds.count('review') + 2 * kinds.count('task'))  # tasks run single and workflow
        self.assertTrue(all(r['status'] == 'ok' for r in rows), rows)
        self.assertTrue(all(r['tests']['solved'] for r in rows if r['kind'] == 'task'))
        self.assertIn('Fake agents', output.with_name('report.md').read_text())
        judged = subprocess.run([sys.executable, '-B', str(EVAL / 'run.py'), 'judge', str(output.parent)],
                                capture_output=True, text=True)
        self.assertEqual(judged.returncode, 0, judged.stderr)
        verdicts = [json.loads(line) for line in (output.parent / 'judge' / 'judge.jsonl').read_text().splitlines()]
        self.assertTrue(verdicts and all(v['prefer'] == 'tie' for v in verdicts), verdicts)

    def test_claude_result_sums_segments(self):
        def seg(cost, out):
            return json.dumps({'type': 'result', 'subtype': 'success', 'total_cost_usd': cost,
                               'usage': {'output_tokens': out, 'service_tier': 'standard'}})
        r = harness.claude_result('\n'.join([seg(1.0, 10), 'not json', seg(2.5, 5)]))
        self.assertEqual((r['total_cost_usd'], r['usage'], r['segments']), (2.5, {'output_tokens': 15}, 2))
        self.assertIsNone(harness.claude_result('{"type": "assistant"}'))

    def test_arm_prompts(self):
        case, trial, repo = self.fixture()
        captured = {}
        def fake_run(argv, cwd, env, stdin_text, timeout, out, err):
            captured['system'] = argv[argv.index('--append-system-prompt') + 1]
            Path(out).write_text('')
            return 'ok', 0.0
        for arm, require_map in (('review-only', False), ('workflow', True)):
            t = self.root / arm
            t.mkdir()
            with patch.object(harness, 'run_proc', fake_run), patch.object(harness, 'grade', lambda *a: {}), \
                    patch.object(harness, 'quality', lambda *a: {}), patch.object(harness, 'rules', lambda *a: {}):
                harness.task_trial(case, arm, t, argparse.Namespace(**{**vars(options()), 'require_map': require_map}))
            system = captured['system']
            self.assertIn('How this evaluation wires the workflow', system)
            self.assertNotIn('__', system.replace('__init__', ''))
            if arm == 'review-only':
                self.assertNotIn('map.md', system)
                self.assertNotIn('decisions.md', system)
            else:
                self.assertIn('This task is not small', system)

    def test_unblind(self):
        v = {'A': [{'severity': 'blocking'}], 'B': [], 'prefer': 'A', 'why': 'x'}
        self.assertEqual(harness.unblind(v, 'fwd')['prefer'], 'single')
        self.assertEqual(harness.unblind(v, 'rev')['prefer'], 'workflow')
        self.assertEqual(harness.unblind(v, 'rev')['workflow'], v['A'])
        self.assertEqual(harness.unblind(dict(v, prefer='?'), 'fwd')['prefer'], 'tie')
        self.assertEqual(harness.unblind(v, 'fwd', ('review-only', 'workflow'))['prefer'], 'review-only')
        self.assertEqual(harness.TRIAL_DIR.match('task-a-review-only-2').groups(), ('task-a', 'review-only', '2'))
        self.assertEqual(harness.parse_verdict('noise {"A": [], "B": [], "prefer": "B"} end')['prefer'], 'B')
        self.assertIsNone(harness.parse_verdict('{"A": "x"}'))
        self.assertIsNone(harness.parse_verdict('no json'))

    def test_change_diff_includes_untracked(self):
        case, trial, repo = self.fixture()
        (repo / 'new_file.py').write_text('x = 1\n')
        self.assertIn('new_file.py', harness.change_diff(repo))
        self.assertEqual(harness.git(repo, 'status', '--short', '--', 'new_file.py'), '?? new_file.py')  # real index untouched

    def test_failure_recorded(self):
        case = next(c for c in harness.load_cases('review') if c['id'] == 'review-clean')
        (self.root / 'case').mkdir()
        (self.root / 'case' / 'config.json').write_text('{"mode":"nonzero"}')
        result = harness.review_trial(case, self.root, options())
        self.assertNotEqual(result['status'], 'ok')
