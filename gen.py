#!/usr/bin/env python3
"""Render entry.png: a one-page newspaper front page for 22 Nov 2026.

Five verified world-news stories from Sunday 22 November 2026, drawn
as a 1024x1024 PNG with Pillow and the DejaVu fonts. The picture is
fully deterministic: fixed text, fixed geometry, no clock, no random
numbers, so running this script twice yields a byte-identical file.
"""

import hashlib
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
EDGE = 32

TEAL = (13, 71, 76)        # deep teal masthead
AMBER = (240, 165, 10)
PAPER = (250, 246, 238)    # warm cream
CARD = (255, 253, 246)
ALERT = (178, 34, 34)
MUTED = (70, 80, 92)
SKY = (214, 232, 240)
RUST = (198, 90, 24)
GREEN = (30, 130, 76)
WHITE = (255, 255, 255)

FONT_HOME = "/usr/share/fonts/truetype/dejavu"
BOLD = os.path.join(FONT_HOME, "DejaVuSans-Bold.ttf")
PLAIN = os.path.join(FONT_HOME, "DejaVuSans.ttf")


def load(path, size):
    return ImageFont.truetype(path, size)


def width(draw, text, fnt):
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0]


def shrink(draw, text, path, start, limit, floor=12):
    """Largest size (down to floor) that fits text inside limit px."""
    size = start
    while size > floor:
        fnt = load(path, size)
        if width(draw, text, fnt) <= limit:
            return fnt
        size -= 1
    return load(path, floor)


def wrap(draw, text, fnt, limit, cap):
    """Greedy word wrap, at most cap lines; words are never split."""
    out, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if width(draw, trial, fnt) <= limit:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
        if len(out) == cap:
            break
    if len(out) < cap and cur:
        out.append(cur)
    return out


