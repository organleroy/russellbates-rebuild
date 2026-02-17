# PROJECT CONTEXT — russellbates.com (Eleventy rebuild)

## Purpose

Rebuild **russellbates.com** as a **fast, static Eleventy (11ty) site** hosted on **GitHub Pages**, matching the old WordPress site’s look precisely (typography, spacing, header width vs grid width, thumbnail behavior), with incremental, controlled improvements.

This project strongly favors **CSS-only solutions** whenever possible. JavaScript is avoided for layout and rendering behavior; a small local-only tool is used for homepage curation/export (see below).

---

## Non-negotiables (Read First)

- **Never edit `_site/`** — it is build output and overwritten every build.
- **Edit only under `src/`.**
- **Global styling single source of truth:** `src/assets/css/site.css`
- Prefer **CSS-only** changes. No JS for layout/image behavior.
- Prefer **full-file replacements** over partial diffs.
- **Header, grid, and footer widths must match** (no full-bleed header bar).
- Preserve the existing typography system (Montserrat + Open Sans) and the restrained, clean editorial feel.

---

## If Something Breaks, Check Here First

Before assuming a bug or Eleventy issue, check these common causes:

1. **Was a file edited inside `_site/`?**  
   - `_site/` is generated output and overwritten on every build.  
   - Any edits there will disappear.  
   - All real changes must be made under `src/`.

2. **Did header, grid, or footer widths stop matching?**  
   - These must always align via the shared inner max-width math.  
   - Look for accidental changes to:
     - `--max`
     - `--gutter`
     - `.site-header-inner`, `.site-footer-inner`, or grid containers.

3. **Are homepage “outlier” thumbnails pillarboxing again?**  
   - The CSS solution depends on `.card.is-outlier` being applied correctly.
   - Homepage outlier detection uses:
     - `thumbMeta.isOutlier` when available, AND
     - a filename heuristic fallback (standard thumbs include `-500x350`; others treated as outliers).
   - If pillarboxing returns, check the homepage template logic in `src/index.njk`.

4. **Are thumbnail overlays or hover states broken?**  
   - Check that spacing or positioning changes didn’t affect:
     - `.card-meta`
     - overlay positioning
     - hover darkening logic.

5. **Are Featured Work thumbnails missing on project pages?**  
   - Confirm that `projectBySlug` still exists in Eleventy’s global data context.
   - Featured thumbnails depend on this lookup.

6. **Is the contact form not submitting or not writing to Google Sheets?**  
   - Apps Script changes require:
     - Deploy → Manage deployments → Edit → New version → Deploy
   - Temporarily remove the hidden iframe + redirect to see script output.

7. **Is spam suddenly getting through (or legit submissions disappearing)?**  
   - Check that the honeypot field (`company`) still exists in the form markup.
   - Confirm `.hp-field` is hidden via CSS but present in the DOM.

8. **Does something look “off” after spacing tweaks?**  
   - Recheck recent changes to:
     - `.site-main` padding
     - negative margins (e.g. About page tightening)
   - Small spacing changes can cascade visually.

If a problem persists after these checks, review recent commits and consult `CHANGELOG.md` before changing behavior.

---

## Stack / Repo / Hosting

- Static generator: **Eleventy (11ty)**
- Repo: `organleroy/russellbates-rebuild`
- Hosting: **GitHub Pages** via **GitHub Actions**
- Local dev:
  - From project root: `npm run dev`
  - Site served at: `http://localhost:8080`

---

## Project Structure (Key Files)

### CSS / Layout
- Global CSS: `src/assets/css/site.css`
- Base layout: `src/_includes/base.njk`
- Homepage (Work): `src/index.njk`

### Content / Data
- Main portfolio data: `src/content/projects.json`
- Data loader & normalization: `src/_data/projects.cjs`
- Homepage ordering data: `src/_data/home.json`

### Tools (Local-only)

- Homepage curator tool: `tools/home-curator.html`
  - Allows drag-and-drop reordering of homepage projects as a **text-only “note card” list**
  - Exports the **first 39 slugs only** into `src/_data/home.json`
  - Mirrors the old WordPress admin ordering experience
  - **This file is intentionally committed to the repo**
    - It documents editorial intent
    - It allows future maintainers (or future-you) to understand and reuse the curation workflow
    - It does **not** ship to production or affect runtime behavior

### Templates / Pages
- Project pages: `src/work/project.njk` → `/work/{{ slug }}/`
- About / Contact: `src/about.njk`
- Thanks page: `src/thanks.njk`

---

