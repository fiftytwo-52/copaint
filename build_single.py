#!/usr/bin/env python3
"""Build the standalone coPaint deliverables:
   1. npm run build (Astro, multi-page)
   2. inline dist CSS + JS into each page
   3. on the paint page: replace outlines/outline-<id>.png with base64 data URIs
   4. rewrite cross-page links so the two files work side by side:
        paint page  /home -> kids-paint-home.html
        home page   /     -> kids-paint.html
   5. node --check each bundled script
   6. write ~/workspace/your_files/kids-paint.html + kids-paint-home.html
"""
import os, re, base64, subprocess, sys

PROJ = os.path.expanduser('~/workspace/kids-paint')
FINAL = os.path.join(PROJ, 'outline-src', 'final')
YOUR = os.path.expanduser('~/workspace/your_files')

print('== astro build ==')
r = subprocess.run(['npm', 'run', 'build'], cwd=PROJ, capture_output=True, text=True)
if r.returncode != 0:
    print(r.stdout[-2000:]); print(r.stderr[-2000:]); sys.exit('BUILD FAILED')

astro_dir = os.path.join(PROJ, 'dist', '_astro')

def inline_css(m):
    name = os.path.basename(m.group(1))
    css = open(os.path.join(astro_dir, name), encoding='utf-8').read()
    return '<style>\n' + css + '\n</style>'

def inline_js(m):
    name = os.path.basename(m.group(1))
    js = open(os.path.join(astro_dir, name), encoding='utf-8').read()
    return '<script>\n' + js + '\n</script>'

def build_page(dist_rel, out_name, link_rewrites, inline_outlines):
    html = open(os.path.join(PROJ, 'dist', dist_rel), encoding='utf-8').read()
    html, n_css = re.subn(r'<link rel="stylesheet" href="[^"]*?([^"/]+\.css)">', inline_css, html)
    # inline JS (drop type=module: file:// pages block module CORS)
    html, n_js = re.subn(r'<script type="module" src="[^"]*?([^"/]+\.js)">\s*</script>', inline_js, html)
    if inline_outlines:
        def inline_img(m):
            oid = m.group(1)
            p = os.path.join(FINAL, f'outline-{oid}.png')
            if not os.path.exists(p):
                print(f'  WARNING: missing {p}, leaving placeholder')
                return m.group(0)
            return 'data:image/png;base64,' + base64.b64encode(open(p, 'rb').read()).decode()
        html, n_img = re.subn(r'outlines/outline-([a-z0-9\-]+)\.png', inline_img, html)
        print(f'  inlined {n_img} outline images')
        left = re.findall(r'outlines/outline-[a-z0-9\-]+\.png', html)
        if left: print('  WARNING: uninlined:', left[:5])
    for old, new in link_rewrites:
        html = html.replace(old, new)
    for i, m in enumerate(re.finditer(r'<script>(.*?)</script>', html, re.S)):
        p = f'/tmp/kp_page_{i}.js'
        open(p, 'w').write(m.group(1))
        r = subprocess.run(['node', '--check', p], capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stderr); sys.exit(f'JS SYNTAX FAILED in {out_name}')
    print(f'  inlined {n_css} css, {n_js} js; js syntax OK')
    out = os.path.join(YOUR, out_name)
    open(out, 'w', encoding='utf-8').write(html)
    print(f'  wrote {out} ({os.path.getsize(out)} bytes)')

print('-- paint page --')
build_page('index.html', 'kids-paint.html', [('href="/home"', 'href="kids-paint-home.html"')], True)
print('-- home page --')
build_page(os.path.join('home', 'index.html'), 'kids-paint-home.html', [('href="/"', 'href="kids-paint.html"')], False)
print('done')
