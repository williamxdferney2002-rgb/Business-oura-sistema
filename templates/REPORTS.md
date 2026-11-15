# Report formats

Each block is **appended** at the end of the task file, with a heading `## <NAME> · round N`. All fields are always present, even if just "none". Every claim carries evidence (command + result, or `path:line`).

**Brief:** one line per field when that is enough. Green tests: "tests.js 140/140 PASSED", no logs. With failures, only the relevant error. Do not repeat the specification, unchanged files, known decisions or the task history. The chat gets only the verdict or a short summary; the report lives here.

---

## IMPLEMENTATION_REPORT (executor)
`STATUS: COMPLETED` → the task moves to `AWAITING_AUDIT`. `PARTIAL` or `BLOCKED` → the task moves to `BLOCKED` (the architect decides).
```
IMPLEMENTATION_REPORT

TASK_ID:
ROUND: 1
STATUS: COMPLETED | PARTIAL | BLOCKED
COMMIT: the commit that contains this report (code + report together)

FILES_CHANGED:
  - <path> — <what and why (step or AC it satisfies)>
FILES_CREATED:
FILES_DELETED:

CHANGES_IMPLEMENTED:
  - <per function / node, not "various improvements">

DECISIONS_MADE:
  - <minor decision made within scope and why>

DEVIATIONS_FROM_PLAN:
  - none
  (or each deviation: what, why, impact)

ACCEPTANCE_CRITERIA_STATUS:
  AC1: met — evidence: <test / path:line>
  AC2: …

TESTS_EXECUTED:
  - <exact command>
TEST_RESULTS:
  - <summarized output: X/Y, warnings>; baseline before: X/Y, after: X/Y

SELF_AUDIT: <result of the delivery-audit skill: ✅ / ⚠️ / ❌ fixed>

INSTALL_STEPS:          (for the owner, exact order; "not applicable" if nothing to install)
WHAT_TO_REVIEW:         (which nodes/files to review when importing or pasting)
SUGGESTED_TESTS:        (owner tests on TEST / Telegram, with an invalid case and a double tap)
NOT_EXECUTED:           (what did not run: Google, n8n, Telegram, real AI…)

KNOWN_LIMITATIONS:
RISKS_OR_PENDING_ITEMS:
INSTRUCTIONS_FOR_AUDITOR:
  - <what to look at first, how to reproduce, test data>
```

---

## CORRECTION_REPORT (executor, after a REJECTED)
No `DISPUTED` findings → `STATUS: AWAITING_AUDIT`. With a `DISPUTED` one → fix the rest and set `STATUS: BLOCKED` (the architect rules with a `SPEC_AMENDMENT`).
```
CORRECTION_REPORT

TASK_ID:
ROUND: <n>
RESPONDS_TO: AUDIT_REPORT · round <n-1>
STATUS: COMPLETED | PARTIAL | BLOCKED
COMMIT: the commit that contains this report
PREVIOUS_COMMIT: <hash audited before>

FIXES:
  ISSUE_001: FIXED | NOT_FIXED | DISPUTED
    CHANGE: <path:line, what changed>
    EVIDENCE: <test that proves it>
    (DISPUTED: why the finding is wrong, with evidence; the architect decides)
  ISSUE_002: …

OPTIONAL_IMPROVEMENTS_APPLIED:
  - none (or which, only if within scope)

FILES_CHANGED:
DEVIATIONS_FROM_PLAN:
TESTS_EXECUTED:
TEST_RESULTS:
SELF_AUDIT:
NEW_RISKS:
INSTRUCTIONS_FOR_AUDITOR:
```

---

## AUDIT_REPORT (auditor, compact)
Task STATUS: `APPROVED` → `APPROVED`; `REJECTED` → `REJECTED`; `ARCHITECTURE_CONFLICT` (includes a third rejection or a spec failure) → `BLOCKED`. `APPROVED` only with 0 CRITICAL, 0 HIGH and every criterion verified.
```
AUDIT_REPORT

TASK_ID:
ROUND: <n>
AUDITED_COMMIT: <hash> · BASE: <hash> · AUDIT_LEVEL: <QUICK | STANDARD | DEEP>
VERDICT: APPROVED | REJECTED | ARCHITECTURE_CONFLICT

FINDINGS:              (none, or one per line; details in 1–3 sentences)
  CRITICAL:
  HIGH:   H1 — <path:line or area> — <criterion not met (AC#, R##, D##, rule)>: <what happens and short evidence>
  MEDIUM:
  LOW:
REQUIRED_FIXES: <blocking IDs> | none
CRITERIA: <all verified | which not and why>
TESTS: <short command → X/Y, only those the auditor ran>
NOT_VERIFIED: <what could not be run (Google, n8n, Telegram…)> | nothing
NEXT: ARCHITECT
```

---

## ARCHITECTURE_CONFLICT (executor; sets STATUS: BLOCKED)
```
ARCHITECTURE_CONFLICT

TASK_ID:
WHERE: <step / AC / constraint in the spec>
CONFLICTS_WITH: <plan §x, R##, D##, existing code path:line, another AC>
PROBLEM:
EVIDENCE:
OPTIONS:
  A. <option> — consequences
  B. …
EXECUTOR_RECOMMENDATION:
WORK_DONE_SO_FAR: <nothing / commit hash>
```

## SPEC_AMENDMENT (architect; answers every BLOCKED)
```
SPEC_AMENDMENT N
TASK_ID:
RESPONDS_TO: ARCHITECTURE_CONFLICT | DISPUTED in CORRECTION_REPORT · round n | PARTIAL/BLOCKED report | auditor escalation (round n)
RULINGS:
  - <ISSUE_00x DISPUTED>: ACCEPTED (finding withdrawn) | REJECTED (executor must fix it) — why
  - <conflict>: chosen option — why
CHANGES: <which spec fields change and how; "none" if only ruling>
APPROVAL: <owner, date> (required if SCOPE, OUT_OF_SCOPE or ACCEPTANCE_CRITERIA change)
NEXT_STATUS: SPEC_READY (no implementation yet) | REJECTED (executor fixes) | AWAITING_AUDIT (only a ruling was missing; the auditor re-audits with it)
```

## HUMAN_TEST_RESULT (architect, transcribes what the owner reports)
```
HUMAN_TEST_RESULT
TASK_ID:
REPORTED_BY: owner, YYYY-MM-DD
RESULTS:
  H1: PASSED | FAILED — <what the owner saw>
  H2: …
OVERALL: PASSED | FAILED
CLOSURE_AUTHORIZED: yes (owner, date) | no
```

## FINAL_STATUS (architect)
```
FINAL_STATUS
TASK_ID:
RESULT: DONE | CANCELLED
APPROVED_IN: AUDIT_REPORT · round <n> (commit <hash>)
HUMAN_TESTS: PASSED (HUMAN_TEST_RESULT of YYYY-MM-DD) | not applicable
CLOSURE_AUTHORIZED_BY: owner, YYYY-MM-DD | not applicable
ROUNDS: <n>
OWNER_ACTIONS_PENDING: <install in Google / import in n8n / none>
STATE_UPDATED: CURRENT_STATE.md (yes/no), DECISIONS.md (D## or no), plan (proposed / not applicable)
FOLLOW_UP_TASKS: <TASK-YYY or none>
```
