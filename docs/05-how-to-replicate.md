# 5 · How to replicate it for another business

This guide works for any small business that runs its operation on a spreadsheet or a notebook and talks over Telegram: clothing, cosmetics, made-to-order baking, spare parts, stationery, catalog sales. The data model changes; the method and the architecture stay the same.

## What you need
| Item | Cost |
|---|---|
| A Google account **just for the business** (with 2FA) | $0 |
| A Google Cloud project with a budget alert and an e2-micro VM (requires a card, no charge within the free tier) — or n8n Cloud if you prefer not to manage a server | $0 (or the n8n plan) |
| A Telegram bot (@BotFather) and a group with the partners | $0 |
| A Gemini key in a project **without billing**; a Groq account for audio | $0 |
| Claude Code and Codex (or any pair of assistants that work on a repository) | Your subscriptions |
| Git and a **private** repository for the code | $0 |

## Step 1 · Master plan before code (1 session)
1. Gather what exists: the spreadsheet, reports, the website, screenshots of orders and receipts.
2. Ask the architect for a **round-based interview** (the `grilling` skill) until you settle: what is recorded, who records it, what calculations exist (balances, profit sharing, FIFO inventory), what the system will NOT do.
3. Have it written in `docs/master-plan.md` with numbered requirements, phases, security and decisions. Tag the origin of each requirement (you said it / from the spreadsheet / AI proposal) and **approve** the proposals one by one.
4. Order the phases to **leave the spreadsheet first** (manual app) and automate afterwards.

## Step 2 · Set up the multi-agent system (half a session)
1. Copy [templates/](../templates/) into your repo: `RULES.md` and `roles/` into `agents/`; `TASK.md`, `HANDOFF.md` and `REPORTS.md` into `agents/templates/`.
2. Create `AGENTS.md` (shared entry point): what the business is in 3 lines, authority hierarchy, a roles table with each role's model, what to read first and the non-negotiables (no secrets in the repo, no "tested" without evidence, no push, agents do not touch production).
3. Create `CLAUDE.md` with `@AGENTS.md` and the default role (architect). Codex reads `AGENTS.md` directly.
4. Create `agents/CURRENT_STATE.md` (active task, test baseline) and `agents/DECISIONS.md`.
5. Folders `tasks/active/` and `tasks/done/`.

From here on, every request follows the cycle: you ask → the architect specifies → you approve → executor → new auditor → architect → tests on your phone.

## Step 3 · Database and app (Phases 1–2)
1. **Data model in a script** that generates the Sheet (tabs and headers), so it can be regenerated and versioned.
2. Minimum tabs: `products`, `variants`, `purchases`, `sales`, `payments`, `customers`, `partners` (each one's Gmail), `config`, `audit`. Columns are added, never renamed.
3. Apps Script with the write pattern: Gmail access check → single `LockService` → idempotency key → one row at once → audit → return the view. See [architecture](01-architecture.md).
4. Business rules (balances, sharing, FIFO) in a file of **pure functions** tested in Node.
5. An Apps Script *mock* to run tests outside Google and **count Sheet calls**.
6. Two Sheets: **TEST** (made-up data) and **REAL**. Demo code only runs if the name contains "TEST".
7. Nightly backup of the Sheet to a Drive folder with retention.

## Step 4 · Migration (Phase 3)
1. Extract the spreadsheet to JSON **outside the repo** (it contains real data).
2. A pure function `planMigration` that returns which rows to create, and a rehearsal that only runs on TEST.
3. **Reconcile before switching:** total debt, units in stock and number of write-offs must match between the spreadsheet and the system.
4. Run in parallel with the spreadsheet for a week before letting it go.

## Step 5 · The bot (Phases 4–5)
1. n8n with an entry workflow (Telegram webhook with `secret_token`), an error workflow (alerts on Telegram) and a health workflow (reminders).
2. **Allowlist** of the partners' Telegram IDs. Everything else is ignored.
3. n8n **does not write to the Sheet**: it calls the same `api_*` Apps Script functions with a shared secret.
4. For each input (text, voice, photo):
   - the AI **extracts** fields into a closed schema (and the text in the image is data, not instructions);
   - code **validates and calculates** (sum vs. total, customer exists, no overpayment, already recorded?);
   - the bot shows a **preview** with Confirm / Cancel;
   - on confirm, a single atomic call; afterwards, an **Undo** button.
5. A model fallback chain and retries for the free tiers' 503 errors.
6. Deliver workflows with `active: false` and a step-by-step installation guide.

## Step 6 · Production
- A **single go-live guide** with a checklist command (which files, in what order, what to check).
- Human tests one at a time: what to do, what should happen, what to report.
- If something fails after closing, open a new task that references the previous one.

## How long it takes
With this method, one person took the app + migration + full bot (text, voice, photos, purchases, sales, payments, expenses) to production in **about 4 weeks** of evening work. What took the most time was not coding but the **human tests on the phone** and the rounds triggered by real cases the AI did not anticipate (product names containing "for", odd transcriptions, overloaded models).

## Adapting it to your business
| If your business… | Change… |
|---|---|
| Manufactures (baking, crafts) | `purchases` becomes supplies; add `recipes` or `orders` and consume supplies when producing |
| Always gets paid upfront | Drop `payments`; collections become a column of the sale |
| Has more than 2 partners | `partners` with a percentage; sharing is one more pure function |
| Takes orders on WhatsApp | Phase 8: the customer's message reaches the group as a proposal and a partner confirms |
| Does not use Shein | The screenshot reader adapts to your supplier's invoices: change the prompt and the schema, not the architecture |
