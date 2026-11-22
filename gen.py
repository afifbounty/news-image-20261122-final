#!/usr/bin/env python3
"""Render entry.png: one single picture summing up 22 Nov 2026.

A single dramatic scene, not a multi-panel page: the Strait of Hormuz
at dusk, tankers on dark water under a burning sky, with one big
catchy headline and a two-line caption carrying the rest of the day's
verified world news from Sunday 22 November 2026. Drawn as a
1024x1024 PNG with Pillow and the DejaVu fonts. Fully deterministic:
fixed geometry, no clock, no random numbers, so running this script
twice yields a byte-identical file.
"""

import hashlib
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
HORIZON = 560
BAND_TOP = 800

INK = (8, 28, 36)          # near-black teal caption band
SKY_TOP = (16, 24, 64)     # deep indigo dusk
SKY_LOW = (232, 120, 30)   # burning amber at the horizon
SEA = (10, 45, 55)
SEA_LINE = (24, 84, 96)
SUN = (245, 176, 20)
SUN_CORE = (255, 214, 90)
HULL = (12, 22, 30)
DECK = (226, 230, 232)
FUNNEL = (178, 34, 34)
FIRE_OUT = (232, 90, 10)
FIRE_MID = (245, 140, 20)
FIRE_IN = (255, 214, 90)
SMOKE_DARK = (70, 78, 88)
SMOKE_MID = (110, 118, 128)
SMOKE_LITE = (150, 158, 166)
AMBER = (240, 165, 10)
ALERT = (178, 34, 34)
WHITE = (255, 255, 255)

FONT_HOME = "/usr/share/fonts/truetype/dejavu"
BOLD = os.path.join(FONT_HOME, "DejaVuSans-Bold.ttf")
PLAIN = os.path.join(FONT_HOME, "DejaVuSans.ttf")


def typeface(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, text, fnt):
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0]


def fit_size(draw, text, path, start, limit, floor=12):
    """Largest size (down to floor) that fits text inside limit px."""
    size = start
    while size > floor:
        fnt = typeface(path, size)
        if text_w(draw, text, fnt) <= limit:
            return fnt
        size -= 1
    return typeface(path, floor)


