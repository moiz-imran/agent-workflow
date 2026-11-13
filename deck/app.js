const deck = [
  {
    "name": "Title",
    "minutes": "0 min",
    "states": [
      {
        "title": "Building Agent Workflows for Better Code",
        "caption": "How I run a large coding task across two models.",
        "task": 90,
        "label": "Task",
        "visual": "title"
      }
    ]
  },
  {
    "name": "Why I use this",
    "minutes": "3 min",
    "states": [
      {
        "title": "Why I set it up this way",
        "caption": "How I use a multi-agent harness to structure a large coding task.",
        "task": 90,
        "label": "Task",
        "visual": "cover",
        "issue": "ready"
      },
      {
        "title": "Why I set it up this way",
        "caption": "I wanted both models available throughout my workweek.",
        "task": 90,
        "label": "Task",
        "visual": "cover",
        "issue": "usage",
        "dwell": 9000
      },
      {
        "title": "Why I set it up this way",
        "caption": "At medium effort, investigation stayed in one thread.",
        "task": 90,
        "label": "Task",
        "visual": "cover",
        "issue": "rules",
        "dwell": 7600
      },
      {
        "title": "Why I set it up this way",
        "caption": "An important choice can get buried in a plan.",
        "task": 90,
        "label": "Task",
        "visual": "cover",
        "issue": "decision",
        "dwell": 11000
      },
      {
        "title": "Why I set it up this way",
        "caption": "I was keeping the review rounds moving myself.",
        "task": 90,
        "label": "Task",
        "visual": "cover",
        "issue": "review"
      }
    ]
  },
  {
    "name": "The starting point",
    "minutes": "½ min",
    "states": [
      {
        "title": "What goes into the task",
        "caption": "The inputs come together in one task.",
        "task": 230,
        "label": "Task",
        "visual": "flow",
        "process": "inputs"
      }
    ]
  },
  {
    "name": "Reader",
    "minutes": "1½ min",
    "states": [
      {
        "title": "Give investigation its own context",
        "caption": "In my setup, Sol reads and reviews. Opus builds.",
        "task": 230,
        "label": "Investigating",
        "visual": "flow",
        "trip": "reader",
        "station": "Tracing the code",
        "roleIntro": true
      }
    ]
  },
  {
    "name": "Inside the Reader",
    "minutes": "1 min",
    "states": [
      {
        "title": "The exploration stays here",
        "caption": "The Reader keeps the exploration; the Builder gets the relevant findings.",
        "task": 230,
        "label": "Investigating",
        "visual": "evidence"
      },
      {
        "title": "The useful evidence comes back",
        "caption": "The Reader sends a map the Builder can follow.",
        "task": 230,
        "label": "Handoff ready",
        "visual": "flow",
        "trip": "reader",
        "back": true,
        "station": "Handoff delivered",
        "payload": [
          "Reader handoff",
          "Behavior · Code links · Open questions"
        ]
      }
    ]
  },
  {
    "name": "The handoff",
    "minutes": "2 min",
    "states": [
      {
        "title": "A map the Builder can work from",
        "caption": "The handoff puts the useful evidence within reach.",
        "task": 230,
        "label": "Handoff ready",
        "visual": "map",
        "reveal": 0
      },
      {
        "title": "Leave a way back to the code",
        "caption": "A source reference lets the Builder check a claim when it needs to.",
        "task": 230,
        "label": "Handoff ready",
        "visual": "map",
        "reveal": 1
      },
      {
        "title": "Keep the uncertainty visible",
        "caption": "An open question gives us something to resolve before it becomes an assumption.",
        "task": 230,
        "label": "Handoff ready",
        "visual": "map",
        "reveal": 2
      }
    ]
  },
  {
    "name": "Builder",
    "minutes": "1½ min",
    "states": [
      {
        "title": "Build from the handoff",
        "caption": "The Builder works from the reviewed spec, the map, and current decisions.",
        "task": 480,
        "label": "Building",
        "visual": "flow",
        "process": "handoff",
        "dwell": 7000
      }
    ]
  },
  {
    "name": "A choice during the build",
    "minutes": "2½ min",
    "states": [
      {
        "title": "Opus resolves most decisions from the spec",
        "caption": "Moved, but nothing changed. Notify followers?",
        "task": 480,
        "label": "Opus · Needs input",
        "visual": "flow",
        "reveal": 2,
        "pause": true,
        "process": "reasoning",
        "chain": true
      },
      {
        "title": "New business logic needs a decision",
        "caption": "Moved, but nothing changed. Notify followers?",
        "task": 480,
        "label": "Needs a decision",
        "visual": "flow",
        "trip": "decision",
        "station": "Notify on a move?",
        "pause": true,
        "packetLabel": "D1 · Question",
        "process": "reasoning",
        "reveal": 2
      },
      {
        "title": "One call to make",
        "caption": "Notifying on moves would expand the behavior we build and check.",
        "task": 480,
        "label": "Needs a decision",
        "visual": "choice",
        "pause": true
      },
      {
        "title": "Return the answer to the work",
        "caption": "Don’t notify on a move.",
        "task": 480,
        "label": "Scope recorded",
        "visual": "flow",
        "trip": "decision",
        "back": true,
        "station": "Decision recorded",
        "payload": [
          "D1 · Current decision",
          "Don’t notify on a move."
        ],
        "packetLabel": "D1"
      }
    ]
  },
  {
    "name": "The decision record",
    "minutes": "1½ min",
    "states": [
      {
        "title": "Every decision, with its history",
        "caption": "The Builder and Reviewer work from the same decisions.",
        "task": 480,
        "label": "Scope recorded",
        "visual": "record"
      }
    ]
  },
  {
    "name": "Review intake",
    "minutes": "2 min",
    "states": [
      {
        "title": "Define what this review covers",
        "caption": "The reviewed spec, current decisions, and the version to check.",
        "task": 740,
        "label": "Change v1",
        "visual": "intake",
        "reveal": 0
      },
      {
        "title": "Send v1 for review",
        "caption": "The Reviewer checks v1 and returns a finding.",
        "task": 740,
        "label": "Change v1",
        "visual": "flow",
        "trip": "review",
        "back": true,
        "roundTrip": "v1 · D1",
        "station": "Finding returned",
        "payload": [
          "F1 · v1",
          "The copy kept the original’s followers."
        ],
        "packetLabel": "F1 · v1",
        "finding": "open"
      }
    ]
  },
  {
    "name": "Repair and recheck",
    "minutes": "2 min",
    "states": [
      {
        "title": "Fix it and check again",
        "caption": "The Builder repairs F1, and v2 comes back verified.",
        "task": 740,
        "label": "Checked v2",
        "visual": "flow",
        "trip": "review",
        "back": true,
        "roundTrip": "v2 · F1",
        "repair": true,
        "station": "v2 check returned",
        "payload": [
          "F1 · Verified on v2",
          "The copy now starts with no followers."
        ],
        "packetLabel": "F1 · v2",
        "finding": "verified"
      }
    ]
  },
  {
    "name": "What was checked",
    "minutes": "3 min",
    "states": [
      {
        "title": "Keep the result with its version",
        "caption": "Each finding has an outcome and a code version behind it.",
        "task": 740,
        "label": "Checked v2",
        "visual": "ledger",
        "reveal": 0,
        "finding": "verified"
      },
      {
        "title": "The review has a clear endpoint",
        "caption": "A clean review, or the push stops.",
        "task": 740,
        "label": "Checked v2",
        "visual": "clean",
        "reveal": 1,
        "finding": "verified"
      },
      {
        "title": "Read before it goes out",
        "caption": "I read every change before anyone else does.",
        "task": 740,
        "label": "Checked v2",
        "visual": "flow",
        "trip": "decision",
        "station": "Self-review",
        "packetLabel": "Self-review · v2",
        "selfReview": true
      },
      {
        "visual": "flow",
        "title": "A human can still send it back",
        "caption": "A clean internal result can still be the wrong design.",
        "task": 905,
        "label": "Changes requested",
        "alert": true,
        "trip": "human",
        "back": true,
        "station": "Finding returned",
        "packetLabel": "H1",
        "roundTrip": "PR · v2",
        "payload": [
          "H1 · Changes requested",
          "Rework the design."
        ]
      },
      {
        "visual": "flow",
        "title": "Back through the gate",
        "caption": "v3 is reviewed again, and this time it’s approved.",
        "task": 905,
        "label": "Approved v3",
        "trip": "human",
        "station": "Approved v3",
        "packetLabel": "PR · v3",
        "returnPacketLabel": "H1 · Clean on v3",
        "roundTrip": "v3 · H1"
      },
      {
        "title": "The miss becomes a rule",
        "caption": "The human finding becomes part of future reviews.",
        "task": 905,
        "label": "Ready to merge",
        "visual": "flow",
        "trip": "review",
        "station": "Rule · Challenge the design",
        "packetLabel": "H1 · Rework the design",
        "reviewRule": true
      }
    ]
  },
  {
    "name": "Where I use it",
    "minutes": "1½ min",
    "states": [
      {
        "title": "When I use more of the setup",
        "caption": "Each handoff needs enough work to justify it.",
        "task": 905,
        "label": "Ready to merge",
        "visual": "fit",
        "finding": "verified"
      }
    ]
  },
  {
    "name": "How I set this up",
    "minutes": "½ min",
    "states": [
      {
        "title": "This is how I’ve set this up",
        "caption": "The delegation rules are instructions. The push gate is enforced.",
        "task": 905,
        "label": "Ready to merge",
        "visual": "setup",
        "reveal": 2,
        "finding": "verified"
      }
    ]
  },
  {
    "name": "Close",
    "minutes": "Questions",
    "states": [
      {
        "title": "What it gave me",
        "caption": "The four things I wanted, and where each one ended up.",
        "task": 905,
        "label": "Ready to merge",
        "visual": "payoff"
      }
    ]
  },
  {
    "name": "Questions",
    "minutes": "Q&A",
    "states": [
      {
        "title": "Thank you",
        "caption": "Questions?",
        "task": 90,
        "label": "Task",
        "visual": "end"
      }
    ]
  }
];

