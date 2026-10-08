# AM Electricals — Image Mapping Guide

How to control which image renders where on the site.

## 1. Where images live

Two folders, two jobs:

| Folder | What it is | Public URL |
|---|---|---|
| `01-assets/panels/` | Source library (you drop originals here, any name) | Not served |
| `web/public/images/panels/` | Live site copies (kebab-case, exact name) | `/images/panels/<file>` |

Files in `web/public/` are served as-is at the root path. So `web/public/images/panels/apfc.jpg` is served at `https://amelectricals.co.in/images/panels/apfc.jpg`.

## 2. Which image renders where

### Home page (`web/src/pages/index.astro`)

Two images are hard-coded in the page:

- **Hero image** (right side, top of page):
  ```
  src="/images/panels/hero-mcc.jpg"
  ```
- **Founder / workshop image** (editorial split, middle of page):
  ```
  src="/images/panels/founder-workshop.jpg"
  ```

To swap: drop your new photo into `web/public/images/panels/` with that same filename, or edit the `src=` string on the page.

### Panel detail pages (auto-driven by `web/src/data/panels.json`)

Every one of the 13 panel pages picks its hero image from `panels.json`. Look for the `image` field on each panel:

```json
{
  "slug": "apfc-panel-manufacturer-kolkata",
  "name": "APFC Panels",
  "image": "/images/panels/apfc.jpg",
  ...
}
```

Change `image` to any path under `web/public/`. Empty string = falls back to a picsum placeholder.

### Panel cards (grid on Home + `/panels/`)

Same source. `PanelCard` component reads `image` from `panels.json`. Change once in the JSON, propagates to every card everywhere.

### About page (`web/src/pages/about.astro`)

- **Workshop image** (right side of hero):
  ```
  src="/images/panels/founder-workshop.jpg"
  ```

## 3. How to swap an image (3 recipes)

### Recipe A: replace an existing panel photo
```bash
# From project root, replace the served copy
cp "01-assets/panels/my-new-apfc-shot.jpg" "web/public/images/panels/apfc.jpg"
```
Save, refresh browser. Done. No code changes needed.

### Recipe B: add a brand new photo + wire it
1. Drop the file: `web/public/images/panels/factory-floor-01.jpg`
2. In `web/src/data/panels.json`, edit the `image` field of the panel you want it on:
   ```json
   "image": "/images/panels/factory-floor-01.jpg"
   ```
3. Save. Astro dev server auto-reloads.

### Recipe C: change the home hero image
Open `web/src/pages/index.astro`, find the block:
```astro
<img
  src="/images/panels/hero-mcc.jpg"
  alt="AM Electricals MCC panel on the Kolkata shopfloor"
  ...
/>
```
Change `src` to any path under `/images/panels/` (or wherever you drop the file under `web/public/`).

## 4. Full current mapping

| Where | File | Panel |
|---|---|---|
| Home hero | `/images/panels/hero-mcc.jpg` | MCC (front-view) |
| Home founder split | `/images/panels/founder-workshop.jpg` | Panel row |
| About workshop | `/images/panels/founder-workshop.jpg` | Panel row |
| Panel: APFC | `/images/panels/apfc.jpg` | APFC control panel |
| Panel: MCC | `/images/panels/mcc.jpg` | MCC panel 2 |
| Panel: PCC | `/images/panels/pcc.jpg` | PCC main |
| Panel: AMF & DG Sync | `/images/panels/amf-dg-sync.jpg` | DG-Synchronising panel |
| Panel: PLC | `/images/panels/plc.jpg` | PLC panel |
| Panel: HVAC | `/images/panels/hvac.jpg` | HVAC panel 2 |
| Panel: AHU & Metering | `/images/panels/ahu.jpg` | AHU control panel 220 |
| Panel: Control Desks | `/images/panels/control-desk.jpg` | Electrical control desk |
| Panel: DG Control | `/images/panels/dg-control.jpg` | DG-set control panel |
| Panel: Fire Alarm | `/images/panels/fire-alarm.jpg` | Fire Panel 2 |
| Panel: PDB | `/images/panels/pdb.jpg` | Distribution panel |
| Panel: STP/ETP/WTP | `/images/panels/stp-etp-wtp.jpg` | ETP panel 1 |
| Panel: Custom | `/images/panels/custom.jpg` | Material handling panel |

## 5. Image spec (for best rendering)

- **Format:** JPG (widely compatible) or WebP (smaller, better)
- **Aspect ratio:** portrait 4:5 for hero + panel detail, 4:3 for panel cards. Original photos work — CSS crops with `object-fit: cover`
- **Resolution:** at least 1200px on the long edge. Higher is fine
- **Weight:** aim <300KB per file after optimization. Use TinyPNG / Squoosh before uploading
- **Alt text:** every `<img>` on the site has an `alt=` string. Edit it in the same place you edit the src — it matters for SEO and accessibility

## 6. Missing image = broken card

If the `image` path doesn't exist under `web/public/`, browsers show a broken-image icon. Fixes:
- Set `image` to `""` in `panels.json` (empty string) → PanelCard falls back to picsum placeholder
- Or drop a real photo at the exact path

## 7. Adding logo, factory, cert scans

Same rules apply. Recommended structure:
```
web/public/
├── images/
│   ├── panels/       ← done
│   ├── factory/      ← drop shop-floor photos here
│   ├── clients/      ← client logos (SVG preferred)
│   └── certificates/ ← CPRI + ISO scans (JPG or PDF)
└── logo/             ← brand logo SVG here (referenced from Header.astro)
```

Logo swap:
1. Save your logo as `web/public/logo/am-electricals.svg`
2. Open `web/src/components/Header.astro` and replace the "AM" text block with an `<img src="/logo/am-electricals.svg" ... />` tag

## 8. Change WITHOUT touching code (once site is live)

If you want a non-technical way to swap images later, options are:
- **Simplest:** Ask me (or any dev) to do batch swaps.
- **Better:** Move image references to a small CMS (Sanity, Contentful free tier, or a headless option like Storyblok). Deferred to Phase 7.

For now, direct file replacement is the fastest workflow.