def put_center(draw, cx, y, text, fnt, fill):
    draw.text((cx - text_w(draw, text, fnt) // 2, y), text, font=fnt, fill=fill)


def blend(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def paint_sky(draw):
    for y in range(HORIZON):
        draw.line([(0, y), (W, y)], fill=blend(SKY_TOP, SKY_LOW, y / HORIZON))


def paint_sun(draw):
    cx, cy, r = 720, 470, 82
    for rr, col in [(122, (232, 120, 30)), (100, (240, 150, 25))]:
        draw.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=col)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SUN)
    draw.ellipse([cx - 52, cy - 52, cx + 52, cy + 52], fill=SUN_CORE)


def paint_birds(draw):
    for bx, by, s in [(150, 150, 14), (210, 120, 11), (880, 200, 12)]:
        draw.arc([bx - s, by - s, bx, by + s], 180, 270, fill=HULL, width=3)
        draw.arc([bx, by - s, bx + s, by + s], 270, 360, fill=HULL, width=3)


def paint_sea(draw):
    draw.rectangle([0, HORIZON, W, BAND_TOP], fill=SEA)
    for y, x0, x1 in [
        (590, 60, 420), (610, 640, 980), (640, 120, 500), (665, 560, 960),
        (690, 80, 380), (715, 620, 990), (740, 140, 460), (770, 540, 940),
    ]:
        draw.line([(x0, y), (x1, y)], fill=SEA_LINE, width=3)


def paint_fire_glow(draw, cx, base):
    """Starburst flames rising from the struck tanker."""
    for outer, inner, pts, col in [
        (66, 26, 10, FIRE_OUT), (46, 18, 10, FIRE_MID), (26, 10, 8, FIRE_IN),
    ]:
        poly = []
        for i in range(pts * 2):
            r = outer if i % 2 == 0 else inner
            ang = math.pi * i / pts - math.pi / 2
            poly.append((cx + r * math.cos(ang), base - 30 + r * math.sin(ang)))
        draw.polygon(poly, fill=col)


def paint_smoke(draw, cx, base, tall, scale=1.0):
    """A plume of grey circles drifting up and left."""
    puffs = [
        (0, 0, 34, SMOKE_DARK), (-22, -42, 42, SMOKE_DARK),
        (-52, -88, 50, SMOKE_MID), (-88, -132, 56, SMOKE_MID),
        (-128, -172, 60, SMOKE_LITE), (-172, -206, 54, SMOKE_LITE),
    ]
    for dx, dy, r, col in puffs:
        k = tall / 206.0
        rr = r * scale
        draw.ellipse([cx + dx * k - rr, base + dy * k - rr,
                      cx + dx * k + rr, base + dy * k + rr], fill=col)


def paint_tanker(draw, x0, x1, deck_y, hull_top, hull_bot, scale, struck):
    """A tanker silhouette; the struck one burns and smokes."""
    draw.polygon([(x0, hull_top), (x1, hull_top), (x1 - 18 * scale, hull_bot),
                  (x0 + 26 * scale, hull_bot)], fill=HULL)
    draw.rectangle([x0 + 10 * scale, hull_top - 4, x1 - 10 * scale, hull_top],
                   fill=DECK)
    bx = x1 - 120 * scale
    draw.rectangle([bx, deck_y, bx + 78 * scale, hull_top], fill=DECK)
    draw.rectangle([bx + 52 * scale, deck_y - 26 * scale,
                    bx + 70 * scale, deck_y], fill=FUNNEL)
    draw.rectangle([bx + 52 * scale, deck_y - 26 * scale,
                    bx + 70 * scale, deck_y - 18 * scale], fill=AMBER)
    if struck:
        fx = x0 + (x1 - x0) // 2 - 40 * scale
        paint_fire_glow(draw, fx, hull_top)
        paint_smoke(draw, fx, hull_top - 40, 206)
        for yy, w0, w1 in [(hull_bot + 16, fx - 34, fx + 34),
                           (hull_bot + 44, fx - 24, fx + 24),
                           (hull_bot + 72, fx - 14, fx + 14)]:
            draw.line([(w0, yy), (w1, yy)], fill=FIRE_MID, width=5)


def paint_scene(draw):
    paint_sky(draw)
    paint_sun(draw)
    paint_birds(draw)
    paint_sea(draw)
    paint_tanker(draw, 40, 170, 622, 632, 652, 0.45, False)
    paint_tanker(draw, 700, 930, 606, 620, 650, 0.7, False)
    paint_tanker(draw, 180, 560, 540, 600, 652, 1.0, True)
    paint_smoke(draw, 905, 620, 110, 0.55)


def paint_caption(draw):
    draw.rectangle([0, BAND_TOP, W, H], fill=INK)
    draw.rectangle([0, BAND_TOP, W, BAND_TOP + 6], fill=AMBER)
    kick = typeface(BOLD, 20)
    put_center(draw, W // 2, 818, "SUNDAY 22 NOVEMBER 2026  \u2022  WORLD NEWS IN ONE PICTURE",
               kick, AMBER)
    head = fit_size(draw, "HORMUZ ON FIRE", BOLD, 100, W - 2 * 32)
    put_center(draw, W // 2, 844, "HORMUZ ON FIRE", head, WHITE)
    sub1 = fit_size(draw, "Iran strikes tankers in the Strait as Bahrain's industrial site burns",
                    PLAIN, 26, W - 2 * 32)
    put_center(draw, W // 2, 948,
               "Iran strikes tankers in the Strait as Bahrain's industrial site burns",
               sub1, WHITE)
    sub2 = fit_size(draw, "Also: 'El Chapo Isidro' captured \u2022 Zelenskyy: peace talks must deliver \u2022 Nvidia probed \u2022 Peru quake 6.9",
                    PLAIN, 22, W - 2 * 32)
    put_center(draw, W // 2, 980,
               "Also: 'El Chapo Isidro' captured \u2022 Zelenskyy: peace talks must deliver \u2022 Nvidia probed \u2022 Peru quake 6.9",
               sub2, (214, 232, 240))


def paint_tag(draw):
    tag = typeface(BOLD, 22)
    label = "BREAKING"
    tag_w = text_w(draw, label, tag) + 28
    ty = 28
    draw.rounded_rectangle([32, ty, 32 + tag_w, ty + 38], radius=8, fill=ALERT)
    draw.text((32 + 14, ty + 6), label, font=tag, fill=WHITE)


def render():
    img = Image.new("RGB", (W, H), INK)
    draw = ImageDraw.Draw(img)
    paint_scene(draw)
    paint_tag(draw)
    paint_caption(draw)
    return img


def main():
    img = render()
    img.save(OUT, format="PNG")
    data = open(OUT, "rb").read()
    print("wrote", OUT, len(data), "bytes")
    print("sha256", hashlib.sha256(data).hexdigest())


if __name__ == "__main__":
    main()