const $ = id => document.getElementById(id);
const params = new URLSearchParams(location.search);
const isPresenter = params.get('view') === 'presenter';
let audienceMode = params.get('view') === 'audience';
let index = 0, step = 0, start = Date.now(), channel, presenterWindow, notesFocus;
let playing = false, playTimer, lastBeat = -1, frame = 0, surfaceFrame = 0, previousVisual, decisionFlight;
const reduced = matchMedia('(prefers-reduced-motion: reduce)');
const beats = deck.flatMap((act, index) => act.states.map((state, step) => ({ ...state, index, step })));
const total = beats.length;
// ponytail: found by title so merging or deleting steps can't shift them
const beatTitled = title => beats.findIndex(beat => beat.title === title);
const decisionPinBeat = beatTitled('Return the answer to the work');
const pushGateBeat = beatTitled('The review has a clear endpoint');
const pushGatePassBeat = beats.findIndex(beat => beat.returnPacketLabel);
const railY = 196;
const pushGateX = 825;
const routes = {
  reader: {
    label: 'Reader', detail: 'Separate context', x: 48, y: 16,
    path: 'M230 196V156Q230 131 205 131H201Q182 131 182 106'
  },
  decision: {
    label: 'Me', detail: 'Business logic', x: 424, y: 16,
    path: 'M480 196V165Q480 142 504 142H535Q560 142 560 118V106'
  },
  review: {
    label: 'Reviewer', detail: 'Independent context', x: 737, y: 294,
    path: 'M740 196V247Q740 274 766 274H853Q878 274 878 294'
  },
  human: {
    label: 'Human reviewer', detail: 'PR review', x: 800, y: 16,
    path: 'M905 196V164Q905 142 927 142H928Q950 142 950 120V106'
  }
};
const firstBeat = Object.fromEntries(Object.keys(routes).map(key => [key, beats.findIndex(beat => beat.trip === key)]));

const visuals = {
  cover: `
    <div class="opening-stage" id="opening-stage">
      <div class="opening-jobs">
        <div data-issue-label="usage"><span>01</span><p>Keep both models available</p></div>
        <div data-issue-label="rules"><span>02</span><p>Make the working rules explicit</p></div>
        <div data-issue-label="decision"><span>03</span><p>Keep every decision visible</p></div>
        <div data-issue-label="review"><span>04</span><p>Stop carrying review findings</p></div>
      </div>
      <div class="opening-demos">
        <section class="opening-demo usage-demo" data-issue-panel="usage" aria-label="Illustration of running out of one provider, then dividing work across both">
          <svg class="usage-diagram" viewBox="0 0 560 250" role="img" aria-label="Opus builds; Sol investigates and reviews">
            <path class="usage-route" id="usage-switch" d="M310 65H420Q446 65 446 91V159Q446 185 420 185H310"/>
            <g class="usage-provider"><rect x="20" y="32" width="285" height="66" rx="12"/><text x="40" y="59">Opus</text><text class="usage-detail" x="40" y="83">Claude Code</text></g>
            <g class="usage-provider"><rect x="20" y="152" width="285" height="66" rx="12"/><text x="40" y="179">Sol</text><text class="usage-detail" x="40" y="203">Codex</text></g>
            <g class="usage-before"><g class="usage-stack"><rect x="172" y="51" width="26" height="28" rx="4"/><rect x="208" y="51" width="26" height="28" rx="4"/><rect x="244" y="51" width="26" height="28" rx="4"/></g><text class="usage-limit" x="320" y="28">Allowance reached</text><circle class="usage-packet" r="7" cx="0" cy="0"/></g>
            <g class="usage-after"><text x="169" y="72">Build</text><text x="169" y="180">Investigate</text><text x="169" y="202">&amp; review</text><path class="usage-join" d="M310 65H420Q446 65 446 91V159Q446 185 420 185H310"/></g>
          </svg>
          <p class="opening-outcome usage-outcome">Divide the effort. Keep both available.</p>
        </section>
        <section class="opening-demo rules-demo" data-issue-panel="rules" aria-label="At medium effort, investigation fills the one thread; at max effort, a Haiku subagent takes the investigation" hidden>
          <div class="effort-row medium-row">
            <div class="meter-heading"><span class="effort-chip">Medium effort</span><span class="meter-limit">One thread</span></div>
            <div class="effort-meter"><div class="effort-fill"></div><span class="effort-label">Investigation + build</span></div>
          </div>
          <div class="effort-row max-row">
            <div class="meter-heading"><span class="effort-chip">Max effort</span><span class="meter-limit">Main thread</span></div>
            <div class="effort-meter"><div class="effort-fill"></div><span class="effort-label">Build</span></div>
            <div class="subagent-chip">↳ Haiku subagent · investigation</div>
          </div>
          <p class="opening-outcome effort-outcome">Medium lasts the week, so delegation became a rule.</p>
        </section>
        <section class="opening-demo decision-demo" data-issue-panel="decision" aria-label="A long implementation plan with a decision to include existing records buried in section 13" hidden>
          <div class="plan-heading"><span class="visual-kicker">Implementation plan</span><span class="plan-length">24 sections</span></div>
          <div class="scope-viewport">
            <div class="scope-messages">
              <div class="scope-message"><span>01</span><div><h3>Trace the request</h3><p>Follow the request from the entry point through validation, persistence, and the response. Note where the current behavior depends on shared helpers.</p></div></div>
              <div class="scope-message"><span>02</span><div><h3>Map the affected callers</h3><p>Find each caller of the update handler and record which fields it provides. Check synchronous requests and background jobs separately.</p></div></div>
              <div class="scope-message"><span>03</span><div><h3>Inspect the data model</h3><p>Review the stored fields, indexes, and relationships used by this flow. Keep the current identifiers and preserve unrelated values.</p></div></div>
              <div class="scope-message"><span>04</span><div><h3>Read the existing tests</h3><p>Identify fixtures that exercise successful updates, rejected input, and retries. Record any setup shared with neighboring features.</p></div></div>
              <div class="scope-message"><span>05</span><div><h3>Define the handler contract</h3><p>List the values the handler requires and the result it returns. Preserve the response shape used by existing clients.</p></div></div>
              <div class="scope-message"><span>06</span><div><h3>Update input validation</h3><p>Validate required fields before writing data. Keep error responses consistent with the rest of the endpoint and cover empty values.</p></div></div>
              <div class="scope-message"><span>07</span><div><h3>Prepare the query</h3><p>Select only the records needed for the operation. Retain the existing filters and ordering so callers receive predictable results.</p></div></div>
              <div class="scope-message"><span>08</span><div><h3>Implement the update</h3><p>Apply the new values within the current transaction boundary. Keep unrelated fields intact and avoid issuing duplicate writes.</p></div></div>
              <div class="scope-message"><span>09</span><div><h3>Handle retries</h3><p>Make repeated requests safe to process. Check that a retry cannot create duplicate events or overwrite a newer value.</p></div></div>
              <div class="scope-message"><span>10</span><div><h3>Update the event payload</h3><p>Include the fields downstream consumers need. Preserve existing event names and make optional additions compatible with older consumers.</p></div></div>
              <div class="scope-message"><span>11</span><div><h3>Check dependent services</h3><p>Trace each consumer through its own validation and persistence. Confirm that the revised payload preserves the behavior those services expect.</p></div></div>
              <div class="scope-message"><span>12</span><div><h3>Keep audit history</h3><p>Record the actor and changed fields using the existing audit mechanism. Keep event ordering consistent with the committed write.</p></div></div>
              <div class="scope-message"><span>13</span><div><h3>Review the rollout</h3><p>Keep the response format compatible with current callers. <mark class="scope-choice">Include existing records.</mark> Process updates in batches through the same handler, retaining the usual validation and retry behavior.</p></div></div>
              <div class="scope-message"><span>14</span><div><h3>Update background jobs</h3><p>Pass the revised fields through the job payload. Retain the existing retry settings and surface failed work through the normal error path.</p></div></div>
              <div class="scope-message"><span>15</span><div><h3>Handle partial failures</h3><p>Keep successful writes committed where the operation permits it. Return enough detail to identify failed items without repeating completed work.</p></div></div>
              <div class="scope-message"><span>16</span><div><h3>Refresh the fixtures</h3><p>Add records with missing optional fields and varied relationships. Reuse the existing test helpers so the setup stays representative.</p></div></div>
              <div class="scope-message"><span>17</span><div><h3>Test normal updates</h3><p>Check the returned values and the stored state. Verify that related events contain the expected fields after a successful write.</p></div></div>
              <div class="scope-message"><span>18</span><div><h3>Test invalid requests</h3><p>Cover missing values, invalid identifiers, and conflicting updates. Confirm that rejected requests leave persisted data unchanged.</p></div></div>
              <div class="scope-message"><span>19</span><div><h3>Test retry behavior</h3><p>Repeat successful and interrupted requests. Verify that the final state and audit history match the expected number of operations.</p></div></div>
              <div class="scope-message"><span>20</span><div><h3>Check integration paths</h3><p>Exercise the endpoint with its downstream consumers. Cover the background job path as well as direct requests from the application.</p></div></div>
              <div class="scope-message"><span>21</span><div><h3>Review query performance</h3><p>Check the queries against representative data volumes. Confirm that existing indexes support the filters used by the updated handler.</p></div></div>
              <div class="scope-message"><span>22</span><div><h3>Run the required checks</h3><p>Run formatting, static analysis, and the relevant test suites. Investigate failures before considering the implementation ready for review.</p></div></div>
              <div class="scope-message"><span>23</span><div><h3>Update the documentation</h3><p>Describe the request fields and response behavior. Keep examples consistent with the implemented validation and event payload.</p></div></div>
              <div class="scope-message"><span>24</span><div><h3>Prepare the review</h3><p>Summarize the changed behavior and link the relevant checks. Include the affected callers and any remaining questions for the reviewer.</p></div></div>
            </div>
            <div class="plan-scrollbar" aria-hidden="true"><i></i></div>
          </div>
          <p class="opening-outcome scope-outcome">It changes the scope, and nothing flagged it as a decision.</p>
        </section>
        <section class="opening-demo review-demo" data-issue-panel="review" aria-label="The developer repeatedly carries revised code to the Reviewer and findings to the Builder" hidden>
          <svg class="courier-diagram" viewBox="0 0 560 220" role="img" aria-label="Builder to developer to Reviewer, and back">
            <path class="courier-route" d="M125 122H435"/>
            <g class="courier-station"><rect x="0" y="98" width="120" height="48" rx="12"/><text x="60" y="128" text-anchor="middle">Builder</text><text class="courier-work builder-work" x="60" y="173" text-anchor="middle">Repair</text></g>
            <g class="courier-station"><rect x="440" y="98" width="120" height="48" rx="12"/><text x="500" y="128" text-anchor="middle">Reviewer</text><text class="courier-work reviewer-work" x="500" y="173" text-anchor="middle">Check</text></g>
            <g class="courier" transform="translate(280 122)">
              <circle class="courier-core" r="15"/>
              <circle class="courier-person" cy="-4" r="3.5"/>
              <path class="courier-person" d="M-6 7Q0-2 6 7"/>
              <text class="courier-me" y="41" text-anchor="middle">Me</text>
              <g class="cargo-code"><rect x="-67" y="-66" width="134" height="29" rx="6"/><text y="-46" text-anchor="middle">Revised code</text></g>
              <g class="cargo-finding"><rect x="-53" y="-66" width="106" height="29" rx="6"/><text y="-46" text-anchor="middle">Findings</text></g>
            </g>
          </svg>
          <p class="courier-summary">Code → Reviewer <span>·</span> Findings → Builder</p>
        </section>
      </div>
    </div>
`,
  evidence: `
    <div class="evidence-layout">
      <section class="context-room">
        <span class="visual-kicker">Inside the Reader’s context</span>
        <div class="source-row"><span class="source-mark">↳</span><strong>Code path</strong><span>How the behavior starts</span></div>
        <div class="source-row"><span class="source-mark">↳</span><strong>Tests</strong><span>Cases already covered</span></div>
        <div class="source-row"><span class="source-mark">↳</span><strong>History</strong><span>Why it works this way</span></div>
      </section>
      <section class="evidence-output">
        <span class="visual-kicker">What the exploration produces</span>
        <h2>A starting point<br>for the change</h2>
        <p>Behavior to preserve</p><p>Places to verify it</p><p>Questions still open</p>
      </section>
    </div>`,
  map: `
    <div class="document-layout">
      <aside class="document-name"><span class="visual-kicker">Reader → Builder</span><h2>map.md</h2><p>A short map with a way back to the evidence.</p></aside>
      <div class="document-sheet">
        <div class="document-row" data-level="0"><span class="row-number">01</span><div><h3>Current behavior</h3><p>What happens today and what the change touches.</p></div></div>
        <div class="document-row" data-level="1"><span class="row-number">02</span><div><h3>Code references</h3><p>Entry points and tests the Builder can inspect.</p></div></div>
        <div class="document-row" data-level="2"><span class="row-number">03</span><div><h3>Open questions</h3><p>Choices that could change the implementation.</p></div></div>
      </div>
    </div>`,
  choice: `
    <div class="choice-layout">
      <div class="choice-source"><span class="visual-kicker"><span class="artifact-key human-key">D1</span> My call</span><h2>Notify on a move?</h2></div>
      <div class="choice-options"><div><span class="choice-letter">A</span><h3>Notify</h3><p>Count a move<br>as a change.</p></div><div><span class="choice-letter">B</span><h3>Don’t notify</h3><p>Keep moves<br>outside this change.</p></div></div>
    </div>`,
  record: `
    <div class="document-layout">
      <aside class="document-name"><span class="visual-kicker">With the task</span><h2>decisions.md</h2><p>One current answer for the next session.</p></aside>
      <div class="decision-sheet">
        <div class="record-question"><span class="visual-kicker"><span class="artifact-key decision-key">D1</span> Business decision</span><h3>Notify on a move?</h3></div>
        <div class="record-answer"><span class="current-badge">Current answer</span><h2>Don’t notify on a move.</h2></div>
        <p>The current answer goes into the build and the next review brief.</p>
        <div class="record-revision">
          <span class="artifact-key decision-key">D2</span>
          <div>
            <div><span>Superseded</span> <del>Notify on every save.</del></div>
            <div><span>Current answer</span> Formatting-only edits don’t notify.</div>
          </div>
        </div>
      </div>
    </div>`,
  ledger: `
    <div class="document-layout">
      <aside class="document-name"><span class="visual-kicker">Every round</span><h2>review-ledger.md</h2><p>Each finding, its fix and its check, tied to a version.</p></aside>
      <div class="document-sheet ledger-sheet">
        <div class="document-row"><span class="row-number">v1</span><div><h3>Round 1 · <span class="artifact-key">F1</span> Open</h3><p>The copy kept the original’s followers.</p></div></div>
        <div class="document-row"><span class="row-number">v2</span><div><h3>Fixed · <code>copy.ts:42</code></h3><p>Copies now start with no followers.</p></div></div>
        <div class="document-row ledger-verified"><span class="row-number">v2</span><div><h3>Round 2 · <span class="artifact-key verified-key">F1</span> Verified</h3><p>tsc ✓ · eslint ✓ · vitest ✓</p></div></div>
      </div>
    </div>`,
  intake: `
    <div class="intake-layout">
      <div class="snapshot"><span class="visual-kicker">Code snapshot</span><h2>v1</h2><span>The version to check</span></div>
      <div class="review-brief">
        <span class="visual-kicker">Fresh review context</span>
        <div class="brief-line" data-level="0"><b>Expected behavior</b><span>Reviewed spec + current decisions</span></div>
        <div class="brief-line decision-brief" data-level="0"><b>Current decision</b><span><span class="artifact-key decision-key">D1</span> Don’t notify on a move.</span></div>
      </div>
    </div>`,
  clean: `
    <div class="clean-layout">
      <section class="severity-scale">
        <span class="visual-kicker">Round 2 · v2 findings</span>
        <ol>
          <li class="above"><b>Blocking</b><span>0</span></li>
          <li class="above"><b>Should-fix</b><span>0</span></li>
          <li class="severity-bar"><span>The bar</span></li>
          <li><b>Minor</b><span>1</span></li>
          <li><b>Nit</b><span>2</span></li>
        </ol>
      </section>
      <section class="clean-outcome">
        <span class="visual-kicker">Nothing above the bar</span>
        <h2>CLEAN</h2>
        <div class="gate-row gate-open"><b>Clean</b><span>Push and PR allowed <i>→</i> human reviewer</span></div>
        <div class="gate-row gate-blocked"><b>Not clean</b><span>A hook blocks any push or PR</span></div>
      </section>
    </div>`,
  fit: `
    <div class="fit-layout">
      <section><span class="visual-kicker">When I keep it light</span><h2>A small edit<br>in familiar code</h2><p>I can brief the Builder directly.</p><div class="fit-route">Brief <span>→</span> Build <span>→</span> Check</div></section>
      <section><span class="visual-kicker">When I use more of the setup</span><h2>A long investigation<br>or several review rounds</h2><p>The handoffs have more work to carry.</p><div class="fit-route">Reader <span>→</span> Build <span>⇄</span> Review</div></section>
      <p class="cost-note">Each review round uses time and allowance.</p>
    </div>`,
  setup: `
    <div class="setup-excerpt">
      <div class="setup-file"><h2>CLAUDE.md</h2><span>Automatic Codex delegation · excerpt</span></div>
      <p class="setup-rule" data-level="0">Keep Claude Code and Opus 5.5 as the main harness and substantive implementation author.</p>
      <p class="setup-rule" data-level="1">Automatically delegate substantial investigation, reproduction, tests, verification, independent review and localized mechanical/standards/simplicity repairs to Codex.</p>
      <p class="setup-rule" data-level="2">Group supporting work into coarse handoffs; finish small straightforward tasks directly.</p>
      <div class="setup-hook"><span class="setup-hook-label">settings.json · PreToolUse hook · enforced</span><p><code>git push</code>, <code>gh pr create</code> → blocked without a <b>CLEAN</b> review</p></div>
    </div>`,
  title: `
    <div class="bookend">
      <span class="bookend-thread" aria-hidden="true"><i></i></span>
      <h2>Building Agent Workflows<br>for Better Code</h2>
      <p>How I run a large coding task across two models.</p>
      <span class="bookend-name">Moiz Imran</span>
    </div>`,
  end: `
    <div class="bookend">
      <span class="bookend-thread" aria-hidden="true"><i></i></span>
      <h2>Thank you</h2>
      <p>Questions?</p>
      <span class="bookend-name">Moiz Imran</span>
    </div>`,
  payoff: `
    <div class="payoff-layout">
      <div class="payoff-row">
        <span class="payoff-mark"><span class="payoff-num">01</span><svg class="payoff-check" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="11"/><path d="M7 12.5l3.2 3.2L17 9"/></svg></span>
        <div class="payoff-want"><p>Keep both models available</p><span class="payoff-before">Ran out of Claude first</span></div>
        <span class="payoff-link" aria-hidden="true"><i></i></span>
        <div class="payoff-tile"><span class="visual-kicker">Two models</span><h3>Opus builds, Sol checks</h3><p>My quota lasts the week</p></div>
      </div>
      <div class="payoff-row">
        <span class="payoff-mark"><span class="payoff-num">02</span><svg class="payoff-check" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="11"/><path d="M7 12.5l3.2 3.2L17 9"/></svg></span>
        <div class="payoff-want"><p>Make the working rules explicit</p><span class="payoff-before">Repeating the same asks</span></div>
        <span class="payoff-link" aria-hidden="true"><i></i></span>
        <div class="payoff-tile"><span class="visual-kicker">CLAUDE.md</span><h3>Standing rules</h3><p>Work delegated, push gate enforced</p></div>
      </div>
      <div class="payoff-row">
        <span class="payoff-mark"><span class="payoff-num">03</span><svg class="payoff-check" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="11"/><path d="M7 12.5l3.2 3.2L17 9"/></svg></span>
        <div class="payoff-want"><p>Keep every decision visible</p><span class="payoff-before">Buried in a long plan</span></div>
        <span class="payoff-link" aria-hidden="true"><i></i></span>
        <div class="payoff-tile"><span class="visual-kicker">decisions.md</span><h3>Every call, with its history</h3><p>Superseded, never lost</p></div>
      </div>
      <div class="payoff-row">
        <span class="payoff-mark"><span class="payoff-num">04</span><svg class="payoff-check" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="11"/><path d="M7 12.5l3.2 3.2L17 9"/></svg></span>
        <div class="payoff-want"><p>Stop carrying review findings</p><span class="payoff-before">Me, relaying every round</span></div>
        <span class="payoff-link" aria-hidden="true"><i></i></span>
        <div class="payoff-tile"><span class="visual-kicker">Review loop</span><h3>Autonomous loop</h3><p>Without me in the middle</p></div>
      </div>
    </div>`
};

