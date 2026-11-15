# 2 · Multi-agent system

## The problem
A single AI assistant that plans, codes and reviews itself tends to agree with itself: it declares "tested" what never ran, changes scope without saying so and forgets decisions from earlier sessions. With 30 tasks in a month, that does not scale.

## The solution: three roles, one memory in files

| Role | Tool | Does | Does not |
|---|---|---|---|
| **Architect** | Claude Code | Reads the plan and the code, interviews the owner, writes the specification for each task, triages audit findings, keeps the state and the decision log | Write production code |
| **Executor** | Codex (Medium level; High only for justified escalations). Fallback: a fresh Claude instance | Implements **only** the current specification, runs the tests, self-audits, makes one commit with code and report | Redesign or change scope: if the spec conflicts with something, it writes `ARCHITECTURE_CONFLICT` |
| **Auditor** | A **new**, independent conversation (model depends on the audit level) | Reviews the actual commit against the spec, runs the tests, looks for regressions and security issues | Fix code: it sends findings back |

Above them, **the owner**: approves every specification, decides on conflicts, installs in Google/n8n and runs the human tests on the phone.

**Executor and auditor are never the same conversation** and, preferably, not the same model either. That is the defense against self-approval bias.

## Authority hierarchy
```
MASTER PLAN      requirements R01–R62, phases, security, founding decisions
   ↓
DECISIONS        D37 onwards, each with date, reason and who approved it
   ↓
TASK             one specification per file
   ↓
IMPLEMENTATION   code + IMPLEMENTATION_REPORT
   ↓
AUDIT            AUDIT_REPORT
```
No agent silently contradicts a higher level: it writes it down and escalates.

## Task lifecycle

```
DRAFT ──(owner approval)──► SPEC_READY ──► IN_PROGRESS ──► AWAITING_AUDIT
                                                              │
                     ┌───────────── REJECTED ◄────────────────┤
                     ▼                                        ▼
        architect triages:                                 APPROVED
        · fix → executor → CORRECTION_REPORT                  │
        · spec change → SPEC_AMENDMENT                        ▼
                                                     AWAITING_HUMAN (tests on the phone)
                                                              │ PASSED
                                                              ▼
                                                            DONE
BLOCKED: architecture conflict, partial report, disputed finding or third rejection.
```

Each task lives in **a single file** (`tasks/active/TASK-XXX-*.md`). At the top, the `CURRENT SPECIFICATION` (the only part that is edited); below it, the history that each role **appends** and never rewrites: original spec, amendments, reports and audits. Whoever comes next finds everything in one place.

Key fields of the specification ([template](../templates/TASK.md)): objective, scope and out of scope, files to inspect and to change, steps, constraints (contracts that do not change, speed), **acceptance criteria verifiable without asking anyone**, automated tests with the expected `X/Y` result, human tests and risks.

## Handoff: the prompt is an index
**PROMPT = INDEX · REPOSITORY = MEMORY · CURRENT SPECIFICATION = OPERATIONAL SOURCE.**

Each agent ends its stage with a 100–200 word block that says who is next, what to read, what to do and what to return. It does not copy the task: it points at it.

```
HANDOFF
TASK: TASK-XXX
STATUS: AWAITING_AUDIT · round 2
NEXT: AUDITOR (NEW conversation)
BASE: <base commit> · audit: <executor commit>
AUDIT_LEVEL: STANDARD
READ:
- AGENTS.md · agents/roles/auditor.md
- tasks/active/TASK-XXX-<slug>.md → CURRENT SPECIFICATION and latest report
DO: Audit the actual diff against the current specification. Do not implement.
RETURN: AUDIT_REPORT in the task file + commit. NEXT: CLAUDE.
```

Effect: each new agent starts by reading 4 files, not the whole repository. Fewer tokens, less confusion.

## Audit levels
| Level | When | Auditor |
|---|---|---|
| `QUICK` | Small, low-risk changes (a label, a format) | Cheaper model |
| `STANDARD` | The default | Claude or Codex in a new conversation |
| `DEEP` | Money, atomic writes, security, migration | Strong model |

## Rules that mattered most
- **No false positives:** never say "works" or "tested" without evidence run in that session (command and `X/Y` result). What could not be run (inside Google, real Telegram) is declared in `NOT_EXECUTED`.
- **Minimal changes:** only the files the task lists; no "improving" neighboring code.
- **Do not destroy:** nothing is deleted without written justification; no `git reset --hard` on uncommitted work.
- **One commit per delivery** with code and report together; the auditor reviews exactly that hash.
- **Agents do not touch production:** not Google, not the sync tool, not the real Sheet. The owner does that with a step-by-step guide.
- **No push:** the owner decides when to push the branch.

Full text: [templates/RULES.md](../templates/RULES.md) and [templates/roles/](../templates/roles/).

## How coordination evolved
1. **Manual (Oct 2026).** The owner copied each handoff from one tool to another: Claude → Codex → new Codex → Claude. It worked, but each task meant 4–8 copy-pastes.
2. **Automatic orchestrator (attempted and postponed).** A Node script was built to launch short-lived Codex processes with read-only permissions and no network. The first test showed that the native Windows sandbox of that version could not guarantee the required read boundary. Decision: **do not use it** until the tool can guarantee it. Lesson: if a security boundary cannot be demonstrated, it does not exist.
3. **Claude as the bridge (Oct 27, 2026).** Claude launches the executor with `codex exec` and, for each audit, a new Codex conversation. After a `REJECTED` it relaunches the fix without waiting for the owner, unless the scope changes. At most 3 rounds per task. The owner only approves specs, installs and tests.
4. **No approval per commit (Nov 4, 2026).** Approving the specification covers every commit of the task. A COMMIT block is shown as a record (files, tests, message) and the commit is made.

## What the owner gained
- Reviewing **specifications** in plain language, not diffs.
- Every delivery includes: what changed, how to install it in exact order, what to check and which tests to run on the phone.
- The separation of roles caught problems before they reached the phone: high-risk issues in the customer statement PDF generation (the pilot task), false alerts on double tap in the bot, a text color with insufficient contrast in customer documents, and functions that would have made more Sheet calls than allowed.
