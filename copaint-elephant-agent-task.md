# TASK: Add Twin the elephant peeking mascot to coPaint

## Goal
Add an animated elephant mascot ("Twin") that peeks in from the right edge of the page.
Same character and behavior as the approved preview: cute blue style, dot eyes, small tusks,
pink inner ears, blush cheeks — no crown, no ornaments, peeking head only (never full body).

## Behavior spec (do not change these)
- First peek **60 seconds** after page load, then **every 10 seconds**; visible ~4 s each time.
- Each peek appears at a **random vertical position** (`top: 8%–48%`).
- On every peek he does a synced **"hello"**: ears flap + both eyes blink together (1.8 s, once).
- Ambient motion: trunk sways gently, hair tuft bobs.
- **Long-press (700 ms)** on the elephant hides him for **10 minutes**; the hidden-until
  timestamp persists in `localStorage` key `twin-peek-hide`, so it survives reloads.
- No click action. Mobile (<640 px): smaller (110 px wide). `prefers-reduced-motion`: static peek, no animation.

## Placement
Render the component in `src/layouts/SiteLayout.astro` so it appears on both `/` (paint canvas)
and `/home/` (homepage). If the owner later wants it on the homepage only, move the
`<ElephantPeek />` tag into `src/pages/home.astro` instead and remove it from the layout.

## Step 1 — Create `src/components/ElephantPeek.astro`
Create this file with the EXACT content below (copy verbatim, do not restyle):

```astro
---
/* Twin the elephant — peeking mascot for coPaint.
   First peek 60s after page load, then every 10s (visible ~4s).
   On each peek he does a synced "hello": ears flap + eyes blink together.
   Long-press (700ms) hides him for 10 minutes (persisted in localStorage). */
---
<div class="twin-wrap" id="twinPeek" aria-label="Twin the elephant peeking">
  <svg viewBox="0 0 220 220" role="img" aria-label="Twin peeking">
    <g class="ear"><ellipse cx="46" cy="108" rx="30" ry="42" fill="#9fb0c6"/><ellipse cx="46" cy="110" rx="16" ry="26" fill="#f6c9d4"/><path d="M38 88 q 8 22 2 44" stroke="#e8a9b8" stroke-width="3.4" fill="none" stroke-linecap="round" opacity=".8"/></g>
    <g class="ear"><ellipse cx="174" cy="108" rx="30" ry="42" fill="#9fb0c6"/><ellipse cx="174" cy="110" rx="16" ry="26" fill="#f6c9d4"/><path d="M166 88 q 8 22 2 44" stroke="#e8a9b8" stroke-width="3.4" fill="none" stroke-linecap="round" opacity=".8"/></g>
    <ellipse cx="110" cy="114" rx="58" ry="54" fill="#aeb9cd"/>
    <ellipse cx="90" cy="86" rx="19" ry="11" fill="#fff" opacity=".28" transform="rotate(-20 90 86)"/>
    <g class="tuft" stroke="#7c8aa0" stroke-width="6" stroke-linecap="round" fill="none"><path d="M104 62 Q 100 48 90 46"/><path d="M116 62 Q 118 48 128 46"/></g>
    <circle cx="66" cy="138" r="8" fill="#f4a7b9" opacity=".8"/>
    <circle cx="154" cy="138" r="8" fill="#f4a7b9" opacity=".8"/>
    <g class="eye"><circle cx="88" cy="108" r="7" fill="#2b2b2b"/></g>
    <g class="eye"><circle cx="132" cy="108" r="7" fill="#2b2b2b"/></g>
    <path d="M92 138 C 88 146 87 152 90 158 C 93 152 96 146 99 142 Z" fill="#f5f0e6" stroke="#ddd3c0" stroke-width="1.6"/>
    <path d="M128 138 C 132 146 133 152 130 158 C 127 152 124 146 121 142 Z" fill="#f5f0e6" stroke="#ddd3c0" stroke-width="1.6"/>
    <g class="trunk"><path d="M110 126 C 108 154 100 176 86 188" stroke="#aeb9cd" stroke-width="24" stroke-linecap="round" fill="none"/><path d="M104 136 C 102 158 96 174 86 184" stroke="#c9d2e2" stroke-width="6" stroke-linecap="round" fill="none" opacity=".8"/><path d="M102 150 q 9 5 17 3" stroke="#8b98ad" stroke-width="3.2" fill="none" stroke-linecap="round" opacity=".85"/><path d="M96 163 q 9 5 17 3" stroke="#8b98ad" stroke-width="3.2" fill="none" stroke-linecap="round" opacity=".85"/><ellipse cx="85" cy="188" rx="6.2" ry="5.2" fill="#8b98ad" opacity=".65"/><circle cx="82.8" cy="187" r="1.7" fill="#5a6579"/><circle cx="87.5" cy="188.6" r="1.7" fill="#5a6579"/></g>
  </svg>
</div>
<style>
  .twin-wrap{position:fixed;right:-170px;top:30%;width:150px;z-index:1500;transition:right .9s cubic-bezier(.34,1.25,.64,1),top .9s ease;filter:drop-shadow(-5px 6px 8px rgba(60,50,90,.18));touch-action:pan-y;user-select:none;-webkit-user-select:none;-webkit-touch-callout:none}
  .twin-wrap.in{right:-50px}
  .twin-wrap svg{display:block;width:100%;height:auto;overflow:visible;transform:rotate(-9deg);transition:transform .2s ease}
  .twin-wrap.pressing svg{transform:rotate(-9deg) scale(.93)}
  .ear{transform-box:fill-box;transform-origin:50% 12%}
  .hello .ear{animation:helloflap 1.8s ease-in-out 1}
  @keyframes helloflap{0%{transform:rotate(0deg)}18%{transform:rotate(-18deg)}32%{transform:rotate(7deg)}46%{transform:rotate(-14deg)}60%{transform:rotate(0deg)}100%{transform:rotate(0deg)}}
  .eye{transform-box:fill-box;transform-origin:50% 50%}
  .hello .eye{animation:helloblink 1.8s ease-in-out 1}
  @keyframes helloblink{0%,26%{transform:scaleY(1)}36%{transform:scaleY(.06)}48%{transform:scaleY(1)}100%{transform:scaleY(1)}}
  .trunk{transform-box:fill-box;transform-origin:50% 6%;animation:trunksway 5.5s ease-in-out infinite alternate}
  @keyframes trunksway{from{transform:rotate(-4deg)}to{transform:rotate(5deg)}}
  .tuft{transform-box:fill-box;transform-origin:50% 100%;animation:tuftbob 5.5s ease-in-out infinite alternate}
  @keyframes tuftbob{from{transform:rotate(-5deg)}to{transform:rotate(5deg)}}
  @media (max-width:640px){.twin-wrap{width:110px;right:-130px}.twin-wrap.in{right:-38px}}
  @media (prefers-reduced-motion:reduce){.twin-wrap *{animation:none!important;transition:none!important}}
</style>
<script>
(function(){
  var el = document.getElementById('twinPeek');
  if(!el) return;
  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var rnd = function(a,b){ return a + Math.random()*(b-a); };
  var FIRST_DELAY = 60000, PERIOD = 10000, VISIBLE = 4000;
  var HIDE_MS = 10*60*1000, LONGPRESS_MS = 700, KEY = 'twin-peek-hide';
  function getHiddenUntil(){ try { return parseInt(localStorage.getItem(KEY) || '0', 10) || 0; } catch(e){ return 0; } }
  function setHiddenUntil(t){ try { localStorage.setItem(KEY, String(t)); } catch(e){} }
  var state = 'peek', peekTimer = null, hideTimer = null, lpTimer = null;
  function clearTimers(){ [peekTimer, hideTimer].forEach(clearTimeout); }
  function cycle(){
    if(state !== 'peek') return;
    el.style.top = rnd(8, 48) + '%';
    el.classList.remove('hello');
    void el.offsetWidth;
    requestAnimationFrame(function(){
      el.classList.add('in');
      if(!reduced) el.classList.add('hello');
    });
    peekTimer = setTimeout(function(){
      el.classList.remove('in', 'hello');
      if(state !== 'peek') return;
      peekTimer = setTimeout(cycle, PERIOD - VISIBLE);
    }, VISIBLE);
  }
  function hideForTen(){
    clearTimers();
    state = 'hidden';
    el.classList.remove('in', 'hello', 'pressing');
    setHiddenUntil(Date.now() + HIDE_MS);
    hideTimer = setTimeout(resume, HIDE_MS);
  }
  function resume(){
    setHiddenUntil(0);
    state = 'peek';
    peekTimer = setTimeout(cycle, 800);
  }
  el.addEventListener('pointerdown', function(){
    el.classList.add('pressing');
    lpTimer = setTimeout(hideForTen, LONGPRESS_MS);
  });
  ['pointerup', 'pointerleave', 'pointercancel'].forEach(function(ev){
    el.addEventListener(ev, function(){ clearTimeout(lpTimer); el.classList.remove('pressing'); });
  });
  el.addEventListener('contextmenu', function(e){ e.preventDefault(); });
  if(getHiddenUntil() > Date.now()){
    state = 'hidden';
    hideTimer = setTimeout(resume, getHiddenUntil() - Date.now());
  } else if(reduced){
    el.style.top = '30%';
    el.classList.add('in');
  } else {
    peekTimer = setTimeout(cycle, FIRST_DELAY);
  }
})();
</script>
```

