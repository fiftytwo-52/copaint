# coPaint 🎨

**A free, friendly drawing app made for kids and classrooms. No accounts — just open and create.**

🌐 **Live app:** https://copaint-qxc.pages.dev · 📖 **About / Guides / FAQ:** https://copaint-qxc.pages.dev/home

coPaint is a zero-friction drawing app for young artists: big buttons, friendly tools, zero clutter. It runs entirely in the browser as a fully static site, autosaves to the device, and can bring a whole class together in realtime rooms — with classroom controls for the teacher. Nothing is uploaded anywhere, no sign-up required.

---

## ✨ Features

### 🖌️ 14 drawing tools

| Tool | Shortcut | What it does |
|---|---|---|
| Select | `S` | Select, move, resize, rotate and delete placed objects |
| Pencil | `P` | Crisp freehand drawing |
| Brush | `B` | 11 brush styles: round, marker, calligraphy, spray, crayon, neon, dots, rainbow, taper, sketch, chalk |
| Highlighter | `H` | Translucent highlight strokes |
| Eraser | `E` | Erase strokes |
| Bucket fill | `G` | Flood-fill any enclosed area with 9 fill styles |
| Line | `L` | Straight lines with editable styles |
| Arrow | `A` | Arrows with editable styles |
| Shapes | `O` | 18 shapes: circle, rect, sharp-rect, triangle, diamond, pentagon, hexagon, plus, crescent, trapezoid, block-arrow, chevron, parallelogram, octagon, semicircle, pie, star, heart |
| Text | `T` | 5 fonts, color, optional background color, move/resize/rotate |
| Sticker | — | 36 vector stickers · 558 color emojis · 88 coloring-book outlines |
| Image | — | Insert a picture from the device |
| Area select | — | Lasso an area to copy or download just that part |
| Move / pan | `M` | Drag the canvas around |

Every tool has adjustable **size, color, opacity** (and line style/dash where it applies). Shapes, text, stickers and outlines **stay selected after you place them** — drag to move, handles to resize/rotate, tap anywhere else to finish.

### 📄 Paper & patterns
- Colored paper plus **5 patterns**: plain, ruled, graph grid, dots, numbered
- **9 fill styles** for shapes and bucket fill: solid, hatch, dots, grid, zigzag, waves, checker, stars, hearts
- Toggleable **A4 print-area guide** for printing on real paper

### 🔍 View
- Zoom slider **25% – 400%** (double-click to reset), zoom in/out buttons
- Undo / redo with `Ctrl/⌘+Z` and `Ctrl/⌘+Y` (or `Ctrl/⌘+Shift+Z`)
- Area-select toolbar: **copy area as image** or **download clipped image**

### 💾 Save & export
- **Autosave** to the browser's local storage as you work — close the tab, come back later
- One-tap **PNG export** and **PDF export** (only pages that actually contain artwork are included)
- Works fully **offline** — only collaboration rooms need internet

### 🌐 Realtime collaboration (rooms)
- **Create a room** and share a random **5-letter code**, optionally **password-protected**
- **Creator mode** — everyone gets their own canvas; the creator watches every student's canvas live, with a hi-res enlarged view
- **Open mode** — everyone draws together on one shared canvas
- The creator can **draw directly on a student's canvas** (pencil, brushes, shapes, text, stickers, fill) and afterwards **select, move, resize, re-edit or delete** what they drew — with instant sync both ways
- **Classroom controls**: pause a student's drawing, remove them from the room, "send my canvas to all", request everyone's pages and **download the whole class's work as one PDF**
- **Friends list** — see who's in the room; students can watch a friend's canvas view-only
- **Live connection status** ("Connecting… 1/3") with automatic **failover across 3 public MQTT brokers** (EMQX, HiveMQ, Mosquitto), automatic reconnection, and same-broker retry before hopping

### 📱 Mobile friendly
- On phones the toolbar becomes a **slim collapsible left rail** and the room bar / teacher panel can be **dragged and folded**
- Popovers scroll instead of clipping; touch-friendly targets
- A dismissible *"coPaint works better on PC"* notice (remembered once closed)

