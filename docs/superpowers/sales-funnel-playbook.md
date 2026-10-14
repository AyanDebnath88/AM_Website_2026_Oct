# AM Electricals sales funnel — run-order playbook

One doc, run top to bottom. No step here requires re-deriving the plan —
just follow it. See `specs/2026-10-13-sales-funnel-design.md` for the full
design rationale.

## Prerequisites (one-time, done 2026-10-13/14)

- [x] Live site deployed, Cloudflare Pages + custom domain cutover complete
- [x] Google Forms lead-capture wired (site's own Contact/Quote forms)
- [x] Lead scraper extended to all 8 industry segments, qualification +
      tiering built in — `C:\Claude Projects\Scraper Leads\leads_pipeline.py`
- [x] Sending mailbox: `outreach@amelectricals.co.in` via Brevo SMTP relay
      through Gmail "Send mail as", domain authenticated (SPF/DKIM/DMARC)
- [ ] Google Sheets CRM connected (Composio) — one-time OAuth click needed
- [ ] Sheet CRM created and scraper output pushed to it
- [ ] Company brochure PDF built

## Step-by-step run

### 1. Scrape

```bash
cd "C:\Claude Projects\Scraper Leads"
python leads_pipeline.py
```

Covers all 8 industries in one run. Free tier (Groq) caps around 500k
tokens/day — if it stops early with "daily token cap reached", that's
normal; rerun the next day to pick up where it left off (dedupes
automatically against everything already in the workbook).

### 2. Enrichment + tiering (automatic, inside the scrape)

No separate step — `enrich_row()` and `classify_tier()` run inline per
lead during step 1. Output: `contact_tier` (1=Procurement, 2=Owner/
Director, 3=Technical, 4=Generic), `contact_email`, `contact_phone`,
`other_contacts_found`.

### 3. Qualification (automatic, inside the scrape)

Also inline — `qualify()` runs per lead. Writes to two sheets in
`leads_master.xlsx`:
- **Leads** — qualified (real contact + industry match + not a
  competitor)
- **Needs Review** — everything else, with `disqualify_reason` filled in

### 4. Your weekly glance (the one required check)

Open `leads_master.xlsx` → **Needs Review** tab. Skim for anything that
should actually qualify (e.g. a phone number the regex missed, a
borderline industry match). Nothing here enters outreach until you
either fix it and move the row, or leave it — it's a one-way filter, not
a queue that blocks on you.

### 5. Push to the Sheet CRM

Once the Google Sheets connection is active (see Prerequisites), the
qualified leads get synced from `leads_master.xlsx`'s **Leads** tab into
the CRM Sheet, with the `Stage` column defaulted to `Qualified` for new
rows. (First-time setup only — after that this is a standing sync, not a
manual step per run.)

### 6. Draft outreach copy

For each `Qualified`-stage row in the Sheet, use the `marketing:email-sequence`
skill to draft a personalized 3-email lead-nurture sequence:
- Audience: the lead's industry segment + contact tier
- Differentiators to use: CPRI 70 kA-tested, IS 8623, 34yr founder-led,
  Kolkata factory, real shopfloor photos (see live site for exact current
  copy/claims — don't let drafts drift from what the site actually says)
- Write the draft into the Sheet, set `Stage` → `Outreach Drafted`

### 7. Your approval (the other required gate)

Review drafted copy in the Sheet. Edit freely. When ready, mark `Stage`
→ `Approved`. **Nothing sends without this.**

### 8. Send

Approved rows get mail-merged out via `outreach@amelectricals.co.in`.
After sending, `Stage` → `Sent`.

### 9. Track replies

When a lead replies, update `Stage` manually: `Replied` → `Meeting
Booked` → `Won`/`Lost`. WhatsApp follow-up only after a lead has engaged
by email — never cold WhatsApp (confirmed ban risk in India B2B).

## Non-negotiables (carried over from the design spec)

- No LinkedIn automation
- No cold WhatsApp
- No paid enrichment APIs
- No email sends without your explicit approval
- Competitor companies filtered out automatically, never enter the funnel