## Step 2 — Edit `src/layouts/SiteLayout.astro`
1. In the frontmatter, add the import (keep any existing lines):
   `import ElephantPeek from '../components/ElephantPeek.astro';`
2. In `<body>`, render it after the slot:
   ```astro
   <body>
     <slot />
     <ElephantPeek />
   </body>
   ```

## Notes for the implementer
- The component's `<style>` is Astro-scoped; `is:global` is NOT needed (all animated elements are static markup in the component).
- The `<script>` is plain (non-module) inline JS; keep it as-is so the single-file build inlines it verbatim.
- `z-index: 1500`, `position: fixed`, right edge. It does not block page scroll (`touch-action: pan-y`).
- `localStorage` access is wrapped in try/catch.

## Verification (do all of these)
1. `npm run build` succeeds with no errors.
2. The built HTML for BOTH pages contains the strings `twinPeek`, `helloflap`, and `twin-peek-hide`.
3. Quick visual test: temporarily change `FIRST_DELAY` from `60000` to `3000`, rebuild, load the page —
   he must peek in from the right edge within ~3 s and do the ear-flap + eye-blink hello.
   Long-press him for ~1 s — he must disappear. Then restore `FIRST_DELAY` to `60000` and rebuild.
4. Confirm the paint canvas still works normally (draw a stroke, open a popup) — the mascot must not
   interfere with drawing or toolbar popups.
5. Rebuild the standalone deliverables and redeploy to https://copaint-qxc.pages.dev.

## Done when
Both pages show the elephant peeking on the same schedule as the spec, long-press hides him for
10 minutes, and the canvas page is fully usable while he is visible.