$('deck').innerHTML = `
  <section class="talk" aria-labelledby="talk-title">
    <header class="story-header">
      <div class="eyebrow">
        <span id="act-number"></span><span class="rule"></span><span id="act-name"></span>
        <span class="author">Moiz Imran</span>
      </div>
      <h1 id="talk-title"></h1>
    </header>
    <div class="stage">
      <div id="scene-visual" class="scene-visual"></div>
      <svg id="simulation" viewBox="0 0 1120 400" role="img" aria-labelledby="world-title">
        <title id="world-title">A code change moves along the Builder’s thread. Reader, decision, internal review and human review packets travel out and back.</title>
        <defs>
          <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
            <circle cx="2" cy="2" r="1" fill="currentColor" opacity=".11"/>
          </pattern>
        </defs>
        <rect width="1120" height="400" fill="url(#grid)"/>
        <path class="rail" d="M68 196H1048"/>
        <path id="travelled" class="rail travelled"/>
        <circle class="rail-end" cx="1048" cy="196" r="4"/>
        <text id="thread-owner" class="diagram-label" x="68" y="236">BUILDER’S THREAD</text>
        ${Object.entries(routes).map(([id, route]) => `
          <g id="branch-${id}" class="branch" visibility="hidden">
            <path id="route-${id}" class="connector" d="${route.path}"/>
            <path id="trace-${id}" class="trace" d="${route.path}" pathLength="1" visibility="hidden"/>
            <g class="station" transform="translate(${route.x} ${route.y})">
              <rect width="300" height="90" rx="16"/>
              <text id="role-${id}" class="station-kicker" x="20" y="25">${route.detail}</text>
              <text class="station-label" x="20" y="55">${route.label}</text>
              <text id="status-${id}" class="station-status" x="20" y="76"></text>
              <circle class="station-lamp" cx="271" cy="28" r="6"/>
            </g>
          </g>`).join('')}
        <path id="route-review-rule" d="M950 106V120Q950 142 928 142H927Q905 142 905 164V196H740${routes.review.path.slice('M740 196'.length)}" visibility="hidden"/>
        <g id="review-rule-tag" visibility="hidden" transform="translate(383 325)">
          <rect width="341" height="37" rx="8"/>
          <text x="170.5" y="24" text-anchor="middle">Next time, the review catches it before you do.</text>
        </g>
        <path id="route-self-review" d="M740 196H480${routes.decision.path.slice('M480 196'.length)}" visibility="hidden"/>
        <path id="self-review-link" class="connector" d="M480 196H740" visibility="hidden"/>
        <g id="payload" class="payload" visibility="hidden">
          <path id="payload-route-link" class="connector"/>
          <rect x="-209" y="0" width="418" height="54" rx="12"/>
          <text id="payload-title" class="station-kicker" x="-193" y="21"></text>
          <text id="payload-detail" x="-193" y="41"></text>
        </g>
        <g id="flow-inputs" class="process-diagram task-inputs" visibility="hidden" aria-hidden="true">
          <defs><marker id="input-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M1 1L9 5L1 9"/></marker></defs>
          <path class="process-route" id="input-spec" d="M183 104V130Q183 150 203 150H210Q230 150 230 170V180" marker-end="url(#input-arrow)"/>
          <path class="process-route" id="input-task" d="M520 104V130Q520 150 500 150H250Q230 150 230 170V180" marker-end="url(#input-arrow)"/>
          <path class="process-route" id="input-prompt" d="M857 104V130Q857 150 837 150H250Q230 150 230 170V180" marker-end="url(#input-arrow)"/>
          <g class="process-node"><rect x="83" y="40" width="200" height="64" rx="10"/><text x="99" y="66">Feature Spec</text><text class="process-detail" x="99" y="88">Human reviewed</text></g>
          <g class="process-node"><rect x="430" y="50" width="180" height="54" rx="10"/><text x="446" y="83">Task definition</text></g>
          <g class="process-node"><rect x="789" y="50" width="136" height="54" rx="10"/><text x="805" y="83">Prompt</text></g>
          <circle class="process-packet" data-route="input-spec" r="6"/><circle class="process-packet" data-route="input-task" r="6"/><circle class="process-packet" data-route="input-prompt" r="6"/>
        </g>
        <g id="flow-handoff" class="process-diagram" visibility="hidden" aria-hidden="true">
          <defs><clipPath id="handoff-build-clip"><rect id="handoff-build-extent" x="230" y="186" width="0" height="20"/></clipPath></defs>
          <path class="handoff-build-marks" clip-path="url(#handoff-build-clip)" d="${Array.from({ length: 12 }, (_, i) => `M${249 + i * 19} 191v10`).join(' ')}"/>
          <path id="handoff-source-path" class="process-route handoff-transient" pathLength="1" d="M539 246V258Q539 270 551 270H635Q647 270 647 282V292"/>
          <g id="handoff-source" class="process-node handoff-transient" transform="translate(538 292)">
            <rect width="284" height="68" rx="10"/>
            <text x="16" y="29">Opens the source it needs</text>
            <text class="process-detail" x="16" y="51">copy.ts:42</text>
          </g>
          ${['Question', 'Answer'].map(label => `
            <g id="handoff-${label.toLowerCase()}" class="packet handoff-transient">
              <rect x="-10" y="-9" width="20" height="18" rx="5"/>
              <path d="M-4 -2H4M-4 2H2"/>
              <text class="handoff-packet-label" y="-18" text-anchor="middle">${label}</text>
            </g>`).join('')}
        </g>
        <g id="flow-reasoning" class="process-diagram opus-decisions" visibility="hidden" aria-hidden="true">
          <g id="reasoning-spec"><path class="process-route" d="M480 96V175"/><g class="process-node"><rect x="424" y="42" width="180" height="54" rx="10"/><text x="440" y="75">Feature Spec</text></g></g>
          ${[
            ['Text edited?', 'Notify followers', 'M480 217V237Q480 250 460 250H240Q220 250 220 265'],
            ['Document copied?', 'Copy has no followers', 'M480 217V237Q480 250 500 250H550Q570 250 570 265'],
            ['Moved, no edits?', 'Ask me · Spec leaves it open', 'M480 217V237Q480 250 500 250H900Q920 250 920 265']
          ].map(([question, answer, path], level) => `
            <g class="reasoning-case ${level === 2 ? 'needs-human' : ''}" data-level="${level}">
              <path class="process-route" id="reasoning-route-${level}" d="${path}"/>
              <rect class="reasoning-card" x="${80 + level * 350}" y="265" width="280" height="78" rx="10"/>
              <text class="reasoning-question" x="${96 + level * 350}" y="295">${question}</text>
              <text class="process-detail reasoning-checking" x="${96 + level * 350}" y="323">Checking the spec…</text>
              <g class="reasoning-result"><text class="reasoning-answer" x="${96 + level * 350}" y="323">${answer}</text><circle class="result-ring" cx="${338 + level * 350}" cy="291" r="11"/><text class="result-icon" x="${338 + level * 350}" y="297" text-anchor="middle">${level === 2 ? '?' : '✓'}</text></g>
              <circle class="process-packet" data-route="reasoning-route-${level}" r="6"/>
            </g>`).join('')}
        </g>
        <g id="decision-pin" class="decision-pin" transform="translate(480 ${railY})" visibility="hidden">
          <path d="M0 0V28"/>
          <rect x="-17" y="28" width="34" height="22" rx="5"/>
          <text x="0" y="43" text-anchor="middle">D1</text>
        </g>
        <g id="push-gate" class="push-gate-marker" transform="translate(${pushGateX} ${railY})" visibility="hidden">
          <path d="M0 0V23"/>
          <path class="gate-lock" d="M-3 23V19a3 3 0 0 1 6 0v4"/>
          <rect x="-5" y="23" width="10" height="10" rx="2"/>
          <text x="0" y="49" text-anchor="middle">Push gate</text>
        </g>
        <g id="task" class="task">
          <rect x="-17" y="-21" width="204" height="42" rx="21"/>
          <g id="task-thinking" class="reasoning-dots" visibility="hidden"><circle cx="90" cy="-32" r="3"/><circle cx="102" cy="-32" r="3"/><circle cx="114" cy="-32" r="3"/></g>
          <circle class="task-core" r="12"/>
          <path class="task-icon" d="M-4 -3H4M-4 0H3M-4 3H1"/>
          <text id="task-label" x="21" y="6"></text>
          <g id="handoff-dock" class="handoff-dock" visibility="hidden">
            <g transform="translate(-17 28)"><rect width="41" height="22" rx="5"/><text x="20.5" y="15">Spec</text></g>
            <g id="handoff-map-chip" transform="translate(30 28)"><rect width="59" height="22" rx="5"/><text x="29.5" y="15">map.md</text></g>
            <g class="handoff-empty" transform="translate(95 28)"><rect width="142" height="22" rx="5"/><text x="71" y="15">decisions.md · empty</text></g>
          </g>
        </g>
        <g id="packet" class="packet" visibility="hidden">
          <rect x="-10" y="-9" width="20" height="18" rx="5"/>
          <path d="M-4 -2H4M-4 2H2"/>
          <line id="packet-route-link" class="connector" x1="-16" x2="-10" y2="0" style="display:none"/>
          <text id="packet-label" x="0" y="-18" text-anchor="middle"></text>
        </g>
        <g id="finding-tag" class="finding-tag" visibility="hidden">
          <rect x="0" y="-16" width="138" height="32" rx="7"/>
          <text id="finding-tag-label" x="69" y="5" text-anchor="middle"></text>
        </g>
        <foreignObject id="self-review-card" x="165" y="110" width="790" height="280" visibility="hidden">
          <section xmlns="http://www.w3.org/1999/xhtml" class="self-review-sheet" aria-label="Self-review of v2">
            <header><h2>Self-review · v2</h2><p>tsc ✓ · eslint ✓ · vitest ✓</p></header>
            <div class="self-review-content">
              <div>
                <ol class="self-review-files">
                  <li><code>copy.ts</code><span class="artifact-key verified-key">F1 fixed · line 42</span><p>Copies start with no followers</p></li>
                  <li><code>move.ts</code><span class="artifact-key decision-key">D1</span><p>Moves don’t notify</p></li>
                  <li><code>edit.ts</code><span class="artifact-key decision-key">D2</span><p>Formatting-only edits don’t notify</p></li>
                </ol>
                <div class="self-review-skim">▸ Skim · 2 test files</div>
              </div>
              <aside class="self-review-decisions"><h3>Decisions</h3>
                <p><span class="artifact-key decision-key">D1</span> Don’t notify on a move</p>
                <p class="self-review-revision"><span class="artifact-key decision-key">D2</span><span>Formatting-only edits don’t notify<del>Notify on every save</del></span></p>
              </aside>
            </div>
          </section>
        </foreignObject>
      </svg>
    </div>
    <div class="story-bottom"><p id="caption"></p><p id="closing-line" hidden></p></div>
  </section>`;

