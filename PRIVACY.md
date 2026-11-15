# Privacy: what is published and what is not

This repository is the public version of a private project. The rule is simple: **publish the method, never the data or the keys.**

## Never included
- Tokens, API keys, passwords, shared secrets between n8n and Apps Script.
- Links or IDs of Google Sheets, Drive, Apps Script projects and deployments (`/exec`).
- Domain and address of the n8n server, webhook IDs.
- Bot username, Telegram chat, group and user IDs.
- Partners' emails, phone numbers and city.
- Customer data, real amounts of debts or sales, screenshots of orders or payment receipts.
- The production code as-is (it contains configuration constants). The architecture is described and templates are published instead.
- The name of the private repository and its branches.

## Published
- The project name (Oura), the type of business and the author.
- The architecture, the technical decisions and why they were made.
- The project log (what was built and what was learned), with dates.
- The rules, roles and templates of the multi-agent system.
- Aggregate project figures (commits, tasks, number of tests), never business figures.

## How it is checked
`check_privacy.py` looks for secret patterns (Google keys, Telegram tokens, Groq/OpenAI/GitHub keys, private keys), Google links and IDs, Telegram IDs, phone numbers, emails and tunnel domains. It also reads `.privacy-local.txt`, a denylist with real names and IDs that **only exists on the owner's computer** (it is in `.gitignore`), so the list itself is not a leak.

```bash
python check_privacy.py --test   # self-test of the patterns
python check_privacy.py          # scans the folder; exit code 1 if anything is found
```

The script never prints the matched value, only file, line and type. If something leaks in a commit that was already pushed, deleting it in a new commit is not enough: **rotate the key** (create a new one and revoke the old one) and rewrite the history.
