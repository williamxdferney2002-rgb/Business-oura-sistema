# Template: compact HANDOFF

**PROMPT = INDEX · REPOSITORY = MEMORY · CURRENT SPECIFICATION = OPERATIONAL SOURCE.**

Every agent ends each important stage with this block, as the last thing in its chat reply. It is not written into the task file. It points at where the context is; it does not copy it. Target: 100–200 words. Only longer for security, migration, incidents or architectural ambiguity.

Important stages: spec ready, executor report, audit, architect review, `SPEC_AMENDMENT`, `ARCHITECTURE_CONFLICT`, human tests, closure and any stop that needs the owner.

## To an agent
```
HANDOFF
TASK: <TASK_ID>
STATUS: <STATUS (and round)>
NEXT: <EXECUTOR | AUDITOR | ARCHITECT> (<model>, new conversation if applicable)
BASE: <base commit> · <commit to audit or last audited, if applicable>
AUDIT_LEVEL: <QUICK | STANDARD | DEEP>
READ:
- AGENTS.md · agents/roles/<role>.md
- tasks/active/<file>.md → CURRENT SPECIFICATION
- <latest relevant report, if applicable>
DO:
<1–3 sentences>
RETURN:
<what it delivers and where>
```
What goes in READ is not summarized in DO. Do not ask to read a `SPEC_AMENDMENT` already merged into the CURRENT SPECIFICATION unless there is an explicit reason.

## To the owner
No prompt to paste.
```
HANDOFF
TASK: <TASK_ID>
STATUS: <STATUS>
NEXT: OWNER
DO:
1. <where to go, what to tap>
2. …
EXPECTED: <what should be seen; what is PASSED and what is FAILED>
REPORT: <what to reply>
```
Complex human tests go one at a time. If the owner must open another agent, DO says which one and in which conversation, and the "To an agent" block goes below for pasting.

## Who is next
| Who finishes | Case | NEXT |
|---|---|---|
| Architect | Task `SPEC_READY`, fix decided after a `REJECTED`, or `SPEC_AMENDMENT` approved | EXECUTOR |
| Architect | Missing approval, a decision or human tests | OWNER |
| Executor | Commit made with its report, `STATUS: AWAITING_AUDIT` | AUDITOR (new conversation) |
| Executor | `ARCHITECTURE_CONFLICT`, contradiction, decision needed, `PARTIAL`/`BLOCKED`, `DISPUTED` | ARCHITECT |
| Auditor | Any verdict: **always** | ARCHITECT (never directly to the executor) |

## Examples
Architect → executor:
```
HANDOFF
TASK: TASK-XXX
STATUS: SPEC_READY
NEXT: EXECUTOR (Codex Medium)
BASE: <hash>
AUDIT_LEVEL: STANDARD
READ:
- AGENTS.md · agents/roles/executor.md
- tasks/active/TASK-XXX-<slug>.md → CURRENT SPECIFICATION
DO:
Implement only the current specification and run the tests it defines. No push, no production.
RETURN:
Report in the task file + commit made; hash in the HANDOFF.
```

Executor → auditor (only data to locate the audit; no opinions about its own work):
```
HANDOFF
TASK: TASK-XXX
STATUS: AWAITING_AUDIT · round N
NEXT: AUDITOR (<model per AUDIT_LEVEL>, NEW conversation)
BASE: <base> · audit: <executor commit> · previously audited: <hash or "none">
AUDIT_LEVEL: STANDARD
READ:
- AGENTS.md · agents/roles/auditor.md
- tasks/active/TASK-XXX-<slug>.md → CURRENT SPECIFICATION and the executor's latest report
DO:
Audit the actual diff against the current specification. Do not implement.
RETURN:
Compact AUDIT_REPORT in the task file + commit made. NEXT: ARCHITECT.
```

Auditor → architect:
```
HANDOFF
TASK: TASK-XXX · round N
NEXT: ARCHITECT
VERDICT: APPROVED | REJECTED | ARCHITECTURE_CONFLICT
FINDINGS: <only IDs and severities; details are in the AUDIT_REPORT>
READ: tasks/active/TASK-XXX-<slug>.md → AUDIT_REPORT · round N
```

No block carries tokens, keys, emails, personal IDs or customer data.
