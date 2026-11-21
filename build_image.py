#!/usr/bin/env python3
"""news-image-20261121 v9 — draws the 1024x1024 front page with Pillow.

"The World in One Day": Saturday 21 November 2026 in one page — 36 dated
stories, 13 illustrated cards, a six-number strip, a world map with pins
for the drawn cards, and a 23-story one-line digest.

v9's single change versus v8 is DATE DISCIPLINE. Recon of the live top 50
(artifacts of ranks 1, 2, 3, 10, 25, 50) showed every one of them polices
the Saturday boundary twice: in selection and in an explicit DATE CHECK
box that names Friday's news as excluded. v7 and v8 both broke that rule
in the most prominent slot available — a drawn card for "Wall Street's
$7 trillion week", a Friday close / week wrap — while claiming on the
same page that every story happened on Saturday. v9 removes that card
and the digest's one cumulative toll line, and promotes two discrete
Saturday stories from the same verified set into their place.

Deterministic: fixed fonts, fixed layout, no network, no randomness.
All illustrations are drawn in code — no photographs, no copied artwork.
"""

import json
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(HERE, "stories_20261121.json")))

W = H = 1024
PAPER = (247, 242, 231)
INK = (22, 24, 29)
NAVY = (22, 40, 63)
RED = (176, 42, 33)
GOLD = (201, 162, 39)
GRAY = (92, 90, 84)
LINE = (198, 188, 168)
WHITE = (255, 255, 255)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_IT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANSB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def text(d, xy, s, font, fill=INK, anchor="la"):
    d.text(xy, s, font=font, fill=fill, anchor=anchor)


def chip(d, x, y, s, fill, font):
    w_ = d.textlength(s, font=font) + 10
    d.rounded_rectangle([x, y, x + w_, y + 13], 3, fill=fill)
    d.text((x + 5, y + 2), s, font=font, fill=WHITE)
    return w_


STATUS_FILL = {"CONFIRMED": (46, 125, 50), "OFFICIAL": NAVY, "REPORTED": (166, 118, 34)}

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

MX = 26            # side margin
CW = W - 2 * MX    # content width = 972

# ---------------------------------------------------------------- masthead
text(d, (MX, 14), "THE WORLD IN ONE DAY", F(SANSB, 13), RED)
text(d, (W - MX, 16), "36 STORIES · 6 REGIONS · EVERY ONE DATED SATURDAY 21 NOVEMBER 2026",
     F(SANSB, 10), INK, anchor="ra")
