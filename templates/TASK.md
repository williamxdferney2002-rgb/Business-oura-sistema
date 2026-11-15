# TASK-XXX · <short title>

<!--
Architect's template. Copy to tasks/active/TASK-XXX-<slug>.md.
One file per task. Each agent APPENDS its section at the end (never rewrites earlier ones);
the only parts edited in place are the STATUS line and the CURRENT SPECIFICATION section.
The architect fills in APPROVAL before handing over the task.
CURRENT SPECIFICATION: with the first approved SPEC_AMENDMENT, the architect adds below STATUS
a "## CURRENT SPECIFICATION" section that consolidates the specification and all amendments, and
updates it in the same commit as each new amendment. It starts with: "For operational work, read this
section. The history below is not required reading unless explicitly referenced." It is the
operational source for executor and auditor; everything below stays as history.
This file's STATUS is the only source of the task's state (CURRENT_STATE.md only says which one is active).

| STATUS          | Set by     | Next to act         | What happens                                                |
|-----------------|------------|---------------------|-------------------------------------------------------------|
| DRAFT           | architect  | owner               | Reviews the spec; on approval the architect fills APPROVAL and sets SPEC_READY |
| SPEC_READY      | architect  | executor            | Implements (requires APPROVAL)                              |
| IN_PROGRESS     | executor   | executor            | Working                                                     |
| AWAITING_AUDIT  | executor   | auditor             | Audits the COMMIT of the latest report                      |
| REJECTED        | auditor    | architect → executor | Architect triages findings; executor fixes → CORRECTION_REPORT |
| APPROVED        | auditor    | architect           | No human tests: FINAL_STATUS. With human tests: AWAITING_HUMAN |
| AWAITING_HUMAN  | architect  | owner               | Runs HUMAN_TESTS, reports PASSED/FAILED + authorizes closure |
| BLOCKED         | anyone     | architect           | Responds with SPEC_AMENDMENT (and the owner if scope changes) |
| DONE            | architect  | —                   | Closed. Requires APPROVED and, if there are HUMAN_TESTS, PASSED + owner authorization |

BLOCKED is set by: the executor (ARCHITECTURE_CONFLICT, PARTIAL/BLOCKED report, or a DISPUTED finding);
the auditor (third rejection, or the problem is in the spec: ESCALATE_TO_ARCHITECT in its AUDIT_REPORT).
The SPEC_AMENDMENT states in NEXT_STATUS how it continues: SPEC_READY, REJECTED or AWAITING_AUDIT.
If a HUMAN_TEST fails, the architect adds a SPEC_AMENDMENT with the fix and NEXT_STATUS: REJECTED.
Each stage ends with the compact HANDOFF (agents/templates/HANDOFF.md): who is next, what to read, what to do.
-->


STATUS: SPEC_READY

## TASK SPECIFICATION
```
TASK_ID: TASK-XXX
OBJECTIVE: <one or two sentences: what works when this is done>
SOURCE_PLAN_SECTION: <plan §x · Phase n · R## · D##>
APPROVAL: <owner, "go ahead", YYYY-MM-DD>   ← without this the executor does not start
BASE_COMMIT: <short hash of HEAD when specifying>
AUDIT_LEVEL: <QUICK | STANDARD | DEEP> — <why>
CURRENT_STATE: <what exists today in the code and in production, with paths; what fails or is missing>
SCOPE:
  - <what is included, concretely>
OUT_OF_SCOPE:
  - <what is NOT touched even if it looks related>
FILES_TO_INSPECT:
  - <path> — <why>
FILES_EXPECTED_TO_CHANGE:
  - <path> — <what changes>
DEPENDENCIES:
  - <previous tasks, owner data or actions, services>
IMPLEMENTATION_STEPS:
  1. <verifiable step: file, function, behavior>
  2. …
CONSTRAINTS:
  - <api_* contracts / columns / workflow IDs that do not change; speed; style; security>
ACCEPTANCE_CRITERIA:
  AC1. <checkable by the auditor without asking anyone>
  AC2. …
REQUIRED_TESTS:            (run by the agents)
  - <exact command> → expected <X/Y>
  - valid cases: …
  - invalid cases: …
  - duplicates / double tap: …
HUMAN_TESTS:               (only the owner can run them: Google, phone, Telegram…; "none" if there are none)
  - H1. <what to do> → <what should happen>
CLOSURE_CONDITIONS:
  - <what must exist to move to DONE>
RISKS:
  - <risk> → <mitigation>
NOTES_FOR_EXECUTOR:
  - <architect's assumptions, applicable pitfalls, skills to read>
```

<!--
Appended below, in order, as they happen (formats in agents/templates/REPORTS.md):
## SPEC_AMENDMENT N          (architect)
## ARCHITECTURE_CONFLICT     (executor)
## IMPLEMENTATION_REPORT     (executor)
## AUDIT_REPORT · round 1    (auditor)
## CORRECTION_REPORT · round 2 (executor)
## AUDIT_REPORT · round 2    (auditor)
## HUMAN_TEST_RESULT         (architect, with what the owner reports)
## FINAL_STATUS              (architect)
-->