function placeTask(x) {
  $('task').setAttribute('transform', `translate(${x} ${railY})`);
  $('travelled').setAttribute('d', `M68 ${railY}H${x}`);
  $('handoff-build-extent').setAttribute('width', Math.max(0, x - 230));
  const gate = $('push-gate');
  gate.classList.toggle('passed', gate.classList.contains('armed') && x >= pushGateX);
}

function transferDecision(from) {
  const target = document.querySelector('#scene-visual .decision-key');
  if (!from || !target) return;
  const to = target.getBoundingClientRect();
  const stage = $('simulation').parentElement;
  const bounds = stage.getBoundingClientRect();
  const token = target.cloneNode(true);
  token.setAttribute('aria-hidden', 'true');
  token.classList.add('artifact-flight');
  token.style.left = to.left - bounds.left + 'px';
  token.style.top = to.top - bounds.top + 'px';
  target.classList.add('artifact-arriving');
  stage.append(token);
  const animation = token.animate([
    { transform: `translate(${from.x - to.left - to.width / 2}px, ${from.y - to.top - to.height / 2}px)` },
    { transform: 'translate(0, 0)' }
  ], { duration: 460, easing: 'cubic-bezier(0.23, 1, 0.32, 1)' });
  const finish = () => { target.classList.remove('artifact-arriving'); token.remove(); decisionFlight = undefined; };
  decisionFlight = () => { animation.cancel(); finish(); };
  animation.onfinish = finish;
}