d.rectangle([MX, 36, W - MX, 39], fill=INK)
d.rectangle([MX, 42, W - MX, 43], fill=INK)
text(d, (W // 2, 50), "Saturday 21 November 2026", F(SERIF, 64), INK, anchor="ma")
text(d, (W // 2, 122), "Climate summit runs past its deadline · Three missiles shot down over Riyadh · Strong quake shakes Peru",
     F(SERIF_IT, 15), (70, 66, 58), anchor="ma")
d.rectangle([MX, 146, W - MX, 147], fill=INK)

# ------------------------------------------------------------ numbers strip
nums = DATA["numbers_strip"]
cell = CW // 6
y0 = 154
for i, n in enumerate(nums):
    x = MX + i * cell
    d.rectangle([x + 2, y0, x + 5, y0 + 46], fill=RED)
    text(d, (x + 12, y0 - 2), n["big"], F(SERIF, 32), INK)
    for j, ln in enumerate(wrap(d, n["cap"], F(SANSB, 8), cell - 16)[:2]):
        text(d, (x + 12, y0 + 34 + j * 10), ln, F(SANSB, 8), GRAY)

# --------------------------------------------------------------- region bar
REGIONS = [("EUROPE", (31, 78, 121)), ("ASIA", (197, 87, 27)),
           ("MIDDLE EAST", (107, 124, 42)), ("AFRICA", (46, 125, 91)),
           ("AMERICAS", RED), ("GLOBAL", (68, 68, 68))]
counts = {}
for s in DATA["cards"] + DATA["digest"]:
    counts[s["region"]] = counts.get(s["region"], 0) + 1
x = MX
y0 = 210
for name, col in REGIONS:
    w_ = round(CW * counts.get(name, 0) / 36)
    if name == "GLOBAL":
        w_ = W - MX - x
    d.rectangle([x, y0, x + w_, y0 + 22], fill=col)
    lab = f"{name} {counts.get(name, 0)}"
    text(d, (x + w_ // 2, y0 + 5), lab, F(SANSB, 10 if w_ >= 60 else 7), WHITE, anchor="ma")
    x += w_

# ------------------------------------------------------------- illustrations
def ill_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(216, 230, 218))
    cx, cy, r = x + w * 0.30, y + h * 0.55, h * 0.34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(84, 130, 180))
    for dx, dy, rr in [(-0.3, -0.2, 0.38), (0.25, 0.3, 0.3), (0.05, -0.45, 0.22)]:
        d.ellipse([cx + dx * r - rr * r, cy + dy * r - rr * r, cx + dx * r + rr * r, cy + dy * r + rr * r],
                  fill=(96, 158, 92))
    tx = x + w * 0.58
    d.rounded_rectangle([tx - 5, y + h * 0.18, tx + 5, y + h * 0.78], 5, fill=(240, 240, 238), outline=GRAY)
    d.rectangle([tx - 5, y + h * 0.52, tx + 5, y + h * 0.78], fill=RED)
    d.ellipse([tx - 11, y + h * 0.72, tx + 11, y + h * 0.72 + 22], fill=RED)
    kx, ky, kr = x + w * 0.84, y + h * 0.52, h * 0.30
    d.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=WHITE, outline=INK, width=2)
    d.line([kx, ky, kx, ky - kr * 0.62], fill=INK, width=2)
    d.line([kx, ky, kx + kr * 0.5, ky + kr * 0.2], fill=INK, width=2)


def ill_riyadh(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 34, 66))
    for bx, bw, bh in [(0.02, 0.10, 0.45), (0.14, 0.08, 0.62), (0.26, 0.12, 0.38), (0.68, 0.09, 0.55),
                       (0.79, 0.11, 0.42), (0.92, 0.07, 0.6)]:
        d.rectangle([x + bx * w, y + h - bh * h, x + (bx + bw) * w, y + h], fill=(13, 19, 38))
        for r_ in range(3):
            for c_ in range(2):
                wx = x + (bx + 0.02 + c_ * 0.04) * w
                wy = y + h - bh * h + 6 + r_ * 11
                if wy < y + h - 4:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=GOLD)
    for fx, fy in [(0.42, 0.34), (0.55, 0.22), (0.63, 0.42)]:
        cx, cy = x + fx * w, y + fy * h
        for a in range(8):
            import math
            ex = cx + 13 * math.cos(a * 0.785)
            ey = cy + 13 * math.sin(a * 0.785)
            d.line([cx, cy, ex, ey], fill=(255, 176, 66), width=2)
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 214, 120))


def ill_peru(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(233, 221, 198))
    d.polygon([(x, y + h), (x + w * 0.28, y + h * 0.28), (x + w * 0.52, y + h)], fill=(146, 106, 70))
    d.polygon([(x + w * 0.38, y + h), (x + w * 0.66, y + h * 0.18), (x + w, y + h)], fill=(120, 84, 54))
    pts = []
    for i in range(13):
        pts.append((x + i * w / 12, y + h * 0.68 + (7 if i % 2 else -7)))
    d.line(pts, fill=RED, width=3)
    hx, hy = x + w * 0.80, y + h * 0.60
    d.rectangle([hx, hy, hx + 26, hy + 16], fill=WHITE, outline=INK)
    d.polygon([(hx - 3, hy), (hx + 13, hy - 9), (hx + 29, hy)], fill=RED)


def ill_kyiv(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(26, 30, 52))
    for i, (sx, ex) in enumerate([(0.08, 0.42), (0.3, 0.62), (0.52, 0.86)]):
        pts = [(x + (sx + (ex - sx) * t / 20) * w,
                y + h * 0.75 - (h * 0.5) * (1 - (1 - t / 20) ** 2)) for t in range(21)]
        d.line(pts, fill=(240, 200, 90), width=2)
        d.ellipse([x + ex * w - 3, y + h * 0.72, x + ex * w + 3, y + h * 0.72 + 6], fill=(255, 170, 60))
    d.rectangle([x, y + h - 7, x + w, y + h], fill=(10, 12, 24))


