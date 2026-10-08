# AM Electricals . Deploy Handover

Step-by-step to get the new site live on `amelectricals.co.in` without breaking the current Softr site.

## Prereqs

- GitHub repo: https://github.com/AyanDebnath88/AM_Website_2026_Oct.git (already set up)
- Cloudflare account (free): https://dash.cloudflare.com/sign-up
- Web3Forms free access key: https://web3forms.com/ (60 seconds, no card)
- Google Search Console access to `amelectricals.co.in`
- GoDaddy control panel (DNS records)

## Phase 1 . Push code to the repo (5 min)

```bash
cd "E:/Claude Projects/AM ELECTRICALS WEBSITE"
git init
git add .
git commit -m "Initial commit: AM Electricals site v1"
git remote add origin https://github.com/AyanDebnath88/AM_Website_2026_Oct.git
git push -u origin main
```

## Phase 2 . Deploy to Cloudflare Pages (10 min)

1. Go to Cloudflare dashboard . **Workers & Pages** . **Create** . **Pages** . **Connect to Git**
2. Authorize GitHub, pick `AM_Website_2026_Oct`
3. Build settings:
   - Framework preset: **Astro**
   - Root directory: `web`
   - Build command: `npm run build`
   - Output directory: `dist`
4. Add environment variables (from `web/.env.example`):
   - `WEB3FORMS_KEY`
   - `PUBLIC_PLAUSIBLE_DOMAIN`
   - `PUBLIC_GSC_VERIFY`
   - `PUBLIC_BING_VERIFY`
5. Click **Save and Deploy** . live in ~1-2 min at `am-website-2026-oct.pages.dev`

301 redirects (old Softr URLs) and security/cache headers are already in `web/public/_redirects` and `web/public/_headers` . Cloudflare Pages picks these up automatically, no extra config needed.

## Phase 3 . Attach the staging subdomain (15 min)

1. Pages project . **Custom domains** . **Set up a custom domain** . enter `new.amelectricals.co.in`
2. Cloudflare shows a CNAME target (e.g. `am-website-2026-oct.pages.dev`)
3. GoDaddy DNS . add CNAME . `new` -> that target (TTL 600)
4. Wait 10 min . visit https://new.amelectricals.co.in . SSL provisions automatically

## Phase 4 . UAT on staging (24-48 hours)

Walk the site on desktop + phone. Submit the lead form (real WhatsApp + real email). Verify:
- Every panel page loads with the right hero photo + gallery
- Nav, footer, breadcrumbs correct
- Cert chips + spec table render
- Contact page map loads
- Careers form submits
- Old URLs (`/apfc`, `/mcc`, etc.) redirect correctly to new panel pages
- Lighthouse (Chrome DevTools): Perf, A11y, SEO all >=90

Fix anything that breaks. Redeploy is instant via `git push`.

## Phase 5 . Google Search Console + Analytics (2 hours before cutover)

1. Search Console -> Add property -> `https://amelectricals.co.in` (Domain property preferred)
2. Verify via DNS TXT (GoDaddy: add TXT with the token Google gives you)
3. Submit sitemap: `https://amelectricals.co.in/sitemap-index.xml`
4. Bing Webmaster Tools . same flow, submit same sitemap
5. Plausible: add site `amelectricals.co.in` . confirm hits are flowing on `new.amelectricals.co.in`
6. Google Business Profile . verify hours, category "Electrical equipment manufacturer", add fresh photos

## Phase 6 . DNS cutover to production (30 min window, LOW risk)

**24 hours before:** Lower the TTL on the production `amelectricals.co.in` A/CNAME record to 300 seconds (5 min). Wait 24h so caches expire.

**Cutover:**
1. In GoDaddy DNS . edit the root `@` record:
   - Delete existing `A` record pointing at Softr
   - Add `CNAME` `@` -> `am-website-2026-oct.pages.dev` (GoDaddy supports CNAME flattening on root; if not, use Cloudflare's full DNS/nameserver takeover for a cleaner setup)
2. `www` CNAME -> `am-website-2026-oct.pages.dev`
3. **DO NOT change MX records** (your email stays on GoDaddy / current provider)
4. Verify propagation: `dig amelectricals.co.in @1.1.1.1` should return the Cloudflare Pages target within 5-10 min

## Phase 7 . Post-cutover (first 72 hours)

- Check form submissions land in email + WhatsApp
- Watch Search Console for crawl spikes / errors
- Softr subscription: **keep active 30 days** as rollback insurance
- 301 redirects from old Softr URLs to new URLs are already in `web/public/_redirects` -> live automatically
- Google Business Profile: add a post with the new site URL

## Rollback (if something goes wrong)

1. GoDaddy DNS . revert the `@` record to the original Softr IP
2. Wait 5-10 min (low TTL) . Softr site is back
3. Diagnose, fix, redeploy on Cloudflare Pages, cutover again

## Ongoing maintenance

- Content changes = edit files in `web/src/data/panels.json` (or the page files) . `git push` . Cloudflare Pages auto-deploys in ~1-2 min
- Image swaps = drop new JPG into `web/public/images/panels/` with the exact same filename . see `IMAGE-MAPPING.md`
- New blog posts (Phase 2): create MDX file under `web/src/pages/blog/` . propagates automatically

## Hosting cost

- Cloudflare Pages: free tier (unlimited bandwidth, 500 builds/month) comfortably covers this site
- Web3Forms: free (unlimited on personal plan)
- Plausible: free 30-day trial, then $9/mo. Alternative: GA4 (free but heavier + privacy tradeoffs)
- GoDaddy: no change . domain fee only
- **Total: $0-$9/mo** vs current Softr subscription

## Note

`web/vercel.json` is leftover from the earlier Vercel plan and is now unused (Cloudflare Pages ignores it). Harmless to keep, safe to delete whenever.
