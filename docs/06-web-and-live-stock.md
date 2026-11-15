# 6 · Website with live stock (Phase 7)

## The goal
A new, good-looking catalog website that shows **what is actually in stock**: when a partner records a sale from the bot or the app, the product leaves "Available now" within minutes, without anyone editing the website.

Planned sections:
- **Available now** (stock > 0).
- **New arrivals** (recently received).
- **Made to order** (out of stock, or products ordered from Shein on demand).
- Search, colors per product and a **cart that ends in a WhatsApp message** with the order ready.
- Hide products manually from the app.

The visual design, structure and colors are defined by the owner (with his Canva design) **before** any line is written: the AI does not propose its own design.

## The problem: response times
Google Sheets + Apps Script is free and convenient, but not fast:

| Real measurement | Value |
|---|---|
| First call after idle time (cold start) | 10–20 s |
| Typical server-side read | 0.7–2.1 s |
| Perceived round trip from the browser | 3–6 s |
| Apps Script quotas | Limited per day and per user |

A public website cannot wait 10 s or depend on Apps Script handling every visit.

## The solution: the website never waits for the Sheet

```
Sale / purchase / adjustment in the app or the bot
        │  (the write already goes through Apps Script)
        ▼
public_catalog tab (only: name, list price, colors, status, photo)
        │
        ├──► Public endpoint from a SEPARATE Apps Script, with CacheService for 1–5 min
        │
        └──► n8n every N minutes (or on change): generates catalog.json
                   and publishes it to the static host via GitHub
                                │
                                ▼
            Static website (Cloudflare Pages, free) reads catalog.json from its own domain:
            loads in milliseconds from the CDN, even when Google is slow
```

Design decisions:
1. **Full separation.** The website only knows `public_catalog`, served by an independent Apps Script. It never sees costs, margins, customers or the Sheet. An automated test checks that the response does not contain those fields.
2. **JSON snapshot on the CDN** as the main source. The website opens instantly; the cached endpoint remains as a fallback and for verification.
3. **Bounded, measurable freshness:** target "a sale shows on the website in ≤ 5 minutes". That is enough for a business that sells over WhatsApp, and it avoids calling Google on every visit.
4. **Out of stock → Made to order**, not "sold out": the sale is not lost.
5. **Photos outside Drive.** The original stays in Drive; n8n creates a **WebP copy in two sizes** and publishes it to the host. The website does not depend on Drive links (slow and rate-limited).
6. **Photo flow over Telegram:** the bot lists products without a photo; the partner sends the photo **as a file** (uncompressed); n8n processes and publishes it. Duplicate or oversized photos are rejected with a notice.

## Planned tests
- The endpoint response and the JSON **never** include cost, margin or customers.
- Product without a photo → placeholder image.
- Sale in the app → reflected on the website within ≤ 5 min.
- Phone and desktop; duplicate or oversized photo.

## Estimate
5–8 sessions once the design is delivered. Depends on: Canva design, logo and photos.

## If your business outgrows this
The architecture leaves a clear exit: the website already consumes a static JSON, so replacing Sheets with a real database (Supabase, Postgres) only changes **who generates the JSON**, not the website.