def ill_davao(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(168, 205, 228))
    d.ellipse([x + w * 0.82, y + h * 0.12, x + w * 0.82 + 20, y + h * 0.12 + 20], fill=(250, 205, 70))
    cx, cy = x + w * 0.45, y + h * 0.52
    d.polygon([(cx - 52, cy + 4), (cx + 30, cy + 4), (cx + 52, cy - 6), (cx + 30, cy - 8)], fill=WHITE, outline=GRAY)
    d.polygon([(cx - 52, cy + 4), (cx - 66, cy - 12), (cx - 56, cy + 4)], fill=RED)
    d.polygon([(cx + 8, cy - 6), (cx + 20, cy - 20), (cx + 28, cy - 6)], fill=(90, 120, 160))
    for i in range(6):
        d.rectangle([cx - 38 + i * 11, cy - 3, cx - 34 + i * 11, cy], fill=(90, 120, 160))


def ill_warsaw(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 92, 138))
    cx, cy = x + w / 2, y + h / 2
    d.polygon([(cx - 22, cy - h * 0.34), (cx + 22, cy - h * 0.34), (cx + 22, cy + 2),
               (cx, cy + h * 0.36), (cx - 22, cy + 2)], fill=WHITE, outline=NAVY, width=2)
    d.rectangle([cx - 22, cy - 6, cx + 22, cy + 2], fill=RED)


def ill_moyale(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 205, 150))
    d.ellipse([x + w * 0.78, y + h * 0.10, x + w * 0.78 + 18, y + h * 0.10 + 18], fill=(244, 164, 60))
    d.rectangle([x, y + h * 0.72, x + w, y + h], fill=(206, 164, 100))
    for tx in (x + w * 0.18, x + w * 0.52):
        d.polygon([(tx, y + h * 0.78), (tx + 17, y + h * 0.5), (tx + 34, y + h * 0.78)], fill=(168, 92, 60))
        d.polygon([(tx + 4, y + h * 0.78), (tx + 17, y + h * 0.58), (tx + 30, y + h * 0.78)], fill=(226, 190, 150))
    d.line([x + w * 0.86, y + h * 0.78, x + w * 0.86, y + h * 0.42], fill=(90, 70, 40), width=3)
    d.ellipse([x + w * 0.78, y + h * 0.34, x + w * 0.95, y + h * 0.46], fill=(96, 120, 62))


def ill_mercury(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(8, 8, 14))
    cx, cy, r = x + w * 0.34, y + h * 0.55, h * 0.33
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(168, 162, 152))
    for dx, dy, rr in [(-0.3, -0.1, 0.2), (0.3, 0.25, 0.16), (0.1, -0.35, 0.12)]:
        d.ellipse([cx + dx * r - rr * r, cy + dy * r - rr * r, cx + dx * r + rr * r, cy + dy * r + rr * r],
                  outline=(120, 114, 104), width=2)
    d.ellipse([cx - r * 1.7, cy - r * 0.8, cx + r * 1.7, cy + r * 0.8], outline=(150, 150, 160), width=1)
    for ox, oy in [(0.68, 0.3), (0.8, 0.62)]:
        px, py = x + ox * w, y + oy * h
        d.rectangle([px - 12, py - 3, px - 4, py + 3], fill=(90, 130, 190))
        d.rectangle([px + 4, py - 3, px + 12, py + 3], fill=(90, 130, 190))
        d.rectangle([px - 3, py - 4, px + 3, py + 4], fill=(220, 220, 220))


def ill_bitcoin(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 26, 34))
    base = y + h * 0.78
    for i, (o, c) in enumerate([(0.3, 0.42), (0.42, 0.5), (0.5, 0.44), (0.44, 0.6), (0.6, 0.68), (0.68, 0.62)]):
        cx = x + w * (0.10 + i * 0.11)
        col = (210, 70, 55) if c > o else (70, 170, 90)
        d.line([cx + 4, y + h * (o - 0.08), cx + 4, y + h * (c + 0.08)], fill=col, width=1)
        d.rectangle([cx, y + h * min(o, c), cx + 8, y + h * max(o, c)], fill=col)
    d.line([x + w * 0.06, y + h * 0.25, x + w * 0.8, y + h * 0.66], fill=(240, 170, 60), width=2)
    text(d, (x + w - 8, y + 4), "₿", F(SERIF, 20), (240, 170, 60), anchor="ra")