function lightSelfReview(active) {
  $('route-decision').classList.toggle('return-lit', active);
  $('self-review-link').setAttribute('visibility', active ? 'visible' : 'hidden');
}

function paintDiagram(scene, beat, arrived) {
  $('packet').setAttribute('visibility', 'hidden');
  lightSelfReview(false);
  $('review-rule-tag').setAttribute('visibility', scene.reviewRule && arrived ? 'visible' : 'hidden');
  const reviewCard = $('self-review-card');
  reviewCard.getAnimations().forEach(animation => animation.cancel());
  const cardOpen = !!(scene.selfReview && arrived);
  reviewCard.setAttribute('visibility', cardOpen ? 'visible' : 'hidden');
  $('simulation').classList.toggle('self-review-open', cardOpen);
  $('task').classList.toggle('paused', arrived && !!(scene.pause || scene.judgment || scene.alert));
  $('task-label').textContent = scene.label;
  $('decision-pin').setAttribute('visibility', beat > decisionPinBeat || (beat === decisionPinBeat && arrived) ? 'visible' : 'hidden');
  const gate = $('push-gate');
  gate.setAttribute('visibility', beat >= pushGateBeat ? 'visible' : 'hidden');
  gate.classList.toggle('armed', beat >= pushGatePassBeat);
  gate.classList.toggle('passed', beat >= pushGatePassBeat && arrived && scene.task >= pushGateX);
  $('thread-owner').textContent = scene.roleIntro ? 'BUILDER’S THREAD · OPUS' : 'BUILDER’S THREAD';
  $('packet-label').textContent = scene.packetLabel || '';
  for (const id of Object.keys(routes)) {
    const branch = $('branch-' + id);
    const active = scene.trip === id;
    branch.setAttribute('visibility', beat >= firstBeat[id] ? 'visible' : 'hidden');
    branch.classList.toggle('current', active);
    branch.classList.toggle('arrived', active && arrived);
    branch.classList.toggle('attention', active && !!(scene.pause || scene.alert));
    $('status-' + id).textContent = active && arrived ? scene.station : '';
    $('role-' + id).textContent = scene.roleIntro && id === 'reader' ? 'Sol · Codex' : routes[id].detail;
    $('trace-' + id).setAttribute('visibility', 'hidden');
  }
  const finding = scene.finding === 'verified' && !arrived ? 'repaired' : scene.finding;
  const showFinding = scene.visual === 'flow' && finding && !(scene.finding === 'open' && scene.back && !arrived);
  $('finding-tag').setAttribute('visibility', showFinding ? 'visible' : 'hidden');
  $('finding-tag').setAttribute('transform', `translate(${scene.task + 204} ${railY})`);
  $('finding-tag').dataset.status = finding || '';
  $('finding-tag-label').textContent = finding ? `F1 · ${finding[0].toUpperCase() + finding.slice(1)}` : '';
  const payload = $('payload');
  payload.getAnimations().forEach(animation => animation.cancel());
  payload.setAttribute('visibility', scene.payload && arrived ? 'visible' : 'hidden');
  payload.classList.toggle('attention', !!scene.alert);
  const reviewReturn = arrived && !!scene.payload && scene.trip === 'review' && scene.back;
  $('route-review').classList.toggle('return-lit', !!reviewReturn);
  if (scene.payload && arrived) {
    payload.setAttribute('transform', reviewReturn ? `translate(${scene.task - 231} 252)` : `translate(${scene.task} 112)`);
    $('payload-route-link').setAttribute('d', reviewReturn ? 'M209 12H216Q231 12 231 -5' : '');
    $('payload-title').textContent = scene.payload[0];
    $('payload-detail').textContent = scene.payload[1];
  }
}

function renderDiagram(scene, beat, instant, fromBeat = lastBeat) {
  const previous = beats[fromBeat];
  const interrupted = !!frame;
  cancelAnimationFrame(frame);
  frame = 0;
  const finish = (animateArrival = false) => {
    placeTask(scene.task);
    paintDiagram(scene, beat, true);
    if (previous?.selfReview && scene.trip === 'human') showSceneCopy(scene);
    if (animateArrival && scene.selfReview) {
      $('self-review-card').animate([{ opacity: 0 }, { opacity: 1 }], { duration: 180 });
    }
    if (animateArrival && scene.payload) {
      $('payload').animate([{ opacity: 0 }, { opacity: 1 }], {
        duration: 160, easing: 'cubic-bezier(0.23, 1, 0.32, 1)'
      });
    }
    const stage = $('simulation').parentElement;
    if (scene.visual === 'flow' && stage.scrollWidth > stage.clientWidth) {
      const task = $('task').getBoundingClientRect();
      const viewport = stage.getBoundingClientRect();
      if (task.left < viewport.left || task.right > viewport.right) {
        stage.scrollLeft += (task.left + task.right - viewport.left - viewport.right) / 2;
      }
    }
  };
  if (instant || reduced.matches || !previous || interrupted || Math.abs(beat - fromBeat) !== 1 || (beat < fromBeat && scene.visual !== 'flow')) {
    finish();
    return;
  }

  const forward = beat > fromBeat;
  const trip = forward ? scene : previous;
  const path = trip.reviewRule ? $('route-review-rule') : trip.selfReview ? $('route-self-review') : trip.trip && $('route-' + trip.trip);
  const trace = !trip.reviewRule && !trip.selfReview && trip.trip && $('trace-' + trip.trip);
  const reviewReturn = forward && scene.returnPacketLabel;
  const selfReviewReturn = forward && previous.selfReview && scene.trip === 'human';
  const closeDuration = selfReviewReturn ? 180 : 0;
  const selfReviewTravel = 1700;
  // ponytail: rework = slide back to the Builder (task 740), H1 out to the Reviewer, clean result back
  const rework = reviewReturn && scene.roundTrip;
  const reworkTask = 740;
  const returnDuration = selfReviewReturn ? closeDuration + selfReviewTravel : rework ? 650 + 1700 : reviewReturn ? 850 : 0;
  const reverse = !!trip.back !== !forward;
  const taskFrom = rework ? reworkTask : previous.task;
  const taskDuration = scene.task === taskFrom ? 0 : 650;
  const roundTrip = forward && scene.roundTrip && !reviewReturn;
  const packetDuration = trip.reviewRule ? 1800 : trip.selfReview ? selfReviewTravel : path ? (roundTrip ? 1700 : 850) : 0;
  const repairHold = forward && scene.repair ? 260 : 0;
  const taskStart = forward ? returnDuration : packetDuration;
  const packetStart = forward ? taskStart + taskDuration + repairHold : 0;
  const duration = Math.max(taskStart + taskDuration, packetStart + packetDuration);

  paintDiagram(forward ? scene : previous, forward ? beat : fromBeat, false);
  $('task-label').textContent = forward && scene.repair ? scene.label : previous.label;
  placeTask(previous.task);
  const packet = $('packet');
  if (reviewReturn) {
    $('branch-review').classList.add('current');
    $('branch-human').classList.remove('current');
    $('status-review').textContent = 'Checking v3';
    if (scene.roundTrip) $('task-label').textContent = 'Change v3';
  }
  if (selfReviewReturn) {
    showSceneCopy(previous);
    $('branch-human').setAttribute('visibility', 'hidden');
    $('branch-human').classList.remove('current');
    $('status-decision').textContent = 'Self-review';
    const card = $('self-review-card');
    card.setAttribute('visibility', 'visible');
    $('simulation').classList.add('self-review-open');
    card.animate([{ opacity: 1 }, { opacity: 0 }], { duration: closeDuration, fill: 'forwards' });
  }
  packet.classList.toggle('attention', !!(trip.pause || trip.alert || trip.reviewRule));
  packet.classList.toggle('rule-chip', !!trip.reviewRule);
  if (!duration) {
    finish();
    return;
  }

  const started = performance.now();
  const progress = (elapsed, offset, span) => Math.max(0, Math.min(1, (elapsed - offset) / span));
  const ease = value => value * value * (3 - 2 * value);
  const returnPath = reviewReturn ? $('route-review') : selfReviewReturn ? $('route-self-review') : null;
  const returnTrace = reviewReturn ? $('trace-review') : null;
  const length = path?.getTotalLength();
  const returnLength = returnPath?.getTotalLength();
  let returning = !!returnPath;
  function drawPacket(path, trace, length, progress, reverse, label, reviewResult) {
    const point = path.getPointAtLength(length * (reverse ? 1 - progress : progress));
    packet.setAttribute('transform', `translate(${point.x} ${point.y})`);
    packet.setAttribute('visibility', progress < 1 ? 'visible' : 'hidden');
    const packetLabel = $('packet-label');
    packetLabel.textContent = label;
    packetLabel.setAttribute('text-anchor', reviewResult ? 'end' : 'middle');
    packetLabel.setAttribute('x', reviewResult ? -18 : 0);
    const labelY = reviewResult ? Math.max(6, railY + 35 - point.y) : trip.reviewRule ? 5 : -18;
    packetLabel.setAttribute('y', labelY);
    const packetLink = $('packet-route-link');
    packetLink.style.display = reviewResult ? '' : 'none';
    packetLink.setAttribute('y1', labelY - 5);
    $('route-review').classList.toggle('return-lit', !!reviewResult && progress < 1);
    lightSelfReview(path.id === 'route-self-review' && progress < 1);
    if (trace) {
      trace.setAttribute('visibility', progress < 1 ? 'visible' : 'hidden');
      trace.style.strokeDashoffset = (reverse ? -1 : 1) * (1 - progress);
    }
  }
  function tickFrame(now) {
    const elapsed = now - started;
    if (elapsed >= duration) {
      frame = 0;
      finish(forward);
      return;
    }
    if (returning && elapsed < returnDuration) {
      if (elapsed < closeDuration) {
        frame = requestAnimationFrame(tickFrame);
        return;
      }
      $('self-review-card').setAttribute('visibility', 'hidden');
      $('simulation').classList.remove('self-review-open');
      const outbound = rework && elapsed < 650 + 850;
      const legStart = rework ? 650 + 850 : closeDuration;
      if (rework && elapsed < 650) {
        placeTask(previous.task + (reworkTask - previous.task) * ease(progress(elapsed, 0, 650)));
        packet.setAttribute('visibility', 'hidden');
      } else if (outbound) drawPacket(returnPath, returnTrace, returnLength, ease(progress(elapsed, 650, 850)), false, scene.roundTrip, false);
      else drawPacket(returnPath, returnTrace, returnLength, ease(progress(elapsed, legStart, returnDuration - legStart)), true, reviewReturn || 'Read · v2', !!reviewReturn);
    } else if (returning) {
      returning = false;
      lightSelfReview(false);
      returnPath.classList.remove('return-lit');
      returnTrace?.setAttribute('visibility', 'hidden');
      $('branch-review').classList.remove('current');
      $('branch-human').classList.add('current');
      $('status-review').textContent = '';
      $('status-decision').textContent = '';
      packet.setAttribute('visibility', 'hidden');
      if (reviewReturn) $('task-label').textContent = 'Checked v3';
      if (selfReviewReturn) {
        $('packet-label').textContent = '';
        $('branch-human').setAttribute('visibility', 'visible');
        showSceneCopy(scene);
      }
    }
    if (taskDuration && !(rework && elapsed < taskStart)) {
      const p = ease(progress(elapsed, taskStart, taskDuration));
      placeTask(taskFrom + (scene.task - taskFrom) * p);
      if (forward && p === 1 && !reviewReturn && !roundTrip) $('task-label').textContent = scene.label;
    }
    if (path && roundTrip && elapsed >= packetStart) {
      const outbound = elapsed < packetStart + 850;
      if (!outbound) $('task-label').textContent = scene.label;
      drawPacket(path, trace, length, ease(progress(elapsed, outbound ? packetStart : packetStart + 850, 850)), !outbound, outbound ? scene.roundTrip : trip.packetLabel, !outbound && trip.trip === 'review');
    } else if (path && elapsed >= packetStart) {
      drawPacket(path, trace, length, ease(progress(elapsed, packetStart, packetDuration)), reverse, trip.packetLabel || '', trip.trip === 'review' && trip.back);
    }
    frame = requestAnimationFrame(tickFrame);
  }
  frame = requestAnimationFrame(tickFrame);
}

