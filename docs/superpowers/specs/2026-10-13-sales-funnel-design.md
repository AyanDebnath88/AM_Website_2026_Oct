# AM Electricals sales funnel — design spec

Date: 2026-10-13
Status: approved for implementation planning

## Goal

Build a lead-gen → qualify → outreach → close pipeline for AM Electricals that
runs with minimal intervention from the user. The only two points requiring
human action are: (1) a weekly glance at the `Needs Review` tab, and (2)
approving outreach email copy before it sends. Everything else — scraping,
enrichment, qualification, hierarchy ranking, sequence drafting, stage
tracking — is automated or scriptable on demand.

Covers all 8 industry segments already defined on the live site's
`/industries/` page (Cement/Steel/Material Handling, Water/Effluent/Sewage,
Chemical/Petrochemical/Pharma, Food & Beverage, Commercial Real
Estate/Hospitality, Data Centres/Telecom, Utilities/Residential/Small
Industry, Custom Process Plants) — not just the existing HVAC/MEP pilot.

## Existing assets (do not rebuild)

- **Lead scraper**: `C:\Claude Projects\Scraper Leads\leads_pipeline.py` —
  free (Groq + self-scrape enrichment, no paid API), already produces
  `leads_master.xlsx` (49 leads from an Aug 2026 HVAC-only run, stale/never
  scheduled). Reused and extended, not replaced.
- **`marketing:email-sequence` skill** — drafts full outreach sequences with
  copy, timing, branching. Used for the outreach-copy step.
- **`superseo:page-audit` / `keyword-deep-dive` / `topic-cluster-planning`**
  — used for the separate, non-blocking SEO track.
- **`anthropic-skills:pdf`** — used to build the company brochure.
- Live site's Google Sheet (lead form submissions) and Cloudflare DNS access
  (already proven working this session) — reused for the sending subdomain.

## Components

### 1. Multi-industry lead scraping

Extend `leads_pipeline.py`'s `QUERIES` and extraction prompt to cover all 8
industry segments, not just HVAC/MEP. Pattern: one query set + one
industry-specific extraction-prompt variant per segment, run against the
same free Groq pipeline. Industry tag written to each lead row so
qualification (below) can match it against the site's own segment list.

### 2. Tiered contact enrichment

Extend `enrich_row()`'s `ENRICH_PATHS` beyond the current
`/contact`, `/contact-us`, `/about-us`, `/about` to also fetch `/team`,
`/leadership`, `/management`, `/our-team`, `/company`. Every name+email
found is classified into a hierarchy tier by title keyword match:

- **Tier 1 — Procurement**: Purchase Manager, Procurement Head, Materials
  Manager, Buyer
- **Tier 2 — Owner/Director**: Owner, Proprietor, Director, MD, Managing
  Director, CEO, Founder
- **Tier 3 — Technical**: Plant Head, Project Head, Electrical Engineer,
  Maintenance Head, Works Manager
- **Tier 4 — Generic**: `info@`, `sales@`, `contact@`, or unnamed company
  mailbox

All contacts found for a company are logged; the highest tier present
becomes that company's primary outreach target. This is a best-effort
ranking from public web pages — not a guaranteed org chart (LinkedIn org
data is explicitly out of scope: scraping it violates LinkedIn's ToS and
gets blocked quickly, consistent with the earlier Harvey research).

### 3. Qualification filter (deterministic, zero judgment calls)

A lead is **Qualified** only if ALL of:
- Has a real contact channel: a personal email (any tier 1-3, not generic)
  OR a direct phone number
- Industry tag matches one of the 8 site segments
- Does NOT match a competitor-exclusion keyword list (company name or
  services containing "panel manufacturer", "switchgear manufacturer",
  "control panel manufacturer", "LT panel maker", etc.)

Anything failing any rule lands in a `Needs Review` tab — never enters the
outreach queue automatically. This is the one point requiring a human
glance, batched weekly rather than per-lead.

### 4. CRM — Google Sheets, not a hosted app

`leads_master.xlsx` migrates to a Google Sheet (same ecosystem as the
existing lead-form Sheet). Columns: company, industry, primary contact
(name/title/tier/email/phone), all secondary contacts found, qualification
status, and a `Stage` column with the funnel below. No self-hosted CRM
(Pipelite/Twenty/zero-cost-crm) — all require Docker/Postgres hosting,
unnecessary overhead for this scale.

**Funnel stages:** `New → Qualified → Outreach Drafted (awaiting approval)
→ Approved & Sent → Replied → Meeting Booked → Won / Lost`

### 5. Outreach generation and send (human approval gate)

For each Qualified lead, `marketing:email-sequence` drafts a personalized
3-email lead-nurture sequence using the lead's industry segment and the
site's real differentiators (CPRI 70 kA-tested, IS 8623, 34yr founder-led,
Kolkata factory, real photos — no slop). Drafts are written to the Sheet in
`Outreach Drafted` stage. **Nothing sends without the user's explicit
approval of the copy.** Approved batches are sent via mail-merge from the
dedicated sending mailbox (component 7), then the Sheet row advances to
`Approved & Sent`.

### 6. Company brochure

A PDF built via `anthropic-skills:pdf`, sourced entirely from real site
content: CPRI cert, 70 kA spec, panel family range, factory photos, 34-year
founder-led history. Used as an email attachment and a standalone
leave-behind. Built once, updated when site content changes materially
(e.g. next cert update).

### 7. Sending subdomain

`sales.amelectricals.co.in`, own SPF/DKIM/DMARC, separate from the root
domain so outreach sending can never damage `amelectricals.co.in`'s own
reputation (same reasoning already applied to the Cloudflare Pages
cutover). DNS setup is mine to do (Cloudflare access already proven this
session); creating the actual mailbox (Google Workspace, ~$7/mo) is the
user's own account action — I cannot create accounts on their behalf.

### 8. Run-order playbook

A single markdown doc (separate from this spec) listing the exact skill/
script sequence end to end, so the pipeline can be run without
re-deriving the plan each time:

```
1. Run leads_pipeline.py (all 8 industry query sets)
2. Enrichment + tiering runs inline (component 2)
3. Qualification filter runs inline (component 3) → Sheet
4. User: glance at Needs Review tab (weekly, batched)
5. For each Qualified lead: marketing:email-sequence drafts outreach → Sheet
6. User: approves or edits drafted copy
7. Approved batch sent via sales@ mailbox mail-merge
8. Replies logged, Sheet stage advanced manually or via a lightweight
   reply-check pass
```

## Out of scope for this spec (separate, non-blocking tracks)

- **SEO**: `superseo:page-audit` on homepage + top 3 panel pages,
  `keyword-deep-dive` per industry page. Independent of the funnel, no
  shared state.
- **Google Business Profile**: content/category/photo optimization is
  something I can draft and walk the user through, but verification
  (OTP/mail) is the user's own account action.
- **Google Ads**: campaign structure, keywords, and ad copy can be drafted
  on request, but account creation and budget commitment are the user's
  decision — not something this spec automates or assumes.

## Explicit non-goals

- No LinkedIn automation (ToS violation, gets accounts blocked).
- No cold WhatsApp outreach (confirmed ban risk in India B2B; WhatsApp is
  a warm follow-up channel only, used after a lead has engaged via email).
- No paid enrichment APIs (Hunter/Apollo/Clay/ZoomInfo) — free-tier
  scraping only, per prior explicit rejection of paid tools.
- No fully autonomous sending — every outreach email is human-approved.