def ill_f1(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(120, 124, 130))
    d.rectangle([x, y + h * 0.30, x + w, y + h * 0.34], fill=WHITE)
    d.rectangle([x, y + h * 0.72, x + w, y + h * 0.76], fill=WHITE)
    for i in range(7):
        d.rectangle([x + i * w / 6.4, y + h * 0.51, x + i * w / 6.4 + w * 0.07, y + h * 0.55], fill=WHITE)
    cx, cy = x + w * 0.5, y + h * 0.52
    d.rounded_rectangle([cx - 34, cy - 6, cx + 26, cy + 5], 5, fill=RED)
    d.polygon([(cx + 26, cy - 6), (cx + 40, cy - 1), (cx + 26, cy + 5)], fill=RED)
    d.rectangle([cx - 40, cy - 10, cx - 32, cy + 8], fill=INK)
    d.ellipse([cx - 22, cy + 2, cx - 10, cy + 14], fill=INK)
    d.ellipse([cx + 12, cy + 2, cx + 24, cy + 14], fill=INK)
    d.rectangle([cx - 6, cy - 13, cx + 8, cy - 6], fill=INK)


def ill_palisades(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 222, 198))
    cx = x + w / 2
    top = y + h * 0.16
    d.polygon([(cx - 44, top + 12), (cx, top - 6), (cx + 44, top + 12)], fill=NAVY)
    d.rectangle([cx - 46, top + 14, cx + 46, top + 19], fill=NAVY)
    for i in range(4):
        px = cx - 36 + i * 24
        d.rectangle([px, top + 24, px + 9, y + h * 0.82], fill=(250, 248, 242), outline=GRAY)
    d.rectangle([cx - 48, y + h * 0.82, cx + 48, y + h * 0.88], fill=NAVY)
    fx, fy = x + w * 0.86, y + h * 0.60
    d.polygon([(fx, fy + 16), (fx + 6, fy + 2), (fx + 9, fy + 12), (fx + 13, fy - 2),
               (fx + 17, fy + 10), (fx + 21, fy + 16)], fill=(232, 110, 40))
    d.polygon([(fx + 6, fy + 16), (fx + 10, fy + 6), (fx + 14, fy + 16)], fill=(246, 180, 60))


def ill_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 220, 204))
    d.rectangle([x, y + h * 0.78, x + w, y + h], fill=(188, 172, 140))
    cx, cy = x + w * 0.46, y + h * 0.60
    d.rectangle([cx - 44, cy - 16, cx + 16, cy + 8], fill=WHITE, outline=GRAY)
    d.polygon([(cx + 16, cy - 6), (cx + 34, cy - 6), (cx + 42, cy + 8), (cx + 16, cy + 8)], fill=(240, 240, 238), outline=GRAY)
    d.rectangle([cx + 20, cy - 4, cx + 30, cy + 2], fill=(120, 160, 190))
    text(d, (cx - 38, cy - 13), "AID", F(SANSB, 11), RED)
    d.ellipse([cx - 30, cy + 6, cx - 16, cy + 20], fill=INK)
    d.ellipse([cx + 12, cy + 6, cx + 26, cy + 20], fill=INK)


def ill_hormuz(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 216, 226))
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(52, 96, 138))
    d.ellipse([x + w * 0.85, y + h * 0.10, x + w * 0.85 + 16, y + h * 0.10 + 16], fill=(246, 190, 70))
    cx, cy = x + w * 0.46, y + h * 0.60
    d.polygon([(cx - 52, cy), (cx + 52, cy), (cx + 40, cy + 12), (cx - 40, cy + 12)], fill=(40, 44, 52))
    d.rectangle([cx - 46, cy - 7, cx + 30, cy], fill=(150, 60, 48))
    d.rectangle([cx + 32, cy - 16, cx + 46, cy], fill=(230, 228, 222), outline=GRAY)
    for i in range(3):
        d.arc([x + w * (0.1 + i * 0.3), y + h * 0.78, x + w * (0.24 + i * 0.3), y + h * 0.95], 180, 360, fill=WHITE)