function renderSurface(scene, beat, instant) {
  const svg = $('simulation');
  const stage = svg.parentElement;
  const visual = $('scene-visual');
  const fromBeat = lastBeat;
  const previous = beats[fromBeat];
  const flow = scene.visual === 'flow';
  const wasFlow = previousVisual === 'flow';
  const interrupted = !!surfaceFrame;
  const changed = scene.visual !== previousVisual;
  const decorations = [...stage.querySelectorAll('.branch, #payload, #packet, #finding-tag, #review-rule-tag')];
  const before = {
    top: parseFloat(svg.style.top) || 0,
    height: svg.getBoundingClientRect().height,
    y: svg.viewBox.baseVal.y,
    viewHeight: svg.viewBox.baseVal.height,
    opacity: Number(decorations[0].style.opacity || 1)
  };
  const target = {
    top: flow ? 0 : Math.max(0, stage.clientHeight - 86),
    height: flow ? stage.clientHeight : 86,
    y: flow ? 0 : 144,
    viewHeight: flow ? 400 : 112,
    opacity: flow ? 1 : 0
  };

  cancelAnimationFrame(surfaceFrame);
  surfaceFrame = 0;
  if (changed || instant) visual.getAnimations().forEach(animation => animation.cancel());
  document.body.classList.toggle('detail-scene', !flow);
  visual.setAttribute('aria-hidden', String(flow));
  if (changed && !flow) {
    visual.innerHTML = visuals[scene.visual] || '';
    stage.scrollLeft = 0;
  }
  previousVisual = scene.visual;

  function position(values) {
    svg.style.top = values.top + 'px';
    svg.style.height = values.height + 'px';
    svg.setAttribute('viewBox', `0 ${values.y} 1120 ${values.viewHeight}`);
    decorations.forEach(element => { element.style.opacity = values.opacity; });
  }
  function finish(snapDiagram) {
    position(target);
    if (flow) visual.innerHTML = '';
    renderDiagram(scene, beat, snapDiagram, fromBeat);
  }

  const morph = previous && !instant && !reduced.matches && (flow !== wasFlow || interrupted);
  if (!morph) {
    if (changed && !flow && previous && !instant && !reduced.matches) {
      visual.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 220 });
    }
    finish(instant || interrupted);
    return;
  }

  cancelAnimationFrame(frame);
  frame = 0;
  placeTask(previous.task);
  paintDiagram(previous, fromBeat, true);
  visual.animate(
    flow ? [{ opacity: 1 }, { opacity: 0 }] : [{ opacity: 0 }, { opacity: 1 }],
    { duration: flow ? 180 : 320, delay: flow ? 0 : 120, fill: 'both', easing: 'cubic-bezier(0.23, 1, 0.32, 1)' }
  );
  const started = performance.now();
  function tickSurface(now) {
    const progress = Math.min(1, (now - started) / 460);
    const eased = progress * progress * (3 - 2 * progress);
    const values = {};
    for (const key of Object.keys(target)) values[key] = before[key] + (target[key] - before[key]) * eased;
    const fade = flow ? Math.max(0, (progress - .45) / .55) : Math.min(1, progress / .4);
    values.opacity = before.opacity + (target.opacity - before.opacity) * fade;
    position(values);
    if (progress === 1) {
      surfaceFrame = 0;
      finish(interrupted);
      return;
    }
    surfaceFrame = requestAnimationFrame(tickSurface);
  }
  surfaceFrame = requestAnimationFrame(tickSurface);
}

function renderOpening(scene, instant) {
  const opening = $('opening-stage');
  if (!opening) return;
  opening.getAnimations({ subtree: true }).forEach(animation => animation.cancel());
  if (scene.visual !== 'cover') return;
  opening.dataset.issue = scene.issue;
  const activeIssue = scene.issue === 'ready' ? 'usage' : scene.issue;
  opening.querySelectorAll('[data-issue-label]').forEach(element => {
    element.classList.toggle('active', element.dataset.issueLabel === activeIssue);
  });
  opening.querySelectorAll('[data-issue-panel]').forEach(element => {
    element.hidden = element.dataset.issuePanel !== activeIssue;
  });
  const staticOpening = reduced.matches || (instant && lastBeat >= 0);
  opening.classList.toggle('static-opening', staticOpening);
  let plan;
  if (scene.issue === 'decision') {
    const viewport = opening.querySelector('.scope-viewport');
    const messages = opening.querySelector('.scope-messages');
    const choice = opening.querySelector('.scope-choice');
    const width = viewport.clientWidth, height = viewport.clientHeight;
    const section = choice.closest('.scope-message');
    const x = section.offsetLeft + section.offsetWidth / 2;
    const y = section.offsetTop + section.offsetHeight / 2;
    const zoom = Math.min(1.35, (width - 40) / section.offsetWidth, (height - 32) / section.offsetHeight);
    plan = {
      start: `translate(${width * .17}px, 12px) scale(.66)`,
      scan: `translate(${width * .17}px, ${height * .68 - y * .66}px) scale(.66)`,
      focus: `translate(${width / 2 - x * zoom}px, ${height / 2 - y * zoom}px) scale(${zoom})`,
      thumb: Math.min(height - 18, y / messages.scrollHeight * height)
    };
    messages.style.transform = plan.focus;
    opening.querySelector('.plan-scrollbar i').style.transform = `translateY(${plan.thumb}px)`;
  }
  if (scene.issue === 'ready' || staticOpening) return;
  const animate = (selector, frames, options = {}) => opening.querySelector(selector).animate(
    frames, { duration: 4400, fill: 'both', easing: 'linear', ...options }
  );

  if (scene.issue === 'usage') {
    const duration = 8000;
    const path = opening.querySelector('#usage-switch');
    const frames = Array.from({length: 41}, (_, i) => {
      const point = path.getPointAtLength(path.getTotalLength() * i / 40);
      return {transform: `translate(${point.x}px, ${point.y}px)`};
    });
    animate('.usage-stack', [{opacity:0, transform:'translateX(-28px)'},{opacity:1, transform:'translateX(0)'}], {duration:1600});
    animate('.usage-limit', [{opacity:0},{opacity:1}], {duration:250,delay:1800});
    animate('.usage-packet', frames, {duration:1600,delay:2400,easing:'cubic-bezier(0.77, 0, 0.175, 1)'});
    animate('.usage-before', [{opacity:1,offset:0},{opacity:1,offset:.58},{opacity:0,offset:.65},{opacity:0}], {duration});
    animate('.usage-after', [{opacity:0,offset:0},{opacity:0,offset:.65},{opacity:1,offset:.75},{opacity:1}], {duration});
    animate('.usage-outcome', [{opacity:0,offset:0},{opacity:0,offset:.75},{opacity:1,offset:.85},{opacity:1}], {duration});
  } else if (scene.issue === 'rules') {
    const timing = { duration: 7000, easing: 'cubic-bezier(0.23, 1, 0.32, 1)' };
    animate('.medium-row .effort-fill', [{ transform: 'scaleX(0)', offset: 0 }, { transform: 'scaleX(0)', offset: .05 }, { transform: 'scaleX(.88)', offset: .38 }, { transform: 'scaleX(.88)' }], timing);
    animate('.max-row', [{ opacity: 0, offset: 0 }, { opacity: 0, offset: .42 }, { opacity: 1, offset: .5 }, { opacity: 1 }], timing);
    animate('.subagent-chip', [{ opacity: 0, transform: 'translateY(-8px)', offset: 0 }, { opacity: 0, transform: 'translateY(-8px)', offset: .52 }, { opacity: 1, transform: 'translateY(0)', offset: .6 }, { opacity: 1, transform: 'translateY(0)' }], timing);
    animate('.max-row .effort-fill', [{ transform: 'scaleX(0)', offset: 0 }, { transform: 'scaleX(0)', offset: .55 }, { transform: 'scaleX(.24)', offset: .75 }, { transform: 'scaleX(.24)' }], timing);
    animate('.effort-outcome', [{ opacity: 0, offset: 0 }, { opacity: 0, offset: .82 }, { opacity: 1, offset: .9 }, { opacity: 1 }], timing);
  } else if (scene.issue === 'decision') {
    const timing = { duration: 9000 };
    animate('.scope-messages', [
      { transform: plan.start, offset: 0 },
      { transform: plan.start, offset: .14 },
      { transform: plan.scan, offset: .52 },
      { transform: plan.scan, offset: .59, easing: 'cubic-bezier(0.77, 0, 0.175, 1)' },
      { transform: plan.focus, offset: .76 },
      { transform: plan.focus, offset: 1 }
    ], timing);
    animate('.plan-scrollbar i', [{ transform: 'translateY(0)', offset: 0 }, { transform: 'translateY(0)', offset: .14 }, { transform: `translateY(${plan.thumb}px)`, offset: .52 }, { transform: `translateY(${plan.thumb}px)`, offset: 1 }], timing);
    animate('.scope-choice', [{ backgroundColor: 'transparent', color: '#aebdb5', offset: 0 }, { backgroundColor: 'transparent', color: '#aebdb5', offset: .76 }, { backgroundColor: '#3a2e1f', color: '#f3bf7a', offset: .83 }, { backgroundColor: '#3a2e1f', color: '#f3bf7a' }], timing);
    animate('.scope-outcome', [{ opacity: 0, offset: 0 }, { opacity: 0, offset: .84 }, { opacity: 1, offset: .92 }, { opacity: 1 }], timing);
  } else if (scene.issue === 'review') {
    const loop = { duration: 7600, iterations: Infinity };
    animate('.courier', [
      { transform: 'translate(140px, 122px)', offset: 0 },
      { transform: 'translate(140px, 122px)', offset: .1 },
      { transform: 'translate(420px, 122px)', offset: .4 },
      { transform: 'translate(420px, 122px)', offset: .55 },
      { transform: 'translate(140px, 122px)', offset: .85 },
      { transform: 'translate(140px, 122px)', offset: 1 }
    ], loop);
    animate('.cargo-code', [{ opacity: 1, offset: 0 }, { opacity: 1, offset: .5 }, { opacity: 0, offset: .55 }, { opacity: 0, offset: .96 }, { opacity: 1, offset: 1 }], loop);
    animate('.cargo-finding', [{ opacity: 0, offset: 0 }, { opacity: 0, offset: .5 }, { opacity: 1, offset: .55 }, { opacity: 1, offset: .96 }, { opacity: 0, offset: 1 }], loop);
    animate('.reviewer-work', [{ opacity: .2, offset: 0 }, { opacity: .2, offset: .39 }, { opacity: 1, offset: .4 }, { opacity: 1, offset: .55 }, { opacity: .2, offset: .56 }, { opacity: .2 }], loop);
    animate('.builder-work', [{ opacity: .2, offset: 0 }, { opacity: .2, offset: .84 }, { opacity: 1, offset: .85 }, { opacity: 1, offset: .99 }, { opacity: .2, offset: 1 }], loop);
  }
}

