Run the AM Electricals sales funnel end to end, per `docs/superpowers/sales-funnel-playbook.md`:

1. Run the scraper: `cd "C:\Claude Projects\Scraper Leads" && python leads_pipeline.py`
   (Groq daily cap stopping it early is normal — note it, don't retry.)
2. Read `leads_master.xlsx`'s **Leads** tab, diff against the CRM Sheet's
   `Leads` tab (spreadsheet_id `1TCzHQtdsrpgU1nRIn-XF-feolvmbzjotSqLWZ3i8uSM`)
   by `company_name`+`website`, push only new rows, `stage` = `Qualified`.
3. For every `Qualified`-stage row with no `outreach_draft`, use the
   `marketing:email-sequence` skill to draft a 3-email sequence (match
   industry + contact_tier, use only claims the live site actually makes —
   CPRI 70 kA, IS 8623, 34yr founder-led, Kolkata factory). Write the draft
   into `outreach_draft`, set `stage` = `Outreach Drafted`.
4. Report counts (pushed / drafted / Needs Review backlog from the
   Dashboard tab) and STOP. Do not touch `Approved` or `Sent` rows — sending
   requires my explicit go-ahead, never part of this command.
