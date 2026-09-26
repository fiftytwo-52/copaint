# coPaint — Fixes Guide (SEO + Mobile Nav + Icons)

**For the agent:** This is a self-contained task list. Do every task in order. Nothing is "done"
until its stated check passes. Work in the Astro source (`src/`), rebuild, redeploy to
Cloudflare Pages, then verify each fix on the LIVE site — not just in the build output.

## Site structure (read first — it shapes the SEO decisions)

- `/` = the paint canvas app. **This is the first page that loads.** Kid-simple UX is the priority
  here: no visible marketing text, no clutter. Its H1 is intentionally screen-reader-only.
- `/home/` = the marketing homepage. Opened by tapping the **(i) info button** in the app
  (above the A4 page indicator). This page is the SEO workhorse: titles, headings, FAQ schema,
  share content all live here.
- Rule: never add visible text/marketing blocks to `/`. All SEO content work happens on `/home/`
  plus `<head>` tags on both pages.

## PART A — What to fix and why

### A1. SEO (from live audit 2026-09-27)
1. **Titles too long** — `/home/` title is 77 chars (truncates in Google), `/` is 64 (borderline).
   Keep ≤ 60 displayable characters.
2. **Canonical mismatch** — `/home/` is served with a trailing slash but its canonical tag says
   `https://copaint-qxc.pages.dev/home` (no slash); the sitemap also lists the slashless URL.
   One policy everywhere, or crawlers see two URLs for one page.
3. **Thin H1 on `/home/`** — the page's only H1 is the bare word "coPaint". It must carry keywords.
4. **Meta keywords stuffing** — `/` has a ~60-phrase `meta name="keywords"` block. Google ignores
   it; it looks sloppy. Delete it.
5. **Viewport blocks zoom** — `maximum-scale=1.0, user-scalable=no`. Accessibility/mobile-usability
   ding. Allow zooming.
6. **No apple-touch-icon** — iOS/Safari bookmarks get no icon. Add a 180×180 PNG.
7. **Hardcoded domain** — canonicals/OG tags hardcode `https://copaint-qxc.pages.dev`. The site
   will move to a custom domain later: centralize the site URL in ONE config constant now so the
   move is a one-line change.

### A2. Mobile nav
The `/home/` sticky pill nav (logo + Features, Guides, FAQ, About, Contact, Privacy, Share +
"Start Drawing" CTA) is horizontally scrollable on phones — cramped and easy to miss. Replace
with a proper mobile menu below ~720px: logo + CTA stay visible, links collapse into a hamburger.

### A3. Icons
Audit every toolbar icon in the app (pencil, brush, eraser, shapes, stickers, text, bucket, line,
arrow, select, undo/redo, download, collab, etc.) at real size. House style: minimal monochrome
line icons on a white surface, consistent stroke width. Redraw/replace only the weak ones —
recognizable at 24px, consistent with the set.

### A4. Copy + suspected bug
- Features card says "17 shapes", footer says "18 Vector Shapes" — verify the true count in code,
  use it everywhere.
- Possible canvas-restore quirk (seen once): after navigating to `/home/` and back, the canvas
  appeared blank while Undo stayed enabled. Investigate autosave/history vs rendered bitmap sync.

---

## PART B — AGENT TASK LIST

### TASK-01: Trim both `<title>` tags to ≤ 60 characters
**Do:** In `src/layouts/SiteLayout.astro` (or wherever titles are set):
- `/` → `coPaint — Free Online Paint & Whiteboard App` (44 chars)
- `/home/` → `coPaint — Free Online Whiteboard & Paint App` (46 chars)
Keep them unique per page; keep the em-dash style.
**Done when:** view-source on both live pages shows the new titles; each ≤ 60 chars.

### TASK-02: One canonical URL policy + centralize the domain
**Do:**
1. Decide: **no trailing slash** (`/home`, not `/home/`). Apply everywhere: the canonical tag on
   `/home/`, the `(i)` info button link in the app, the "Start Drawing"/nav links, and
   `sitemap.xml` (which must list `https://copaint-qxc.pages.dev/` and
   `https://copaint-qxc.pages.dev/home` — exactly these two, no variants).
2. Move the site URL (`https://copaint-qxc.pages.dev`) into a single config constant
   (e.g. `src/config.ts` → `SITE_URL`) and build canonical, `og:url`, `og:image`, sitemap, and
   `robots.txt` Sitemap line from it. No hardcoded domain strings left in layouts/pages.
**Done when:** canonical on live `/home` === the URL in the address bar === the sitemap entry;
`grep -r "copaint-qxc.pages.dev" src/` returns zero hits outside the config file.

