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

   **Image map — pull from `web/src/data/panels.json`'s own `image`
   (hero) field AND `gallery` array per category. Both are real photos
   the live site actually displays for that panel (hero thumbnail +
   gallery carousel on the panel's own detail page) — never the
   unrelated raw `/images/panels/*` files that aren't referenced by
   either field for that category.**

   **Rotate, don't repeat:** within a single `/run-funnel` run, if more
   than one lead shares an industry, cycle through that industry's pool
   (hero + gallery, de-duplicated) round-robin by position — lead 1 gets
   pool[0], lead 2 gets pool[1], etc., wrapping around. Never give two
   leads drafted in the same run (or already sitting in the Sheet) the
   identical image for the same industry if the pool has more than one
   entry. When pushing a new lead whose industry already has drafted
   leads in the Sheet, check what the most recent one used and pick the
   next pool entry, not pool[0] again.

   | industry id | panels.json category | image pool (hero + gallery) |
   |---|---|---|
   | fire-safety-systems | Fire Pump Control Panels | `fire-alarm.jpg`, `fire-alarm-1.jpg`, `fire-alarm-3.jpg`, `fire-alarm-4.jpg` |
   | cement-steel-material-handling | MCC Panels | `mcc-4.jpg` (only one real image — no rotation available) |
   | water-effluent-sewage-treatment | STP/ETP/WTP Panels | `stp-etp-wtp-6.jpg`, `stp-etp-wtp-4.jpg`, `stp-etp-wtp-5.jpg`, `stp-etp-wtp-7.jpg` |
   | commercial-real-estate-hospitality | HVAC Control Panels | `hvac.jpg`, `hvac-1.jpg`, `hvac-2.jpg` |
   | chemical-petrochemical-pharma | Custom & Specialised Panels | `custom-5.jpg` (only one real image — no rotation available) |
   | food-beverage-processing | Power Distribution Panels | `pdb-3.jpg` (only one real image — no rotation available) |
   | data-centres-telecom | DG Control Panels | `dg-control.jpg`, `dg-control-1.jpg`, `dg-control-2.jpg`, `dg-control-3.jpg` |
   | utilities-residential-small-industry | APFC Panels | `apfc.jpg`, `apfc-1.jpg`, `apfc-2.jpg`, `apfc-3.jpg`, `apfc-4.jpg` |
   | custom-process-plants | Custom & Specialised Panels | `custom-5.jpg` (only one real image — no rotation available) |

   Prefix every image path with `https://amelectricals.co.in/images/panels/`
   for the live URL. `email_2`/`email_3` stay short plain text (as already
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