### 🔒 Privacy first
- **No accounts, no tracking, no personal data**
- Drawings live only in your browser's local storage — never uploaded
- In rooms, only strokes + a chosen display name travel through a public message service, only while you're in the room
- Room codes are random; use a password to keep a room private
- See the full [privacy policy on the site](https://copaint-qxc.pages.dev/home#hpPrivacy)

---

## 🚀 Getting started

### Prerequisites
- **Node.js** 18.17+ (developed on Node 22)
- **npm** 9+

### Install & run

```bash
git clone https://github.com/fiftytwo-52/copaint.git
cd copaint
npm install
npm run dev
```

The dev server starts at **http://localhost:4321/** (the paint app at `/`, the info page at `/home`).

### Scripts

| Command | What it does |
|---|---|
| `npm run dev` | Start the Astro dev server with hot reload |
| `npm run build` | Build the static site into `dist/` |
| `npm run preview` | Preview the production build locally |
| `npm run deploy` | Build and deploy directly to Cloudflare Pages |

---

## 🏗️ Tech stack

- **[Astro 7](https://astro.build)** — static site generator (`output: 'static'`), the only npm dependency
- **Vanilla HTML / CSS / JavaScript** — the whole paint app is a single self-contained page (`src/pages/index.astro`, ~5,000 lines) with no UI framework and no canvas library
- **Canvas 2D API** for all rendering; images export via `toDataURL`
- **MQTT over WebSocket** (raw, protocol-first implementation) for realtime rooms over public brokers — no backend server
- **localStorage** for autosave and settings persistence
- Deployed as static files on **Cloudflare Pages**

---

## 📁 Project structure

```
copaint/
├── astro.config.mjs          # Astro config (static output)
├── package.json              # scripts + single dependency (astro)
├── src/
│   ├── pages/
│   │   ├── index.astro       # 🎨 the entire paint app (UI + styles + JS)
│   │   └── home.astro        # 📖 landing page: features, guides, FAQ, privacy
│   ├── layouts/
│   │   └── SiteLayout.astro  # shared shell (head, meta, favicon)
│   ├── components/homepage/  # landing-page sections
│   │   ├── Nav.astro  Hero.astro  Features.astro  Guides.astro
│   │   ├── Faq.astro  About.astro  Privacy.astro  Contact.astro  Footer.astro
│   └── styles/
│       └── homepage.css      # landing-page styles
├── public/
│   └── outlines/             # 88 coloring-book outlines (512px, transparent PNGs)
├── outline-src/              # outline sources + generated contact sheet
├── process_outlines.py       # regenerates outline PNGs (transparency + resize)
├── build_single.py           # optional: builds standalone offline HTML files
└── dist/                     # build output (git-ignored)
```

---

## ⌨️ Keyboard shortcuts

| Key | Action |
|---|---|
| `Ctrl`/`⌘` + `Z` | Undo |
| `Ctrl`/`⌘` + `Y` or `Ctrl`/`⌘` + `Shift` + `Z` | Redo |
| `P` | Pencil |
| `B` | Brush |
| `H` | Highlighter |
| `E` | Eraser |
| `G` | Paint bucket fill |
| `L` | Line tool |
| `A` | Arrow tool |
| `O` | Shapes |
| `T` | Text tool |
| `S` | Select tool |
| `M` | Move / pan the canvas |
| `Delete` / `Backspace` | Delete the selected drawing |
| `Esc` | Cancel placing / deselect |

---

## 🏫 How collaboration works

1. **Create** — Tap the people button → *Create room* (optionally set a password). You get a random 5-letter code.
2. **Join** — Friends tap the same button, enter the code (+ password) and join. No accounts needed.
3. **Pick a mode**
   - **Creator mode** — each collaborator draws on their own canvas; live previews stream to the creator, who can watch, zoom in, draw on anyone's canvas, pause or remove them.
   - **Open mode** — everyone draws together on one shared canvas in realtime.
4. **Collect work** — The creator can request every canvas and download the whole class's work as a single **PDF**.

**Safety for classrooms:** random codes, optional passwords, and the creator can pause or kick anyone at any time.

### Under the hood
Rooms run over **MQTT topics** (`kp1/room/<CODE>/…`) on public WebSocket brokers with automatic failover between three providers. Stroke items, canvas previews, presence (hello/join/leave), moderation (pause/kick/end) and teacher overlays (`t-draw`, `t-update`, `t-del`, `t-fill`) all travel as small JSON/binary messages — there is **no application server and no database**.

---

## 🚢 Deployment

The site is fully static — deploy `dist/` to any static host.

**Cloudflare Pages** (current production):

```bash
npm run deploy
```

Or manually:

```bash
npm run build
npx --yes wrangler@4 pages deploy dist --project-name=copaint --branch=main
```

Or connect the GitHub repo in the Cloudflare dashboard with build command `npm run build` and output directory `dist` for automatic deploys on every push.

---

## 🛠️ Helper scripts

| Script | Purpose |
|---|---|
| `process_outlines.py` | Turns generated outline images into `outline-src/final/outline-<id>.png` (max 512px, white → transparent) |
| `build_single.py` | Builds standalone offline HTML files: inlines CSS/JS and embeds all outline images as base64, producing `kids-paint.html` + `kids-paint-home.html` |

---

## ❓ FAQ (short version)

| | |
|---|---|
| **Is coPaint free?** | Yes — completely free, no accounts, no sign-up. |
| **Where are drawings saved?** | Only in your browser on your device. Never uploaded. |
| **Does it work offline?** | Drawing, saving and exporting do. Rooms need internet. |
| **Can I print?** | Yes — turn on the A4 guide, then export PNG or PDF and print. |

More answers on the [info page](https://copaint-qxc.pages.dev/home#hpFaq).

---

## 📬 Contact

Questions, ideas or found a bug? [Get in touch](mailto:gun.yes@proton.me) — we'd love to hear from you.

## 📄 License

Free for kids, parents and schools to use and share. ISC license — see [`package.json`](package.json).