function renderHandoff(active, animate, fadeDock, delay) {
  const dock = $('handoff-dock');
  const lamp = $('branch-reader').querySelector('.station-lamp');
  dock.getAnimations({ subtree: true }).forEach(animation => animation.cancel());
  lamp.getAnimations().forEach(animation => animation.cancel());
  dock.setAttribute('visibility', active || fadeDock ? 'visible' : 'hidden');
  if (fadeDock) dock.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 220, fill: 'forwards' });
  if (!active || !animate) return;

  $('handoff-map-chip').animate([{ opacity: 1 }, { opacity: .45 }, { opacity: 1 }], { delay, duration: 600 });
  $('handoff-source-path').animate([
    { opacity: 1, strokeDashoffset: 1, offset: 0 },
    { opacity: 1, strokeDashoffset: 0, offset: .36 },
    { opacity: 1, strokeDashoffset: 0, offset: .82 },
    { opacity: 0, strokeDashoffset: 0 }
  ], { delay: delay + 320, duration: 2040 });
  $('handoff-source').animate([{ opacity: 0 }, { opacity: 1, offset: .18 }, { opacity: 1, offset: .78 }, { opacity: 0 }],
    { delay: delay + 1060, duration: 1300 });

  const route = $('route-reader');
  const railLength = 250;
  const length = route.getTotalLength() + railLength;
  const routeFrames = Array.from({ length: 81 }, (_, i) => {
    const distance = length * i / 80;
    const point = distance <= railLength ? { x: 480 - distance, y: railY } : route.getPointAtLength(distance - railLength);
    return { transform: `translate(${point.x}px, ${point.y}px)`, opacity: 1 };
  });
  const outbound = routeFrames.map((frame, i) => ({ ...frame, offset: i / 80 * (1080 / 1460) }));
  outbound.push({ ...routeFrames.at(-1), offset: 1 });
  $('handoff-question').animate(outbound, { delay: delay + 2540, duration: 1460 });
  lamp.animate([{ fill: 'var(--mint)' }, { fill: 'var(--mint)' }], { delay: delay + 3550, duration: 460 });
  const returning = routeFrames.slice().reverse();
  returning[returning.length - 1] = { ...returning.at(-1), opacity: 0 };
  $('handoff-answer').animate(returning, { delay: delay + 4000, duration: 1190, easing: 'ease-in-out' });
}

function renderProcess(scene, animate) {
  document.querySelectorAll('.process-diagram, #task-thinking').forEach(group => {
    group.getAnimations({ subtree: true }).forEach(animation => animation.cancel());
  });
  const handoff = scene.process === 'handoff';
  const inputs = scene.process === 'inputs';
  const reasoning = scene.process === 'reasoning';
  for (const [id, shown] of [['flow-inputs', inputs], ['flow-handoff', handoff], ['flow-reasoning', reasoning], ['task-thinking', reasoning && !scene.trip]]) {
    $(id).setAttribute('visibility', shown ? 'visible' : 'hidden');
    $(id).setAttribute('aria-hidden', String(!shown));
  }
  $('reasoning-spec').setAttribute('visibility', reasoning && !scene.trip ? 'visible' : 'hidden');
  $('flow-reasoning').querySelectorAll('[data-level]').forEach(row => {
    const shown = reasoning && Number(row.dataset.level) <= scene.reveal;
    row.classList.toggle('unrevealed', !shown);
    row.classList.toggle('active-line', shown && Number(row.dataset.level) === scene.reveal);
    row.setAttribute('aria-hidden', String(!shown));
  });
  const previous = beats[lastBeat];
  const delay = (previous?.visual !== 'flow' ? 460 : 0) + (previous?.task !== scene.task ? 650 : 0);
  const motion = animate && !reduced.matches;
  renderHandoff(handoff, motion, motion && reasoning && previous?.process === 'handoff', delay);
  const diagram = inputs ? $('flow-inputs') : reasoning ? $('flow-reasoning') : null;
  if (!diagram || !motion || scene.trip) return;
  const timing = { duration: 1500, delay, fill: 'both' };
  const packets = inputs
    ? [...diagram.querySelectorAll('.process-packet')]
    : [...diagram.querySelectorAll(`[data-level="${scene.reveal}"] .process-packet`)];
  // ponytail: chain plays each reasoning row in turn within one step
  const levels = reasoning && scene.chain ? [...Array(scene.reveal + 1).keys()] : [scene.reveal];
  const step = 1700;
  if (reasoning && scene.chain) levels.slice(1).forEach(level => {
    diagram.querySelector(`[data-level="${level}"]`).animate([{ opacity: 0 }, { opacity: 1 }], { duration: 300, delay: delay + level * step, fill: 'backwards' });
  });
  if (reasoning && scene.chain) packets.splice(0, packets.length, ...levels.map(level => diagram.querySelector(`[data-level="${level}"] .process-packet`)));
  packets.forEach((packet, i) => {
    const path = $(packet.dataset.route);
    const length = path.getTotalLength();
    const frames = Array.from({ length: 41 }, (_, n) => {
      const point = path.getPointAtLength(length * n / 40);
      return { transform: `translate(${point.x}px, ${point.y}px)`, opacity: n === 40 ? 0 : 1 };
    });
    packet.animate(frames, { duration: 900, delay: delay + (scene.chain ? i * step : i * 220), fill: 'both', easing: 'ease-in-out' });
  });
  if (scene.process === 'reasoning') {
    levels.forEach((level, n) => {
      const row = diagram.querySelector(`[data-level="${level}"]`);
      const t = { ...timing, delay: delay + n * step };
      row.querySelector('.reasoning-result').animate([{ opacity: 0, offset: 0 }, { opacity: 0, offset: .75 }, { opacity: 1 }], t);
      row.querySelector('.reasoning-checking').animate([{ opacity: 1 }, { opacity: 1, offset: .65 }, { opacity: 0, offset: .75 }, { opacity: 0 }], t);
      $('task-thinking').querySelectorAll('circle').forEach((dot, i) => {
        dot.animate([{ opacity: .25 }, { opacity: 1 }, { opacity: .25 }], { duration: 500, delay: t.delay + i * 100, iterations: 2 });
      });
    });
  }
}

function renderPayoff(scene, animate) {
  document.body.classList.toggle('payoff', scene.visual === 'payoff');
  const rows = [...document.querySelectorAll('.payoff-row')];
  if (scene.visual !== 'payoff' || !animate || reduced.matches) return;
  // ponytail: one staggered timeline per row; the end state is the static CSS, so skipping it is safe
  const fill = 'backwards', easing = 'cubic-bezier(0.23, 1, 0.32, 1)';
  rows.forEach((row, i) => {
    const t = 500 + i * 1100;
    const q = selector => row.querySelector(selector);
    q('.payoff-want p').animate([{ color: '#788b80' }, { color: '#788b80', offset: .5 }, { color: 'var(--fg)' }], { duration: 700, delay: t, fill });
    q('.payoff-before').animate([{ opacity: 0, transform: 'translateY(-4px)' }, { opacity: 1, transform: 'none' }], { duration: 300, delay: t - 300, fill, easing });
    q('.payoff-before').animate([{ backgroundSize: '0% 1px', color: 'var(--muted)' }, { backgroundSize: '100% 1px', color: '#5f6e66' }], { duration: 380, delay: t + 150, fill, easing: 'ease-in-out' });
    q('.payoff-num').animate([{ opacity: 1 }, { opacity: 0 }], { duration: 160, delay: t + 420, fill });
    q('.payoff-check').animate([{ opacity: 0, transform: 'scale(.4)' }, { opacity: 1, transform: 'scale(1.15)', offset: .7 }, { opacity: 1, transform: 'scale(1)' }], { duration: 360, delay: t + 480, fill, easing });
    q('.payoff-check path').animate([{ strokeDashoffset: 20 }, { strokeDashoffset: 0 }], { duration: 260, delay: t + 600, fill, easing: 'ease-out' });
    q('.payoff-link').animate([{ transform: 'scaleX(0)' }, { transform: 'scaleX(1)' }], { duration: 420, delay: t + 380, fill, easing: 'ease-in-out' });
    q('.payoff-link i').animate([{ left: '0%', opacity: 1 }, { left: '100%', opacity: 1, offset: .85 }, { left: '100%', opacity: 0 }], { duration: 520, delay: t + 380, fill: 'both', easing: 'ease-in-out' });
    q('.payoff-tile').animate([{ opacity: 0, transform: 'translateX(-14px)' }, { opacity: 1, transform: 'none' }], { duration: 420, delay: t + 720, fill, easing });
    q('.payoff-tile').animate([{ borderColor: 'var(--mint)', boxShadow: '0 0 0 4px #a3f3cc22' }, { borderColor: 'var(--line)', boxShadow: '0 0 0 0 #a3f3cc00' }], { duration: 900, delay: t + 900, fill, easing: 'ease-out' });
  });
}

function showSceneCopy(scene) {
  $('talk-title').textContent = scene.title;
  $('caption').textContent = scene.caption;
  const closingLine = $('closing-line');
  closingLine.textContent = scene.closingLine || '';
  closingLine.hidden = !scene.closingLine;
  $('note').textContent = scene.notes;
  $('next-cue').textContent = scene.cue;
  $('announcement').textContent = [scene.title, scene.caption, ...(scene.payload ?? []), ...(scene.closingLine ? [scene.closingLine] : [])].join('. ');
}

