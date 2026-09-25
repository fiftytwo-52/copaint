#!/usr/bin/env python3
"""Post-process generated coloring outlines:
   - find media-generation-outline-<id>-0-*.png files
   - rename to outline-<id>.png
   - resize to max 512px, convert white background -> transparent
   - write to outline-src/final/
"""
import os, re, sys

SRC = os.path.expanduser('~/workspace/kids-paint/outline-src')
DST = os.path.join(SRC, 'final')
os.makedirs(DST, exist_ok=True)

from PIL import Image
import numpy as np

EXPECTED = ['cat','dog','bird','fish','butterfly','bee','turtle','rabbit','elephant','lion',
'monkey','frog','owl','horse','face','eye','ear','nose','mouth','hand','foot','tooth',
'tree','pine-tree','sunflower','tulip','rose','leaf','mushroom','cactus','daisy','palm-tree',
'car','bus','truck','bicycle','airplane','boat','boy','girl','baby','jumping-child',
'school','book','pencil','backpack','scissors','crayon','globe','bell',
'computer','laptop','keyboard','mouse','printer','headphones','tablet','robot',
# 2026-09-25 additions: trees, desktop parts, phones, carnivores, omnivores, herbivores
'oak-tree','apple-tree','coconut-tree','willow-tree','cherry-tree','christmas-tree',
'monitor','cpu-tower','speakers','webcam','smartphone','telephone',
'tiger','shark','crocodile','wolf','eagle','snake','spider',
'bear','pig','chicken','crow','raccoon',
'cow','deer','goat','giraffe','zebra',
'desktop-set']

found = {}
for f in os.listdir(SRC):
    m = re.match(r'media-generation-outline-(.+?)-0-[0-9a-f-]+\.png$', f)
    if m:
        oid = m.group(1)
        # keep the largest file if duplicates
        p = os.path.join(SRC, f)
        if oid not in found or os.path.getsize(p) > os.path.getsize(found[oid]):
            found[oid] = p

missing = [e for e in EXPECTED if e not in found]
extra = [k for k in found if k not in EXPECTED]
print(f'found {len(found)}/50')
if missing: print('MISSING:', missing)
if extra: print('EXTRA (unexpected ids):', extra)

def process(oid, src):
    img = Image.open(src).convert('RGBA')
    img.thumbnail((512, 512), Image.LANCZOS)
    a = np.array(img)
    lum = a[..., :3].mean(axis=2)
    # white (lum>=245) -> transparent; black (lum<=180) -> opaque; smooth ramp between
    alpha = np.clip((245 - lum) * 255.0 / 65.0, 0, 255).astype(np.uint8)
    a[..., 3] = alpha
    out = Image.fromarray(a, 'RGBA')
    out.save(os.path.join(DST, f'outline-{oid}.png'), optimize=True)
    return out.size

for oid in EXPECTED:
    if oid in found:
        size = process(oid, found[oid])
        print(f'  outline-{oid}.png {size}')

# contact sheet for visual QA
import math
thumbs = []
thumbsize = (160, 160)
for oid in EXPECTED:
    p = os.path.join(DST, f'outline-{oid}.png')
    if os.path.exists(p):
        t = Image.open(p).convert('RGBA')
        t.thumbnail(thumbsize, Image.LANCZOS)
        bg = Image.new('RGBA', thumbsize, (255, 255, 255, 255))
        bg.alpha_composite(t, ((thumbsize[0]-t.width)//2, (thumbsize[1]-t.height)//2))
        thumbs.append((oid, bg.convert('RGB')))

cols = 10
rows = math.ceil(len(thumbs) / cols)
sheet = Image.new('RGB', (cols * thumbsize[0], rows * thumbsize[1]), (240, 240, 240))
for i, (oid, t) in enumerate(thumbs):
    sheet.paste(t, ((i % cols) * thumbsize[0], (i // cols) * thumbsize[1]))
sheet.save(os.path.join(DST, '_contact-sheet.png'))
print('contact sheet written')