### TASK-03: Keyword-bearing H1 on `/home/`
**Do:** The hero H1 currently reads just "coPaint". Change to
`coPaint — Free Online Paint & Collaborative Whiteboard`, styled so "coPaint" stays the visual
hero and the descriptor reads as a natural subline (keep the existing rainbow bar/gradient design
intact). Keep exactly one H1 on the page; leave the H2/H3 structure untouched.
**Done when:** live `/home` source shows the new H1 text; page still has exactly one H1;
visual hero looks unchanged apart from the added descriptor line.

### TASK-04: Delete the meta keywords block
**Do:** Remove the entire `<meta name="keywords" …>` tag (~60 phrases) from the `/` page head.
Do not replace it with anything.
**Done when:** `view-source:https://copaint-qxc.pages.dev/` contains no `name="keywords"`.

### TASK-05: Allow pinch-zoom (viewport fix)
**Do:** Change the viewport meta on both pages to
`<meta name="viewport" content="width=device-width, initial-scale=1">`
— drop `maximum-scale=1.0, user-scalable=no`. Verify the canvas UI still works with touch zoom
(pinching the page must not break drawing; the app's own zoom slider is unaffected).
**Done when:** view-source on both live pages shows the new viewport; manual phone-viewport test:
pinch-zoom works, drawing still works.

### TASK-06: Add apple-touch-icon
**Do:** Generate a 180×180 PNG from the existing brush-mark logo (rounded-square, same artwork as
the SVG favicon) at `public/apple-touch-icon.png`; add
`<link rel="apple-touch-icon" href="/apple-touch-icon.png">` to the layout head. Keep the
existing SVG favicon as-is.
**Done when:** `https://copaint-qxc.pages.dev/apple-touch-icon.png` loads (180×180); link tag
present in view-source on both pages.

### TASK-07: Mobile nav — hamburger menu below ~720px
**Do:** On `/home/` (and any shared header):
1. At viewport widths below ~720px, collapse the nav links (Features, Guides, FAQ, About,
   Contact, Privacy, Share) into a hamburger button. Logo (left) and "Start Drawing" CTA (right)
   stay visible in the bar.
2. Tapping hamburger opens a dropdown panel with the same anchor links; tapping a link
   smooth-scrolls to the section (preserve existing smooth-scroll JS) and closes the panel.
3. Accessible: `aria-expanded` on the button, `Esc` closes, focus moves sanely, panel is
   keyboard-navigable. No layout shift when opening/closing; no horizontal page scroll at 360px.
4. Desktop (≥721px) keeps the current pill nav unchanged.
**Done when:** at 360×740 viewport the bar shows logo + hamburger + CTA, no clipped links;
menu opens/closes, links smooth-scroll and land on the right sections; at 1280px the full pill
nav renders as before; zero horizontal overflow on mobile.

### TASK-08: Icon audit — refresh only the weak icons
**Do:**
1. Screenshot each toolbar icon at its real rendered size (24–40px) on the `/` app page:
   pencil, brush, highlighter, eraser, bucket, line, arrow, shapes, stickers, text, add-picture,
   select, pan, area-select, undo, redo, trash, download, export, classroom, zoom, info (i), A4.
2. Judge each against the house style: minimal monochrome line icon, consistent stroke width
   with the set, instantly recognizable at small size, no blurriness.
3. Redraw/replace ONLY the ones that fail (as inline SVG, same stroke system as the good ones).
   Do not restyle the whole set; do not change working icons' appearance or positions.
**Done when:** a short audit list exists (icon → pass/fail + reason); every failed icon is replaced
and re-screenshotted passing; the toolbar looks visually unchanged except for the fixed icons.

### TASK-09: Fix the shape-count inconsistency
**Do:** Count the actual shapes offered in the shapes popover in code. Update BOTH the "Features"
card ("17 shapes") and the footer ("18 Vector Shapes") — and the `/home/` meta description if it
mentions a count — to the true number.
**Done when:** `grep -ri "17 shapes\|18.*shapes" src/` shows one consistent number everywhere.

### TASK-10: Investigate the canvas-restore quirk
**Do:** Reproduce: draw a stroke → navigate to `/home/` → back to `/`. Check whether the canvas
bitmap ever renders blank while history/Undo still holds the stroke. If reproducible, fix the
autosave → re-render sync (render must reflect the saved state before history controls enable).
If NOT reproducible after 5 tries, note it as unreproduced and move on — do not refactor blindly.
**Done when:** written note: reproduced (with fix + retest) or unreproduced after 5 attempts.

### TASK-11: Re-verify live and report
**Do:** Redeploy, then on the LIVE site confirm: TASK-01–09 checks pass in view-source and at a
360px viewport; `/` still opens straight into the canvas with zero visible marketing text;
the `(i)` button still opens `/home`; drawing, popovers, and collab room create/join still work
(quick smoke test only).
**Done when:** every task's "Done when" holds on the live deployment.

---

## Completion report
For each TASK-01…TASK-11 reply: **DONE** (1-line evidence), **PARTIAL** (what's missing), or
**BLOCKED** (reason + what you need). Then list any deviations from this guide and why.