function render(sync = true, instant = false) {
  const beat = beats.findIndex(s => s.index === index && s.step === step);
  const scene = beats[beat];
  const act = deck[index];
  $('act-number').textContent = String(index).padStart(2, '0'); // ponytail: title slide is section 0 and its header is hidden
  $('act-name').textContent = act.name;
  showSceneCopy(scene);
  const reference = $('note-source');
  reference.textContent = scene.source?.title || '';
  if (scene.source) reference.href = scene.source.url;
  else reference.removeAttribute('href');
  $('note-reference').hidden = !scene.source;
  $('source-scope').textContent = scene.source?.scope || '';
  document.body.classList.toggle('opening', scene.visual === 'cover');
  document.body.classList.toggle('bookend-slide', scene.visual === 'title' || scene.visual === 'end');
  if (beat !== lastBeat || instant) {
    decisionFlight?.();
    let from;
    const previous = beats[lastBeat];
    if (!instant && !reduced.matches && !frame && !surfaceFrame && beat === lastBeat + 1 &&
        ((scene.visual === 'record' && previous?.trip === 'decision' && previous.back) ||
         (scene.visual === 'intake' && previous?.visual === 'record'))) {
      const source = previous.visual === 'record' ? document.querySelector('.decision-key') : $('payload-title');
      const rect = source?.getBoundingClientRect();
      if (rect?.width) from = { x: previous.visual === 'record' ? rect.left + rect.width / 2 : rect.left + 15, y: rect.top + rect.height / 2 };
    }
    renderSurface(scene, beat, instant);
    renderOpening(scene, instant);
    renderPayoff(scene, !instant);
    transferDecision(from);
  }
  $('scene-visual').querySelectorAll('[data-level]').forEach(element => {
    const level = Number(element.dataset.level);
    element.classList.toggle('unrevealed', level > (scene.reveal ?? 0));
    element.classList.toggle('active-line', level === (scene.reveal ?? 0));
    element.setAttribute('aria-hidden', String(level > (scene.reveal ?? 0)));
  });
  if (beat !== lastBeat || instant) renderProcess(scene, !instant && beat === lastBeat + 1);

  $('count').textContent = `${index + 1} / ${deck.length}`;
  $('step-count').textContent = `${beat + 1} / ${total}`;
  if (beat !== lastBeat) $('notes').scrollTop = 0;
  $('timing').textContent = `${act.name} · ${act.minutes}`;
  $('next').disabled = beat === total - 1;
  $('previous').disabled = beat === 0;
  if ((scene.pause || scene.selfReview || scene.issue === 'review') && playing) stopPlayback();
  $('play').textContent = playing ? 'Pause' : 'Play';
  $('play').setAttribute('aria-pressed', String(playing));
  const hash = `#slide-${index + 1}/step-${step}`;
  if (location.hash !== hash) history.replaceState(null, '', hash);
  lastBeat = beat;
  if (sync) sendState();
}
function stopPlayback(){clearTimeout(playTimer);playing=false;if($('play')){$('play').textContent='Play';$('play').setAttribute('aria-pressed','false');}}
function move(direction){stopPlayback();const b=beats.findIndex(s=>s.index===index&&s.step===step);const s=beats[Math.max(0,Math.min(total-1,b+direction))];index=s.index;step=s.step;render();}
function resetPresentation(){stopPlayback();index=0;step=0;start=Date.now();$('notes').scrollTop=0;render(true,true);tick();$('next').focus({preventScroll:true});}
function schedule(){clearTimeout(playTimer);playTimer=setTimeout(()=>{const b=beats.findIndex(s=>s.index===index&&s.step===step);if(beats[b].pause||beats[b].selfReview||beats[b].issue==='review'||b===total-1){stopPlayback();return;}const s=beats[b+1];index=s.index;step=s.step;render();if(playing)schedule();},beats.find(s=>s.index===index&&s.step===step).dwell||4200);}
function togglePlay(){if(playing){stopPlayback();render();return;}const s=deck[index].states[step];if(s.pause||s.selfReview||s.issue==='review')return;playing=true;render();schedule();}
function readHash(){stopPlayback();const m=location.hash.match(/^#slide-(\d+)(?:\/step-(\d+))?$/);index=Math.max(0,Math.min(deck.length-1,Number(m?.[1]||1)-1));step=Math.max(0,Math.min(deck[index].states.length-1,Number(m?.[2]||0)));render(true,true);}
function toggleNotes(){if(isPresenter||audienceMode)return;const open=$('notes').classList.toggle('open');$('notes').inert=!open;$('notes-toggle').setAttribute('aria-expanded',String(open));if(open){notesFocus=document.activeElement;$('close-notes').focus();}else notesFocus?.focus();}
async function toggleFullscreen(){try{if(document.fullscreenElement)await document.exitFullscreen();else if(document.documentElement.requestFullscreen)await document.documentElement.requestFullscreen();else $('announcement').textContent='Fullscreen is unavailable in this browser.';}catch{$('announcement').textContent='Try the Fullscreen button in a browser tab.';}}
function tick(){const seconds=Math.floor((Date.now()-start)/1000),value=`${Math.floor(seconds/60)}:${String(seconds%60).padStart(2,'0')}`;$('timer').textContent=value;$('elapsed').textContent=value;}
function sendState(){channel?.postMessage({type:'state',index,step,start});}
function setAudience(active){audienceMode=active;document.body.classList.toggle('audience',active);$('notes').classList.remove('open');$('notes').inert=true;$('notes-toggle').setAttribute('aria-expanded','false');const url=new URL(location.href);if(active)url.searchParams.set('view','audience');else url.searchParams.delete('view');history.replaceState(null,'',url);}
function connect(session){
  if(!/^(?:[a-f0-9-]{36}|[a-f0-9]{32})$/.test(session||''))return;
  channel?.close();channel=new BroadcastChannel(`two-ai-agents-${session}`);
  channel.onmessage=({data})=>{
    if(!data||typeof data!=='object')return;
    if(data.type==='ready'&&data.presenter===!isPresenter){if(!isPresenter)setAudience(true);$('connection').textContent='Connected to audience';sendState();}
    else if(data.type==='state'){
      if(!Number.isInteger(data.index)||data.index<0||data.index>=deck.length||!Number.isInteger(data.step)||data.step<0||data.step>=deck[data.index].states.length||!Number.isFinite(data.start)||data.start<=0||data.start>Date.now())return;
      const reset=data.start!==start;
      stopPlayback();index=data.index;step=data.step;start=data.start;if(reset)$('notes').scrollTop=0;render(false,reset);tick();if(isPresenter)$('connection').textContent='Connected to audience';
    }else if(data.type==='presenter-closed'&&!isPresenter)setAudience(false);
    else if(data.type==='audience-closed'&&isPresenter)$('connection').textContent='Audience disconnected. Reopen the presentation and choose Presenter view.';
  };
  channel.postMessage({type:'ready',presenter:isPresenter});
}
function openPresenter(){
  if(isPresenter){if(window.opener&&!window.opener.closed)window.opener.focus();else $('connection').textContent='Open the presentation normally and choose Presenter view.';return;}
  if(presenterWindow&&!presenterWindow.closed){presenterWindow.focus();return;}
  if(!('BroadcastChannel'in window)){$('message').textContent='Presenter view needs a current browser with synchronized-window support.';return;}
  const session = crypto.randomUUID?.() ?? Array.from(crypto.getRandomValues(new Uint8Array(16)), byte => byte.toString(16).padStart(2, '0')).join('');
  const url=new URL(location.href);url.searchParams.set('session',session);url.searchParams.set('view','presenter');
  presenterWindow=window.open(url,`presenter-${session}`,'popup,width=1440,height=900');
  if(!presenterWindow){$('message').textContent='Allow popups for this site to open the separate presenter window.';return;}
  $('message').textContent='';const audienceURL=new URL(location.href);audienceURL.searchParams.set('session',session);history.replaceState(null,'',audienceURL);connect(session);setAudience(true);
}

$('previous').addEventListener('click',()=>move(-1));$('next').addEventListener('click',()=>move(1));$('play').addEventListener('click',togglePlay);
$('reset').addEventListener('click',resetPresentation);
$('notes-toggle').addEventListener('click',toggleNotes);$('close-notes').addEventListener('click',toggleNotes);$('presenter-toggle').addEventListener('click',openPresenter);$('fullscreen').addEventListener('click',toggleFullscreen);
document.addEventListener('fullscreenchange',()=>{$('fullscreen').textContent=document.fullscreenElement?'Exit fullscreen':'Fullscreen';$('fullscreen').setAttribute('aria-pressed',String(!!document.fullscreenElement));});
document.addEventListener('keydown',event=>{
 if(event.altKey||event.ctrlKey||event.metaKey||event.target.closest('input,textarea,select,[contenteditable="true"]'))return;
 if(event.key===' '&&event.target.closest('button,a'))return;
 if(['ArrowRight','ArrowDown','PageDown',' ','ArrowLeft','ArrowUp','PageUp'].includes(event.key)){event.preventDefault();if(!event.repeat)move(['ArrowRight','ArrowDown','PageDown',' '].includes(event.key)?1:-1);}
 else if(!event.repeat&&['Home','End'].includes(event.key)){event.preventDefault();stopPlayback();index=event.key==='Home'?0:deck.length-1;step=0;render();}
 else if(!event.repeat&&event.key.toLowerCase()==='p')togglePlay();
 else if(!event.repeat&&event.key.toLowerCase()==='n')toggleNotes();
 else if(!event.repeat&&event.key.toLowerCase()==='f')toggleFullscreen();
 else if(event.key==='Escape'&&!isPresenter&&$('notes').classList.contains('open'))toggleNotes();
});
window.addEventListener('hashchange',readHash);window.addEventListener('pagehide',()=>channel?.postMessage({type:isPresenter?'presenter-closed':'audience-closed'}));
reduced.addEventListener('change',()=>{render(false,true);});
document.body.classList.toggle('presenter',isPresenter);document.body.classList.toggle('audience',audienceMode);
if(isPresenter){document.title='Presenter · Building Agent Workflows for Better Code';$('notes').classList.add('open');$('notes').inert=false;$('presenter-toggle').textContent='Show audience';}
tick();setInterval(tick,1000);readHash();if('BroadcastChannel'in window)connect(params.get('session'));

let stageSize;
new ResizeObserver(([entry]) => {
  const { width, height } = entry.contentRect;
  if (stageSize && (Math.abs(width - stageSize.width) > .5 || Math.abs(height - stageSize.height) > .5)) {
    render(false, true);
  }
  stageSize = { width, height };
}).observe($('simulation').parentElement);