## Data Model (`projects.json`)

All projects — homepage items and bench projects — use the **same unified schema**.

Each project includes:
- `title`  
  - Stored as: `Brand "Project Title"`
- `slug`
- `thumb`
- `vimeo_id`
- `subtitle` (string; may be empty)
- `agency` (string; may be empty)
- `featured_slugs` (array of 4 slugs)
- `featured_home` (boolean; informational only)

### Derived fields (via `projects.cjs`)
- `brand` → parsed from `title`
- `spot` → parsed from `title`
- `spotQuoted` → convenience quoted string of `spot`
- Compatibility aliases:
  - `subhed` → `subtitle`
  - `blurb` → `agency`

**Important:**  
Canonical fields are `subtitle` and `agency`. Compatibility aliases exist only to prevent regressions in templates.

---

## Homepage (“Work”) Page

### Ordering & Curation
- Homepage ordering is controlled by `src/_data/home.json`
- The file contains an ordered list of slugs representing **visual flow**
- Only the **first 39 slugs** are rendered on the homepage
- Bench projects remain untouched until explicitly promoted

### Grid behavior
- Desktop: **3 columns × 13 rows (39 items)**
- Responsive: 3 → 2 → 1 column
- Gap: **10px**
- Aspect ratio: **10:7**

### Thumbnail image behavior
- Default: `object-fit: contain`
- Outliers: `.card.is-outlier { object-fit: cover }`
- Homepage outlier detection:
  - uses `thumbMeta.isOutlier` when present
  - otherwise treats any thumb not containing `-500x350` as an outlier

### Thumbnail text
- Brand: ALL CAPS (Montserrat)
- Title: ALL CAPS, quoted
- Line 3 behavior on homepage:
  - If `subtitle` / `subhed` is present → show it
  - Else if `agency` is present → show agency
  - Else show nothing

---

## Header (Critical Design Match)

- Header is **not full-bleed**
- Black bar width exactly matches grid width
- Achieved via:
  - `.site-header-inner { max-width: calc(var(--max) - (var(--gutter) * 2)); }`

Typography:
- Name: Open Sans, 30px, orange `#ff5a01`, uppercase
- Role: Open Sans, 18px, white, uppercase
- Nav: Montserrat, 14px, uppercase

Responsive breakpoint: ~760px

---

## Footer

- Text-only footer (matches old site)
- Width matches header and grid
- Black inner panel using `.site-footer-inner`
- Spacing tuned to sit tightly under the grid

---

## Individual Project Pages (`/work/<slug>/`)

Template: `src/work/project.njk`

### Title above video
- Line 1: Brand (ALL CAPS)
- Line 2: Spot title (ALL CAPS, quoted)
- Both lines same size, centered

### Credits under video
- Left-aligned
- Displays (no duplication; order preserved):
  - `subtitle` (preferred)
  - `agency` (preferred)
  - fallback to `blurb` only if `agency` is missing (compat)
  - de-duplication guard prevents identical strings printing twice

### Featured Work strip
- Header row:
  - “FEATURED WORK” (left)
  - “MORE >” (right, same color)
- Uses `featured_slugs`
- Requires `projectBySlug` lookup
- Featured thumbnail line-3 remains subtitle-only (no agency fallback)

---

## About / Contact Page

Source: `src/about.njk`

- Bio text from original WordPress site
- Lead paragraph styled via `.about-lead`
- Contact form posts to Google Apps Script
- Hidden iframe submission + `/thanks/` redirect

### Honeypot
- Field name: `company`
- Hidden via `.hp-field`
- Apps Script ignores submissions where `company` is filled

---

## Thanks Page

Source: `src/thanks.njk`

- Confirmation message
- CTA links back to `/`

---

## CSS Notes

- Single source of truth: `src/assets/css/site.css`
- Variables defined in `:root`
- Spacing carefully tuned; small changes can cascade
- Be cautious adjusting:
  - `.site-main`
  - `.card-meta`
  - header/footer inner widths

---

## Workflow

Local:
1. Edit files under `src/`
2. Run `npm run dev`
3. Check `http://localhost:8080`

Deploy:
1. `git commit`
2. `git push`
3. GitHub Actions builds and deploys automatically

---

## Current Status (Baseline)

- Homepage grid stable, ordered, polished
- Homepage subtitle → agency fallback implemented
- Homepage outlier heuristic prevents pillarboxing regressions
- Project pages correctly formatted and credited
- About/Contact page working with spam protection
- Footer restored and aligned
- Data schema unified and consistent (`subtitle` + `agency`)