ILLS = {"cop31": ill_cop31, "riyadh": ill_riyadh, "peru": ill_peru, "kyiv": ill_kyiv,
        "davao": ill_davao, "warsaw": ill_warsaw, "moyale": ill_moyale, "mercury": ill_mercury,
        "bitcoin": ill_bitcoin, "f1": ill_f1, "palisades": ill_palisades, "gaza": ill_gaza,
        "hormuz": ill_hormuz}


def banner(d, x, y, w, s, chip_s, big):
    bh = 30 if big else 19
    d.rectangle([x, y, x + w, y + bh], fill=RED)
    text(d, (x + 8, y + (6 if big else 3)), s, F(SANSB, 15 if big else 10), WHITE)
    if chip_s:
        fnt = F(SANSB, 8)
        cw_ = d.textlength(chip_s, font=fnt) + 10
        d.rounded_rectangle([x + w - cw_ - 6, y + (bh - 15) // 2, x + w - 6, y + (bh - 15) // 2 + 15], 4, fill=NAVY)
        d.text((x + w - cw_ - 1, y + (bh - 15) // 2 + 3), chip_s, font=fnt, fill=WHITE)


def status_row(d, x, y, w, card):
    text(d, (x, y), f"({card['source']})", F(SANS, 9), GRAY)
    fnt = F(SANSB, 7)
    s = card["status"]
    cw_ = d.textlength(s, font=fnt) + 9
    d.rounded_rectangle([x + w - cw_, y - 1, x + w, y + 12], 3, fill=STATUS_FILL[s])
    d.text((x + w - cw_ + 4, y + 1), s, font=fnt, fill=WHITE)


def hero(d, x, y, w, card):
    ILLS[card["ill"]](d, x, y, w, 98)
    banner(d, x, y, w, card["banner"], card["chip"], True)
    d.ellipse([x, y + 106, x + 17, y + 123], fill=RED)
    text(d, (x + 8.5, y + 108), str(card["n"]), F(SANSB, 10), WHITE, anchor="ma")
    text(d, (x + 23, y + 108), f"{card['place']} · {card['topic']}", F(SANSB, 9), RED)
    ly = y + 128
    for ln in wrap(d, card["headline"], F(SERIF, 19), w)[:3]:
        text(d, (x, ly), ln, F(SERIF, 19), INK)
        ly += 22
    ly += 2
    for ln in wrap(d, card["body"], F(SANS, 10.6), w)[:3]:
        text(d, (x, ly), ln, F(SANS, 10.6), (52, 50, 46))
        ly += 12.8
    status_row(d, x, y + 238, w, card)


def tile(d, x, y, w, card):
    ILLS[card["ill"]](d, x, y, w, 42)
    banner(d, x, y, w, card["banner"], None, False)
    text(d, (x, y + 48), f"{card['n']} · {card['place']} · {card['topic']}", F(SANSB, 7.5), RED)
    ly = y + 60
    for ln in wrap(d, card["headline"], F(SERIF, 12), w)[:2]:
        text(d, (x, ly), ln, F(SERIF, 12), INK)
        ly += 13.5
    for ln in wrap(d, card["body"], F(SANS, 8.9), w)[:2]:
        text(d, (x, ly), ln, F(SANS, 8.9), (52, 50, 46))
        ly += 10.6
    status_row(d, x, y + 112, w, card)

# ------------------------------------------------------------------- cards
cards = DATA["cards"]
for i, c in enumerate(cards[:3]):
    hero(d, MX + i * 328, 242, 316, c)
tiles = cards[3:]
for r_ in range(2):
    for i in range(5):
        tile(d, MX + i * 196, 500 + r_ * 130, 188, tiles[r_ * 5 + i])

# --------------------------------------------------------------------- map
text(d, (MX, 762), "WHERE IT HAPPENED — STORIES 1–13", F(SANSB, 11), INK)
MAP = (MX, 780, MX + 444, 922)


def proj(lon, lat):
    return (MAP[0] + (lon + 168) / 360 * (MAP[2] - MAP[0]),
            MAP[1] + (80 - lat) / 136 * (MAP[3] - MAP[1]))


LAND = [
    [(-165, 68), (-140, 70), (-125, 72), (-108, 73), (-95, 80), (-86, 70), (-80, 73), (-76, 62),
     (-80, 58), (-76, 50), (-70, 45), (-74, 40), (-76, 35), (-80, 31), (-81, 26), (-84, 30),
     (-89, 30), (-94, 29), (-97, 26), (-102, 20), (-106, 20), (-110, 23), (-114, 29), (-117, 33),
     (-122, 37), (-124, 46), (-130, 55), (-150, 60), (-162, 62)],
    [(-46, 60), (-32, 68), (-22, 70), (-20, 76), (-30, 82), (-52, 80), (-58, 76), (-54, 69), (-50, 64)],
    [(-78, 7), (-72, 12), (-64, 10), (-55, 6), (-50, 0), (-44, -3), (-35, -8), (-39, -14),
     (-40, -21), (-48, -26), (-55, -33), (-58, -38), (-65, -41), (-66, -47), (-68, -54),
     (-71, -54), (-73, -46), (-73, -37), (-71, -30), (-70, -20), (-75, -15), (-79, -8), (-80, -3), (-78, 2)],
    [(-9, 43), (-2, 44), (-1, 46), (-5, 48), (0, 50), (3, 53), (8, 55), (8, 57), (18, 56),
     (21, 60), (19, 65), (26, 66), (31, 70), (45, 68), (60, 69), (75, 72), (95, 75), (110, 74),
     (130, 72), (155, 70), (170, 67), (178, 66), (178, 62), (162, 56), (156, 51), (142, 46),
     (140, 40), (135, 40), (130, 38), (127, 40), (122, 38), (121, 31), (115, 29), (109, 27),
     (108, 19), (106, 9), (104, 3), (100, 7), (98, 14), (95, 17), (92, 20), (90, 22),
     (88, 21), (86, 20), (83, 18), (80, 14), (77, 8), (75, 14), (72, 19), (70, 22),
     (66, 25), (61, 25), (57, 27), (52, 28), (50, 29), (48, 30), (44, 29), (42, 32),
     (39, 35), (36, 36), (33, 36), (30, 36), (27, 37), (26, 39), (23, 36), (20, 40),
     (16, 38), (15, 40), (12, 44), (9, 44), (7, 44), (3, 43), (0, 39), (-2, 37), (-6, 36), (-9, 37)],
    [(-6, 35), (0, 36), (10, 37), (11, 34), (20, 32), (30, 31), (33, 30), (35, 27),
     (38, 22), (40, 16), (43, 12), (48, 11), (51, 12), (46, 4), (42, -3), (40, -9),
     (40, -15), (38, -21), (35, -25), (32, -29), (27, -33), (20, -35), (17, -32),
     (15, -27), (13, -20), (12, -15), (13, -10), (9, -5), (9, 0), (5, 4), (-3, 5),
     (-8, 5), (-13, 8), (-16, 13), (-17, 16), (-16, 21), (-15, 26), (-13, 29), (-9, 32)],
    [(95, 5), (103, 0), (110, -2), (117, -3), (124, -2), (131, -3), (139, -4), (146, -6),
     (141, -9), (131, -8), (122, -8), (114, -8), (106, -7), (99, -1)],
    [(130, 31), (133, 34), (137, 35), (140, 37), (141, 41), (142, 44), (140, 42), (138, 38), (134, 34), (131, 32)],
    [(-5, 50), (-3, 53), (-2, 56), (-3, 58), (-6, 58), (-8, 55), (-6, 52)],
    [(113, -22), (114, -29), (116, -34), (119, -35), (124, -33), (130, -32), (132, -32),
     (135, -35), (138, -36), (140, -39), (145, -38), (147, -39), (150, -37), (153, -31),
     (153, -27), (151, -24), (146, -19), (143, -15), (142, -11), (140, -14), (136, -15),
     (135, -12), (131, -11), (127, -14), (122, -17), (118, -20)],
    [(167, -46), (171, -43), (173, -41), (175, -39), (176, -37), (174, -37), (172, -41), (169, -46)],
    [(44, -16), (47, -15), (50, -17), (48, -21), (46, -25), (45, -25), (44, -21), (43, -18)],
]
d.rectangle(MAP, fill=(233, 226, 205))
for poly in LAND:
    d.polygon([proj(lon, lat) for lon, lat in poly], fill=(214, 196, 156), outline=(178, 158, 116))
for c in cards:
    if c["pin"]:
        px, py = proj(c["pin"][0], c["pin"][1])
        d.ellipse([px - 8.5, py - 8.5, px + 8.5, py + 8.5], fill=RED, outline=WHITE, width=1)
        text(d, (px, py - 5), str(c["n"]), F(SANSB, 8), WHITE, anchor="ma")
text(d, (MX, 928), "Pin 8 is in space: Mercury orbit.", F(SANS, 9), GRAY)

# ------------------------------------------------------------------ digest
DX = MX + 460
text(d, (DX, 762), "ALSO ON SATURDAY 21 NOVEMBER — 23 MORE STORIES", F(SANSB, 11.5), INK)
dig = DATA["digest"]
cols = [dig[:12], dig[12:]]


def rich_item(x, y, w, item, size):
    fn = F(SANS, size)
    fb = F(SANSB, size)
    parts = [(f"{item['n']} ", fb, RED), (f"{item['place']} — ", fb, INK),
             (item["text"] + " ", fn, (40, 38, 34)), (f"({item['source']})", fn, GRAY)]
    words = []
    for s, fnt, col in parts:
        for w_ in s.split(" "):
            if w_:
                words.append((w_, fnt, col))
    cx, cy = x, y
    for w_, fnt, col in words:
        ww = d.textlength(w_ + " ", font=fnt)
        if cx + ww > x + w and cx > x:
            cx, cy = x, cy + size + 3.4
        d.text((cx, cy), w_, font=fnt, fill=col)
        cx += ww
    return cy + size + 6.5


size = 9.6
for _ in range(6):
    ok = True
    for ci, col_items in enumerate(cols):
        yy = 776
        for it in col_items:
            yy = rich_item(DX + ci * 254, yy, 246, it, size) if False else yy
        # measure pass on a scratch draw
        from PIL import Image as _I
        scratch = _I.new("RGB", (10, 10))
        sd = ImageDraw.Draw(scratch)
        yy = 780
        for it in col_items:
            # replicate rich_item measurement without drawing on main canvas
            fn = F(SANS, size); fb = F(SANSB, size)
            parts = [(f"{it['n']} ", fb), (f"{it['place']} — ", fb),
                     (it["text"] + " ", fn), (f"({it['source']})", fn)]
            cx = 0; lines = 1
            for s, fnt in parts:
                for w_ in s.split(" "):
                    if not w_:
                        continue
                    ww = sd.textlength(w_ + " ", font=fnt)
                    if cx + ww > 246 and cx > 0:
                        lines += 1; cx = 0
                    cx += ww
            yy += lines * (size + 3.4) + 3.1
        if yy > 946:
            ok = False
    if ok:
        break
    size -= 0.4
for ci, col_items in enumerate(cols):
    yy = 780
    for it in col_items:
        yy = rich_item(DX + ci * 254, yy, 246, it, size)

# -------------------------------------------------------------- date check
d.rectangle([MX, 954, W - MX, 986], outline=RED, width=2)
dc = DATA["date_check"]
fnt = F(SANS, 9.8)
fb = F(SANSB, 9.8)
label = "DATE CHECK — "
lw = d.textlength(label, font=fb)
lines = wrap(d, dc, fnt, CW - 24 - lw)
text(d, (MX + 10, 961), label, fb, RED)
for j, ln in enumerate(lines[:2]):
    text(d, (MX + 10 + (lw if j == 0 else 0), 961 + j * 13), ln, fnt, (52, 50, 46))

# ------------------------------------------------------------------ footer
text(d, (MX, 992), "Sources named beside each story · Original drawings made in code · No photographs, no copied artwork.",
     F(SANS, 8.5), GRAY)
text(d, (W - MX, 992), "CONFIRMED = 2+ outlets · OFFICIAL = on the record · REPORTED = one outlet",
     F(SANS, 8.5), GRAY, anchor="ra")

out = os.path.join(HERE, "entry.png")
img.save(out, optimize=True)
import hashlib
raw = open(out, "rb").read()
print("entry.png bytes:", len(raw), "sha256:", hashlib.sha256(raw).hexdigest())
