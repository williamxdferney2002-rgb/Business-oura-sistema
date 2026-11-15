# Oura · A small business run from Telegram, built with a team of AI agents

> How one person, with no development team, replaced a small business's Excel workbook with its own system (internal web app + Telegram bot) by directing three AI agents with separate roles: one that **plans**, one that **implements** and an independent one that **audits**.

**Oura** is a small resale business in Colombia owned by two partners (50/50). They buy products (mostly from Shein) and sell them to customers who pay upfront or in installments. For years everything lived in a macro-heavy Excel workbook: purchases, inventory, sales, installments, debts, expenses and profit sharing. This repository explains how the system that replaced it was built, and provides the pieces for another small business to replicate it.

> This repo contains no production code and no real data. It contains the **methodology**, the **architecture**, the **project log** and the **templates** of the multi-agent system, ready to copy. See [PRIVACY.md](PRIVACY.md).

## What the system does today

| Component | What it does | Status (Nov 2026) |
|---|---|---|
| **Internal app** (Google Apps Script on Google Sheets) | Purchases, live inventory, sales, installments split across sales, collections, inventory write-offs, voids with full history, customer statements and invoices as PDF/image | In production |
| **Telegram bot** (n8n) in the partners' group | Records **Shein orders from a screenshot**, **payments from a receipt photo or a voice note**, **sales and expenses by text or voice**, debt lookups, order tracking and undo. Always with a preview and a **Confirm** button | In production |
| **Catalog website with live stock** | Show what is available now, new arrivals and "made to order", with a cart that ends in WhatsApp | Planned (Phase 7) · [see design](docs/06-web-and-live-stock.md) |
| **WhatsApp for customers** | Receive orders and forward them to the group for a partner to confirm | Planned (Phase 8) |
| **Dashboard** (Looker Studio) | Sales, debtors, profit per partner, unsold stock | Planned (Phase 9) |

## Project figures

- **Timeline:** from Oct 4, 2026 (first commit) to Nov 4, 2026 (app and bot fully in production on Nov 2) · 25 working days.
- **~360 commits** and **31 specified tasks**, each with its specification, implementation report and audit in a single file.
- **~1,050 automated checks** that run outside Google (business rules, deployment sync tool, UI screens in Chromium at 390 and 1366 px).
- **Infrastructure: $0/month.** Free tiers of Google Cloud, a personal Google account, self-hosted n8n and AI models with free quotas. The only cost is the AI assistant subscriptions used to build it.

## The core idea in one picture

```
                  ┌──────────── the owner (approves specs, installs, tests on the phone)
                  ▼
   ARCHITECT (Claude Code) ── spec ──► EXECUTOR (Codex) ── commit + report ──► AUDITOR (NEW conversation)
          ▲                                                                         │
          └──────────────────── APPROVED / REJECTED + findings ─────────────────────┘

   Shared memory = Markdown files in the repo (plan, decisions, one task = one file).
   The prompt only points at what to read: PROMPT = INDEX · REPOSITORY = MEMORY.
```

## Documentation

| # | Document | What it covers |
|---|---|---|
| 1 | [Architecture](docs/01-architecture.md) | How it is built: Sheets as the database, a single writer, AI that proposes and code that calculates, security |
| 2 | [Multi-agent system](docs/02-multi-agent-system.md) | Roles, protocol, task states, handoff, audit levels and how it evolved |
| 3 | [Tools](docs/03-tools.md) | Everything that was used and why: Claude Code, Codex, skills, n8n, Apps Script, Gemini, Groq, Playwright… |
| 4 | [Project log](docs/04-project-log.md) | What was done, in what order and what was learned (kept up to date) |
| 5 | [How to replicate it](docs/05-how-to-replicate.md) | Step-by-step guide to build the same thing for another business that records from Telegram |
| 6 | [Website with live stock](docs/06-web-and-live-stock.md) | The website goal, the response-time problem and how it will be solved |
| — | [Templates](templates/) | Rules, roles and formats (TASK, HANDOFF, reports) of the multi-agent system, ready to copy |

## How this repo is maintained

This folder is the **public version** of the project, separate from the private repository. Every time a task or phase is closed:

1. An entry is added to [docs/04-project-log.md](docs/04-project-log.md) (what was done and learned, no data).
2. The privacy checker runs: `python check_privacy.py` must end with `Result: 0 findings.`
3. Only then is the change committed and pushed.

## Author

**William Delgado, Engineer** · Colombia · [GitHub](https://github.com/williamxdferney2002-rgb)

Co-founder of Oura and author of the system. I designed the architecture and wrote the master plan (requirements, phases, security, data model). I also created the multi-agent method and its rules, and directed the agents task by task: I approved every specification, made the calls on conflicts, ran the acceptance tests and handled the production rollout. In the rest of the documentation I appear as "the owner".

What this project demonstrates:
- **Directing AI agents as a team:** separate roles, independent audits, verifiable specifications and memory in the repository.
- **Business process automation** with n8n, Google Apps Script, Google Sheets and AI APIs (Gemini, Groq Whisper).
- **Taking a system from zero to production in one month**, with $0 infrastructure cost, automated tests and security by design.

## License

Documentation and templates under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/): use them, adapt them and credit the source.

---

### Resumen en español

Oura es un pequeño negocio de reventa en Colombia. Este repositorio documenta cómo su cofundador reemplazó el Excel del negocio por un sistema propio: una app interna en Google Apps Script y un bot de Telegram en n8n que registra compras desde pantallazos, abonos desde fotos de comprobantes o notas de voz, y ventas y gastos por texto o voz. Para construirlo dirigió a tres agentes de IA con roles separados (arquitecto, ejecutor y auditor independiente). Pasó de cero a producción en un mes, con costo de infraestructura $0. Aquí se publican la metodología, la arquitectura, la bitácora y las plantillas para replicarlo; el código de producción y los datos reales no se publican.
