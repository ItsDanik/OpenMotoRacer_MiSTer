#!/usr/bin/env python3
"""package/logos/MotoRacer.png from the game's own logo (its MENU.BKF, BITMAP/LOGOMR.LEZ, on
white, unpacked to a PNG first with the game's tools/lez.py): the white around it taken away, the
shadow under it kept as a see-through black, then fitted into 440x200.
    tools/make_game_logo.py logomr.png package/logos/MotoRacer.png
"""
import sys
from collections import deque
import numpy as np
from PIL import Image

src = np.asarray(Image.open(sys.argv[1]).convert("RGB")).astype(int)
h, w, _ = src.shape
lum = src.mean(axis=2)
neutral = (src.max(axis=2) - src.min(axis=2)) < 14
outer = np.zeros((h, w), bool)
seen = deque((x, y) for x in range(w) for y in (0, h - 1))
seen.extend((x, y) for y in range(h) for x in (0, w - 1))
# from the corners inward, the white alone: the silver letters are as light as the shadow's greys
for x, y in seen:
    outer[y, x] = True
while seen:
    x, y = seen.popleft()
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        a, b = x + dx, y + dy
        if 0 <= a < w and 0 <= b < h and not outer[b, a] and lum[b, a] >= 248:
            outer[b, a] = True
            seen.append((a, b))
# the soft edge next to it, two pixels' worth
soft = outer.copy()
for _ in range(2):
    soft[1:-1, 1:-1] |= soft[:-2, 1:-1] | soft[2:, 1:-1] | soft[1:-1, :-2] | soft[1:-1, 2:]
soft &= neutral
# the shadow: the greys under the letters, outside the oval
yy, xx = np.mgrid[0:h, 0:w]
oval = ((xx - 320) / 292.0) ** 2 + ((yy - 238) / 132.0) ** 2 < 1
shadow = neutral & ~oval & (yy >= 350)
clear = soft | shadow
# black, as see-through as it is light
alpha = np.where(clear, np.clip(255 - lum, 0, 255), 255).astype(np.uint8)
rgb = np.where(clear[..., None], 0, src).astype(np.uint8)
im = Image.fromarray(np.dstack((rgb, alpha)), "RGBA")
im = im.crop(im.getchannel("A").point(lambda v: 255 if v > 12 else 0).getbbox())
k = min(440 / im.width, 200 / im.height)
im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
out = Image.new("RGBA", (440, 200), (0, 0, 0, 0))
out.paste(im, ((440 - im.width) // 2, 200 - im.height))
out.save(sys.argv[2])
print(im.size)
