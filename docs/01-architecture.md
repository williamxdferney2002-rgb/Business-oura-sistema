# 1 · Architecture

## Constraints that shaped it
- **Cost as close to zero as possible.** No paid AI billing.
- **Leave Excel as soon as possible:** first a manual app that replaces it; automation comes later.
- **Two users, both on their phones**, plus a Telegram group they already used to talk.
- **Low volume:** a few dozen transactions per month. A "real" database is not needed.
- **One person building**, with AI agents.

## System map

```
Telegram (partners' group) ──────┐
WhatsApp (customers, Phase 8) ───┼──► n8n (free e2-micro VM + Caddy with HTTPS)
                                 │        │  never writes to the Sheet directly: calls Apps Script functions
Internal app (Apps Script) ──────┼────────┼──► Google Sheets (data + calculated tabs)
(only the partners'              │        │        │
 Gmail accounts)                 │        │        ├──► Looker Studio (Phase 9)
                                 │        │        └──► public_catalog tab ──► public endpoint ──► website (Phase 7)
Google Drive: order screenshots, payment receipts, PDFs and nightly Sheet backup
Free AI: Gemini (screenshots and text) · Groq Whisper (voice) · Gemma (fallback)
```

| Component | Choice | Why |
|---|---|---|
| Database | **Google Sheets** | Free, never paused for inactivity, the partners already understand it, native Looker connector. Supabase was planned at first and replaced in the first week |
| Internal app | **Apps Script** (web app) | Lives next to the Sheet, free Gmail-based authentication, no server |
| Automation | **Self-hosted n8n** on an e2-micro VM from the Google Cloud free tier | Visual workflows, Telegram and AI nodes, no per-execution cost |
| AI | Gemini with a key from a project **without billing**; Groq Whisper for audio; Gemma as fallback | Free quotas cover the volume; a fallback chain handles 503 errors |
| Files | Google Drive | Screenshots and receipts stay next to the record that uses them |

## The five rules that hold everything together

1. **Single writer.** Every write goes through an `api_*` function in Apps Script, protected by one `LockService` lock. The app and the bot share the same lock, so they never collide. n8n does not use the Google Sheets node to write.
2. **Idempotency.** Every operation carries a unique key (Telegram message id + execution number, or a form id). A double tap or a network retry produces **exactly one record**.
3. **AI proposes, a human confirms, code calculates.** The model reads the screenshot or voice note and proposes; the bot shows a preview with a **Confirm** button. Sums, balances, FIFO inventory costing and profit sharing are done by deterministic, tested code, never by the model.
4. **Void, never delete.** Sales, purchases, payments and write-offs are voided with a reason; every change lands in an audit tab (history). Production corrections are new rows, never edits to calculated rows.
5. **Separate test copy.** A "TEST" Sheet with made-up data is where every version is installed and tested before going to the real one. Demo code and migration rehearsals only run if the Sheet name contains "TEST".

## Pattern of every write function

```
api_registerPayment(data)
  → requireAccess_()      is the email in the partners tab?
  → withLock_(...)        a single LockService for the whole app and the bot
  → idempotency key       already recorded? → return the same result
  → append_/update_       one row at once
  → audit_                written to the history
  → returns the updated view (the page does not ask for it again)
```

## Security (mandatory in every phase)
- Secrets only in **n8n credentials** and Apps Script `PropertiesService`. Never in code, JSON, the repo or chat.
- **Allowlist:** in Telegram only the partners' IDs can give commands; in the app only their Gmail accounts.
- **Signed webhooks:** Telegram with `secret_token`; n8n calls to Apps Script carry a shared secret.
- **Everything that comes from customers, screenshots or receipts is data, not instructions** (defense against prompt injection in images).
- The future website will only see a public tab (name, list price, colors, status, photo). Never costs, margins or customers.
- A global error workflow that alerts on Telegram, and a nightly Sheet backup with 30-day retention.

## Speed
Apps Script is slow to start (10–20 s for the first save) and every `google.script.run` round trip costs 1–3 s. So:
- The tabs a screen needs are read **in a single call** (`Sheets.Spreadsheets.Values.batchGet`).
- Each execution caches in memory what it already read.
- Every action that saves returns the updated view.
- Tests outside Google **count the calls to the Sheet**: a new function that reads more than allowed fails in tests before reaching production.

Result: from 8–11 s per save at the beginning to about 3 s, and screens that open instantly with preloaded data.