def centre(draw, cx, y, text, fnt, fill):
    draw.text((cx - width(draw, text, fnt) // 2, y), text, font=fnt, fill=fill)


def glyph_dove(draw, x, y, w, h):
    """Diplomacy: a globe with an olive sprig and a green check."""
    cx, cy = x + w // 2, y + h // 2
    draw.ellipse([cx - 32, cy - 32, cx + 32, cy + 32], outline=TEAL, width=4)
    draw.ellipse([cx - 13, cy - 32, cx + 13, cy + 32], outline=TEAL, width=3)
    draw.line([(cx - 32, cy), (cx + 32, cy)], fill=TEAL, width=3)
    draw.arc([cx - 32, cy - 12, cx + 32, cy + 12], 180, 360, fill=GREEN, width=3)
    draw.line([(cx + 18, cy + 18), (cx + 26, cy + 26), (cx + 38, cy + 8)],
              fill=GREEN, width=5, joint="curve")


def glyph_scales(draw, x, y, w, h):
    """Justice: a balance scale."""
    cx = x + w // 2
    top, base = y + 10, y + h - 12
    draw.line([(cx, top), (cx, base)], fill=TEAL, width=4)
    draw.line([(cx - 34, top + 8), (cx + 34, top + 8)], fill=TEAL, width=4)
    for sx in (cx - 34, cx + 34):
        draw.line([(sx, top + 8), (sx, top + 30)], fill=TEAL, width=3)
        draw.arc([sx - 14, top + 22, sx + 14, top + 44], 0, 180,
                 fill=AMBER, width=4)
    draw.line([(cx - 22, base), (cx + 22, base)], fill=TEAL, width=4)


def glyph_candles(draw, x, y, w, h):
    """Markets: three candlesticks and a falling trend line."""
    base = y + h - 12
    bars = [(x + 20, 26, GREEN), (x + 46, 44, ALERT), (x + 72, 18, ALERT)]
    for bx, bh, col in bars:
        draw.line([(bx + 7, y + 8), (bx + 7, base - bh - 8)], fill=TEAL, width=2)
        draw.rectangle([bx, base - bh, bx + 14, base - 6], fill=col)
    draw.line([(x + 14, y + 16), (x + 52, y + 34), (x + 92, y + 52)],
              fill=RUST, width=4, joint="curve")


def glyph_seismic(draw, x, y, w, h):
    """Disaster: a seismograph trace with a red epicentre dot."""
    cy = y + h // 2
    pts = [(x + 8, cy), (x + 26, cy), (x + 34, cy - 26), (x + 42, cy + 22),
           (x + 50, cy - 8), (x + 62, cy), (x + 70, cy - 34), (x + 78, cy + 28),
           (x + 86, cy), (x + 108, cy)]
    draw.line(pts, fill=RUST, width=4, joint="curve")
    draw.ellipse([x + 66, cy - 38, x + 74, cy - 30], fill=ALERT)


GLYPHS = {
    "dove": glyph_dove,
    "scales": glyph_scales,
    "candles": glyph_candles,
    "seismic": glyph_seismic,
}

STORIES = [
    {
        "kicker": "DIPLOMACY",
        "title": "Zelenskyy: peace talks must deliver",
        "body": (
            "Ukraine's president says upcoming four-nation talks must "
            "bring meaningful progress as Russian forces hit bridges "
            "109 times."
        ),
        "glyph": "dove",
    },
    {
        "kicker": "JUSTICE",
        "title": "Mexico captures 'El Chapo Isidro'",
        "body": (
            "FBI's most-wanted cartel boss seized in Sinaloa after a US "
            "intelligence tip; the firefight leaves at least 11 dead."
        ),
        "glyph": "scales",
    },
    {
        "kicker": "MARKETS",
        "title": "Nvidia faces SEC inquiry",
        "body": (
            "Nvidia's finances come under SEC scrutiny as a resignation "
            "scramble shakes the chip giant."
        ),
        "glyph": "candles",
    },
    {
        "kicker": "DISASTER",
        "title": "6.9 quake rocks Peru",
        "body": (
            "A magnitude 6.9 earthquake strikes Peru's Junin region "
            "on Sunday."
        ),
        "glyph": "seismic",
    },
]

LEAD_HEAD = "IRAN STRIKES TANKERS IN HORMUZ"
LEAD_BODY = (
    "Tehran attacks tankers in the Strait of Hormuz as a pair is struck "
    "near Oman; Bahrain reports an Iranian strike set an industrial site "
    "ablaze while air defences intercept more attacks"
)
TICKER = (
    "Alcaraz faces Zverev in ATP Finals decider \u2022 "
    "France sees 4th weekend of cost-of-living protests",
    "Norway court voids oil licences \u2022 "
    "Gaza flooding: four nations urge Israel to open aid access",
)


def draw_masthead(draw):
    draw.rectangle([0, 0, W, 148], fill=TEAL)
    title = shrink(draw, "THE WORLD IN ONE PICTURE", BOLD, 40, W - 2 * EDGE)
    centre(draw, W // 2, 14, "THE WORLD IN ONE PICTURE", title, AMBER)
    date = shrink(draw, "SUNDAY 22 NOVEMBER 2026", BOLD, 56, W - 2 * EDGE)
    centre(draw, W // 2, 58, "SUNDAY 22 NOVEMBER 2026", date, WHITE)
    sub = load(PLAIN, 24)
    centre(draw, W // 2, 116, "WORLD NEWS \u2022 FIVE STORIES, ONE DAY", sub, SKY)
    draw.rectangle([0, 148, W, 156], fill=AMBER)


def draw_lead(draw):
    tag = load(BOLD, 24)
    label = "BREAKING"
    tag_w = width(draw, label, tag) + 28
    ty = 172
    draw.rounded_rectangle([EDGE, ty, EDGE + tag_w, ty + 38], radius=8, fill=ALERT)
    draw.text((EDGE + 14, ty + 6), label, font=tag, fill=WHITE)
    head = shrink(draw, LEAD_HEAD, BOLD, 42, W - 2 * EDGE)
    draw.text((EDGE, 222), LEAD_HEAD, font=head, fill=TEAL)
    body_font = load(PLAIN, 26)
    lines = wrap(draw, LEAD_BODY, body_font, W - 2 * EDGE, 3)
    y = 282
    for line in lines:
        draw.text((EDGE, y), line, font=body_font, fill=MUTED)
        y += 34
    draw.line([(EDGE, 382), (W - EDGE, 382)], fill=TEAL, width=3)


def draw_card(draw, story, px, py):
    pw, ph = 472, 252
    draw.rectangle([px, py, px + pw, py + ph], fill=CARD, outline=TEAL, width=2)
    draw.rectangle([px, py, px + pw, py + 40], fill=TEAL)
    tag = load(BOLD, 23)
    draw.text((px + 16, py + 7), story["kicker"], font=tag, fill=AMBER)
    ix, iy, iw, ih = px + 16, py + 40 + 16, 118, 86
    draw.rectangle([ix, iy, ix + iw, iy + ih], fill=SKY)
    GLYPHS[story["glyph"]](draw, ix, iy, iw, ih)
    tx, tw = px + 144, 312
    head = shrink(draw, story["title"], BOLD, 30, tw)
    lines = wrap(draw, story["title"], head, tw, 2)
    hy = py + 40 + 14
    for line in lines:
        draw.text((tx, hy), line, font=head, fill=TEAL)
        hy += 36
    cap_font = load(PLAIN, 22)
    cap_lines = []
    for size in range(22, 16, -1):
        cap_font = load(PLAIN, size)
        cap_lines = wrap(draw, story["body"], cap_font, pw - 32, 3)
        if len(cap_lines) <= 3 and " ".join(cap_lines) == story["body"]:
            break
    cy = py + 40 + 16 + 86 + 12
    for line in cap_lines:
        draw.text((px + 16, cy), line, font=cap_font, fill=MUTED)
        cy += 28


def draw_footer(draw):
    draw.rectangle([0, 936, W, H], fill=TEAL)
    foot = load(BOLD, 24)
    draw.text((EDGE, 944), "ALSO IN THE NEWS", font=foot, fill=AMBER)
    y = 972
    for line in TICKER:
        fnt = shrink(draw, line, PLAIN, 20, W - 2 * EDGE)
        draw.text((EDGE, y), line, font=fnt, fill=WHITE)
        y += 26


def render():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    draw_lead(draw)
    spots = [(EDGE, 404), (EDGE + 472 + 16, 404),
             (EDGE, 404 + 252 + 16), (EDGE + 472 + 16, 404 + 252 + 16)]
    for story, (px, py) in zip(STORIES, spots):
        draw_card(draw, story, px, py)
    draw_footer(draw)
    return img


def main():
    img = render()
    img.save(OUT, format="PNG")
    data = open(OUT, "rb").read()
    print("wrote", OUT, len(data), "bytes")
    print("sha256", hashlib.sha256(data).hexdigest())


if __name__ == "__main__":
    main()
