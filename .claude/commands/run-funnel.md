Run the AM Electricals sales funnel end to end, per `docs/superpowers/sales-funnel-playbook.md`:

1. Run the scraper: `cd "C:\Claude Projects\Scraper Leads" && python leads_pipeline.py`
   (Groq daily cap stopping it early is normal — note it, don't retry.)
2. Read `leads_master.xlsx`'s **Leads** tab, diff against the CRM Sheet's
   `Leads` tab (spreadsheet_id `1TCzHQtdsrpgU1nRIn-XF-feolvmbzjotSqLWZ3i8uSM`)
   by `company_name`+`website`, push only new rows, `stage` = `Qualified`,
   `zone` from the scraper's own `zone` column.
3. For every `Qualified`-stage row with no `email_1`, draft a 3-email
   sequence — always via both `marketing:email-sequence` AND
   `marketing:draft-content` skills together (standing rule, see
   `feedback_email_copy_skills.md`), matching industry + contact_tier,
   using only claims the live site actually makes (CPRI 70 kA, IS 8623,
   34yr founder-led, Kolkata factory). Write `email_1`, `email_2`, `email_3`
   into separate columns (P/T/U), `stage` → `Outreach Drafted`.

   **`email_1` is an image-backed HTML email, not plain text.** Build it
   from this exact template, swapping only the bracketed parts:

   ```html
   <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;padding:24px 0;"><tr><td align="center"><table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;font-family:Arial,sans-serif;"><tr><td><img src="https://amelectricals.co.in/images/marketing/prospectus-banner.png" width="600" style="display:block;width:100%;" alt="AM Electricals - control panel manufacturer, Kolkata"></td></tr><tr><td style="padding:24px 32px 8px 32px;font-size:15px;line-height:1.6;color:#222;"><p>[greeting]</p><p>[pain-point paragraph, 1-2 sentences, personalized to the lead]</p><p>[proof/CTA bridge paragraph, 1 sentence]</p></td></tr><tr><td style="padding:8px 32px;"><img src="[IMAGE URL - see map below]" width="536" style="display:block;width:100%;border-radius:4px;" alt="[panel type], from our product range"></td></tr><tr><td style="padding:16px 32px 24px 32px;font-size:15px;line-height:1.6;color:#222;"><p>[one-line CTA]</p></td></tr><tr><td style="padding:16px 32px 32px 32px;border-top:1px solid #eee;"><p style="margin:0;font-weight:bold;">Ayan Debnath</p><p style="margin:0;color:#666;">AM Electricals | 7980954823 | <a href="https://amelectricals.co.in" style="color:#c0392b;text-decoration:none;">amelectricals.co.in</a></p></td></tr></table></td></tr></table>
   ```

   **Image map — always pull from `web/src/data/panels.json`'s own
   `image` field per category (the real on-site photo), never the raw
   `/images/panels/*-1.jpg` etc "secondary shot" gallery, which is lower
   quality and not what the site itself shows:**

   | industry id | panels.json category | image |
   |---|---|---|
   | cement-steel-material-handling | MCC Panels | `/images/panels/mcc-4.jpg` |
   | water-effluent-sewage-treatment | STP/ETP/WTP Panels | `/images/panels/stp-etp-wtp-6.jpg` |
   | commercial-real-estate-hospitality | HVAC Control Panels | `/images/panels/hvac.jpg` |
   | chemical-petrochemical-pharma | Custom & Specialised Panels | `/images/panels/custom-5.jpg` |
   | food-beverage-processing | Power Distribution Panels | `/images/panels/pdb-3.jpg` |
   | data-centres-telecom | DG Control Panels | `/images/panels/dg-control.jpg` |
   | utilities-residential-small-industry | APFC Panels | `/images/panels/apfc.jpg` |
   | custom-process-plants | Custom & Specialised Panels | `/images/panels/custom-5.jpg` |

   Prefix every image path with `https://amelectricals.co.in` for the
   live URL. `email_2`/`email_3` stay short plain text (as already
   established), signed just `Ayan`.

   **Signature identity is Ayan Debnath (7980954823)** — the person
   running this funnel, not founder Ajit Debnath. Company-history claims
   ("34 years founder-led") stay factual and unchanged; only the sender
   line changes.

4. Generate (or update) the copy-ready preview Artifact: one HTML page,
   per-lead sections switched by `#company-key` hash anchor, each image
   embedded as a base64 data URI (Artifact CSP blocks remote images), with
   a "Copy for Gmail" button using the Clipboard API
   (`text/html` + `text/plain` ClipboardItem). Add/update a `preview_link`
   column (V) in the Leads Sheet with a `HYPERLINK()` formula per new row
   pointing at `<artifact-url>#<key>`.
5. Report counts (pushed / drafted / Needs Review backlog from the
   Dashboard tab) and STOP. Do not touch `Approved` or `Sent` rows — sending
   requires my explicit go-ahead, never part of this command.
