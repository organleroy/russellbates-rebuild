# CHANGELOG — russellbates.com

This file records **design, data-model, and architectural decisions**
that are not obvious from the code alone.

It is intentionally **high-level, editorial, and human-readable**.
This is not a commit log.

---

## 2026-02-15 — Baseline Established

### Homepage Curation & Ordering
- Replaced WordPress drag-and-drop homepage ordering with a **slug-based curation system**.
- Homepage order is now defined by `src/_data/home.json`, containing an ordered list of project slugs.
- Only the **first 39 slugs** are rendered on the Home / Work page (13 × 3 grid).
- Bench projects remain untouched until explicitly promoted.

#### Editorial workflow
- Added a local-only curator tool: `tools/home-curator.html`
- Tool provides a **text-only “note card” list** of homepage projects that can be reordered visually.
- Export function writes the first 39 slugs into `home.json`.
- Tool is **committed to the repo intentionally** to document editorial intent and enable future reuse.
- Tool does not ship to production and has no runtime impact.

---

### Data Model Unification
- Standardized **all projects** (homepage + bench) on a single schema in `projects.json`.
- Canonical fields are now:
  - `subtitle` → descriptive line (e.g. “starring…”)
  - `agency` → agency / production credit
- Removed ambiguity around legacy `blurb` usage.
- Ensured every project includes:
  - `subtitle` (string, may be empty)
  - `agency` (string, may be empty)

#### Compatibility handling
- `projects.cjs` provides **compatibility aliases**:
  - `subhed` → `subtitle`
  - `blurb` → `agency`
- Aliases exist only to prevent regressions in templates.
- New work should **never** introduce `blurb` again.

---

### Title Parsing & Normalization
- Project titles remain stored as:  
  `Brand "Spot Title"`
- `projects.cjs` now reliably parses:
  - `brand`
  - `spot`
  - supports straight and curly quotes
- Prevented double-brand rendering on thumbnails and project pages.
- All titles display as:
  - Line 1: Brand (ALL CAPS)
  - Line 2: Quoted spot title (ALL CAPS)

---

### Homepage Thumbnail Rules
- Grid locked to **39 items max**, CSS-only.
- Thumbnail behavior:
  - Default: `object-fit: contain`
  - Outliers: `object-fit: cover`
- Outlier detection uses:
  - `thumbMeta.isOutlier` when present
  - filename heuristic fallback (standard thumbs include `-500x350`)
- This prevents pillarboxing regressions without JS.

#### Thumbnail text logic (homepage only)
- Line 1: Brand
- Line 2: Quoted title
- Line 3:
  - Show `subtitle` if present
  - Else show `agency`
  - Else show nothing

(Featured Work thumbnails intentionally **do not** use this fallback.)

---

### Project Pages (`/work/<slug>/`)
- Title above video:
  - Two-line, centered, equal weight
  - Brand (line 1) + quoted spot (line 2)
- Credits under video:
  - Left-aligned
  - Displays `subtitle` then `agency`
  - Fallback to `blurb` only if `agency` missing
  - De-duplication guard prevents repeated lines
- Featured Work strip:
  - Header row restored: “FEATURED WORK” + “MORE >”
  - Both use same color and weight
  - Depends on `projectBySlug` global data

---

### About / Contact
- Added subtle lead-paragraph treatment for stronger editorial opening.
- Refined column balance: bio slightly wider than contact form.
- Implemented on-site contact form using **Google Sheets + Apps Script** (no paid services).
- Added honeypot spam protection (`company` field) and verified behavior.
- Styled `/thanks/` confirmation page with warm messaging and “VIEW WORK →” CTA.

---

### Layout / Design System
- Tightened vertical rhythm:
  - Header → content
  - Content → footer
- Reconfirmed non-negotiable rule:
  - Header, grid, and footer **inner widths must always match**
  - No full-bleed black header bar
- All layout decisions remain CSS-only.

---

## 2026-02-10

### Data / Templates
- Fixed missing Featured Work thumbnails by restoring `projectBySlug` in Eleventy global data.
- Standardized project title formatting across homepage and project pages.

---

## 2026-02-08

### Architecture
- Migrated site from WordPress to static Eleventy (11ty).
- Established `src/` as the only editable source.
- Treated `_site/` as disposable build output.
- Deployed via GitHub Pages + GitHub Actions.

---

## Notes for Future Changes

- If homepage order needs changing: update `home.json` (preferably via curator tool).
- If credits look wrong: check `subtitle` vs `agency` before touching templates.
- If thumbnails pillarbox again: inspect outlier detection before changing CSS.
- If something feels “off” visually, review spacing changes carefully — small CSS tweaks cascade.