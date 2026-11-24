#!/usr/bin/env python3
"""News front page for Tuesday 24 November 2026 (make.fun news-image-20261124).
Drawn fresh with PIL: light paper, serif masthead, 3 headlines + 10 secondary
+ 28 briefs, UTC timeline, dot-matrix world map, DATE CHECK box.
Reads stories.json next to this file, writes entry.png next to it.
Deterministic: no timestamps, no randomness."""
import json
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
M = 24                      # side margin
CW = W - 2 * M              # content width 976
PAPER = "#f7f3e8"
CARD = "#fffdf6"
INK = "#111111"
GREY = "#555555"
RED = "#b91c1c"
LINE = "#c9c2ae"
DOT = "#948a74"
BADGE = {"CONFIRMED": "#15803d", "REPORTED": "#1d4ed8",
         "CLAIM": "#b45309", "FORECAST": "#6d28d9", "OFFICIAL": "#0f766e"}
FONTDIR = "/usr/share/fonts/truetype/dejavu"


def f_serif_b(size):
    return ImageFont.truetype(f"{FONTDIR}/DejaVuSerif-Bold.ttf", size)


def f_serif(size):
    return ImageFont.truetype(f"{FONTDIR}/DejaVuSerif.ttf", size)


def f_sans(size):
    return ImageFont.truetype(f"{FONTDIR}/DejaVuSans.ttf", size)


def f_sans_b(size):
    return ImageFont.truetype(f"{FONTDIR}/DejaVuSans-Bold.ttf", size)


def tw(draw, text, font):
    return draw.textlength(text, font=font)


def cut(draw, text, font, maxw, ell="..."):
    """Shorten text with an ellipsis so it fits maxw pixels."""
    if tw(draw, text, font) <= maxw:
        return text
    while text and tw(draw, text + ell, font) > maxw:
        text = text[:-1]
    return text + ell


def wrap(draw, text, font, maxw, max_lines):
    """Greedy word wrap, at most max_lines lines; last line gets an ellipsis."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if tw(draw, trial, font) <= maxw:
            cur = trial
        else:
            lines.append(cur)
            cur = word
            if len(lines) == max_lines:
                return lines
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = cut(draw, lines[-1], font, maxw)
    return lines


def badge(draw, x, y, label):
    """Small coloured verification badge; returns width used."""
    font = f_sans_b(9)
    w = int(tw(draw, label, font)) + 10
    h = 14
    draw.rounded_rectangle([x, y, x + w, y + h], radius=3,
                           fill=BADGE[label])
    draw.text((x + 5, y + 2), label, font=font, fill="white")
    return w


def num_dot(draw, cx, cy, n, r=11):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    font = f_sans_b(13)
    t = str(n)
    draw.text((cx - tw(draw, t, font) / 2, cy - 8), t, font=font, fill="white")


def rule(draw, y, x0=M, x1=W - M, fill=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- illustrations
def ill_gaza(d, x, y, w, h):
    """Coastline, rooftops, red blast star, smoke."""
    d.rectangle([x, y, x + w, y + h], fill="#efe8d6")
    d.line([(x, y + h - 18), (x + w, y + h - 18)], fill="#8fa3b8", width=3)
    d.rectangle([x, y + h - 18, x + w, y + h], fill="#b8d0de")
    for bx, bw, bh in [(10, 70, 46), (90, 60, 62), (160, 78, 38), (248, 54, 52)]:
        d.rectangle([x + bx, y + h - 18 - bh, x + bx + bw, y + h - 18],
                    fill="#c9b896", outline="#8a7a5c")
        for wx in range(bx + 10, bx + bw - 6, 20):
            d.rectangle([x + wx, y + h - 18 - bh + 8, x + wx + 8,
                         y + h - 10 - bh + 16], fill="#5c5238")
    cx, cy = x + 250, y + 26
    for k in range(8):
        import math
        a = k * math.pi / 4
        d.line([(cx - 20 * math.cos(a), cy - 20 * math.sin(a)),
                (cx + 20 * math.cos(a), cy + 20 * math.sin(a))],
               fill=RED, width=3)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill="#f59e0b")
    for sx, sy, sr in [(x + 60, y + 22, 10), (x + 78, y + 12, 13),
                       (x + 100, y + 24, 8)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill="#9aa0a6")


def ill_market(d, x, y, w, h):
    """Rising line chart, candlesticks, chip."""
    d.rectangle([x, y, x + w, y + h], fill="#e8f0e4")
    for gy in (y + 22, y + 50, y + 78):
        d.line([(x + 12, gy), (x + w - 12, gy)], fill="#c6d4c2", width=1)
    pts = [(x + 12, y + 84), (x + 62, y + 70), (x + 112, y + 74),
           (x + 162, y + 46), (x + 212, y + 50), (x + 262, y + 24),
           (x + w - 12, y + 12)]
    d.line(pts, fill="#15803d", width=4)
    d.ellipse([pts[-1][0] - 5, pts[-1][1] - 5, pts[-1][0] + 5,
               pts[-1][1] + 5], fill=RED)
    d.rectangle([x + 34, y + 14, x + 70, y + 38], fill="#1f2937")
    for px in range(x + 40, x + 66, 8):
        d.line([(px, y + 19), (px, y + 33)], fill="#4ade80", width=2)


def ill_records(d, x, y, w, h):
    """Rising bar chart with a document."""
    d.rectangle([x, y, x + w, y + h], fill="#ece4d4")
    d.line([(x + 16, y + 88), (x + 200, y + 88)], fill="#8a7a5c", width=2)
    bars = [(26, 30, "#7f1d1d"), (62, 46, "#991b1b"), (98, 58, "#b91c1c"),
            (134, 76, "#dc2626"), (170, 92, "#ef4444")]
    for bx, bh, c in bars:
        d.rectangle([x + bx, y + 88 - bh, x + bx + 24, y + 88], fill=c)
    d.rectangle([x + 216, y + 12, x + 292, y + 92], fill="white",
                outline="#8a7a5c")
    d.rectangle([x + 216, y + 12, x + 292, y + 28], fill="#1f2937")
    for ly in (42, 54, 66, 78):
        d.line([(x + 224, y + ly), (x + 284, y + ly)], fill="#9aa0a6", width=3)
    d.rectangle([x + 224, y + 84, x + 258, y + 92], fill=RED)


ILLUS = {"gaza": ill_gaza, "market": ill_market, "records": ill_records}


def icon(d, x, y, name):
    """Small 187x30 flat icon for a secondary story."""
    c = "#1f2937"
    if name == "ball":
        d.ellipse([x + 6, y + 2, x + 28, y + 28], outline=c, width=2)
        d.polygon([(x + 17, y + 10), (x + 24, y + 15), (x + 21, y + 23),
                   (x + 13, y + 23), (x + 10, y + 15)], fill=c)
        for px, py in [(17, 6), (25, 11), (25, 21), (17, 27), (9, 21), (9, 11)]:
            d.line([(x + 17, y + 15), (x + px, y + py)], fill=c, width=1)
    elif name == "dome":
        d.arc([x + 4, y + 4, x + 30, y + 26], 180, 360, fill=c, width=2)
        d.line([(x + 2, y + 24), (x + 32, y + 24)], fill=c, width=2)
        for bx in (7, 14, 21, 28):
            d.line([(x + bx, y + 16), (x + bx, y + 24)], fill=c, width=2)
        d.line([(x + 17, y + 2), (x + 17, y + 5)], fill=c, width=2)
    elif name == "pad":
        d.rectangle([x + 6, y + 8, x + 28, y + 22], fill=c)
        d.rectangle([x + 4, y + 12, x + 8, y + 18], fill=c)
        d.rectangle([x + 26, y + 12, x + 30, y + 18], fill=c)
        d.polygon([(x + 17, y + 13), (x + 20, y + 16), (x + 14, y + 16)],
                  fill="white")
        d.ellipse([x + 21, y + 14, x + 24, y + 17], fill="white")
    elif name == "flag":
        d.line([(x + 8, y + 2), (x + 8, y + 28)], fill=c, width=2)
        d.rectangle([x + 8, y + 3, x + 30, y + 18], fill="#1d4ed8")
        d.rectangle([x + 8, y + 3, x + 30, y + 8], fill="#1d4ed8")
        d.rectangle([x + 8, y + 8, x + 30, y + 13], fill="white")
        d.rectangle([x + 8, y + 13, x + 30, y + 18], fill=RED)
    elif name == "chip":
        d.rectangle([x + 8, y + 8, x + 26, y + 22], fill=c)
        d.rectangle([x + 13, y + 13, x + 21, y + 17], fill="#4ade80")
        for px in (12, 18, 24):
            d.line([(x + px, y + 4), (x + px, y + 8)], fill=c, width=2)
            d.line([(x + px, y + 22), (x + px, y + 26)], fill=c, width=2)
    elif name == "lens":
        d.ellipse([x + 6, y + 6, x + 24, y + 24], outline=c, width=2)
        d.line([(x + 21, y + 21), (x + 30, y + 28)], fill=c, width=3)
        d.arc([x + 10, y + 10, x + 20, y + 20], 200, 320, fill=c, width=2)
    elif name == "chat":
        d.rectangle([x + 4, y + 6, x + 26, y + 20], outline=c, width=2)
        d.polygon([(x + 10, y + 20), (x + 10, y + 26), (x + 16, y + 20)],
                  fill=c)
        d.line([(x + 8, y + 11), (x + 22, y + 11)], fill=c, width=2)
        d.line([(x + 8, y + 15), (x + 18, y + 15)], fill=c, width=2)
    elif name == "gate":
        d.line([(x + 6, y + 4), (x + 6, y + 26)], fill=c, width=2)
        d.line([(x + 28, y + 4), (x + 28, y + 26)], fill=c, width=2)
        d.line([(x + 6, y + 6), (x + 28, y + 6)], fill=c, width=2)
        for gx in (12, 18, 24):
            d.line([(x + gx, y + 6), (x + gx, y + 26)], fill=c, width=1)
    elif name == "wheat":
        d.line([(x + 17, y + 6), (x + 17, y + 28)], fill=c, width=2)
        for k in range(4):
            yy = y + 7 + k * 5
            d.ellipse([x + 10, yy, x + 17, yy + 5], fill="#b45309")
            d.ellipse([x + 17, yy, x + 24, yy + 5], fill="#b45309")
    elif name == "bot":
        d.rectangle([x + 7, y + 9, x + 27, y + 24], outline=c, width=2)
        d.ellipse([x + 12, y + 14, x + 15, y + 17], fill=c)
        d.ellipse([x + 19, y + 14, x + 22, y + 17], fill=c)
        d.line([(x + 13, y + 20), (x + 21, y + 20)], fill=c, width=2)
        d.line([(x + 12, y + 5), (x + 12, y + 9)], fill=c, width=2)
        d.line([(x + 22, y + 5), (x + 22, y + 9)], fill=c, width=2)


# ---------------------------------------------------------------- world map
# 62 x 26 dot grid; row = int((90 - lat) / 180 * 26), col = int((lon + 180) / 360 * 62)
MAP_ROWS = [
    ".....#####...........####...............#######.....####......",
    "....#############...#######...........#####################...",
    "..######...........#####....####....#######################.",
    "..#####.............#..#####.#########################.",
    ".....################.......##.#########################.",
    "......###############.......###############################...",
    ".......##############........##############################...",
    "........############.........##########################.##....",
    ".........##########..........############################.....",
    "........######...............###############.##########.......",
    "..........#####..............##########.......###.#####.......",
    "............####.............#####.####...........####........",
    "..............#####...........########............#######.....",
    "...............######..........######.............########....",
    "...............########........######...............#######...",
    "................########.......#####.##.............######....",
    "................#######........#####.#............#########...",
    "................#####...........###...............##########..",
    ".................###......................................##..",
    "..................#.......................................#...",
    "..................#...........................................",
    "..............................................................",
    "..............................................................",
    "..............................................................",
    "..............................................................",
    "..............................................................",
]
MAP_POINTS = [("Moscow", 37, 4), ("Khan Younis", 37, 8), ("Seoul", 53, 7)]


def draw_map(d, x, y):
    cell = 4
    for r, row in enumerate(MAP_ROWS):
        for c, ch in enumerate(row):
            if ch == "#":
                d.ellipse([x + c * cell + 1, y + r * cell + 1,
                           x + c * cell + 3, y + r * cell + 3], fill=DOT)
    for n, (name, col, row) in enumerate(MAP_POINTS, 1):
        cx, cy = x + col * cell + 2, y + row * cell + 2
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED)
        d.text((cx - 2, cy - 8), str(n), font=f_sans_b(10), fill="white")




# ---------------------------------------------------------------- layout
def header(d, s):
    d.text((M, 10), s["count_line"], font=f_sans_b(13), fill=RED)
    rule(d, 32, width=1)
    size = 58
    while tw(d, s["date"], f_serif_b(size)) > CW and size > 30:
        size -= 1
    d.text((M, 38), s["date"], font=f_serif_b(size), fill=INK)
    rule(d, 104, width=3)
    rule(d, 107, width=1)
    sub = wrap(d, s["subhead"], f_serif(15), CW, 2)
    for i, line in enumerate(sub):
        d.text((M, 112 + i * 20), line, font=f_serif(15), fill=GREY)


def timeline(d, s):
    d.text((M, 132), "TODAY IN UTC", font=f_sans_b(12), fill=RED)
    d.text((M, 148), "Events as the day unfolded", font=f_serif(11), fill=GREY)
    x0, x1, ly = 150, 1000, 160
    d.line([(x0, ly), (x1, ly)], fill=INK, width=2)
    for item in s["timeline"]:
        hh, mm = map(int, item["utc"].split(":"))
        frac = (hh * 60 + mm) / 1440.0
        px = x0 + frac * (x1 - x0)
        d.ellipse([px - 4, ly - 4, px + 4, ly + 4], fill=RED)
    legend = "  ·  ".join(f'{it["utc"]} {it["label"]}' for it in s["timeline"])
    d.text((x0, 174), legend, font=f_sans(10), fill=INK)
    rule(d, 190, width=1)


def headlines(d, s):
    colw, gap = 312, 20
    for i, h in enumerate(s["headlines"]):
        x = M + i * (colw + gap)
        num_dot(d, x + 11, 208, h["n"])
        d.text((x + 28, 198), h["tag"], font=f_sans_b(12), fill=RED)
        d.text((x + 28, 214), h["region"], font=f_sans_b(10), fill=GREY)
        ILLUS[h["illus"]](d, x, 232, colw, 108)
        title = wrap(d, h["title"], f_serif_b(21), colw, 3)
        for j, line in enumerate(title):
            d.text((x, 348 + j * 26), line, font=f_serif_b(21), fill=INK)
        body = wrap(d, h["body"], f_sans(12), colw, 2)
        for j, line in enumerate(body):
            d.text((x, 430 + j * 15), line, font=f_sans(12), fill=GREY)
        bw = badge(d, x, 468, h["badge"])
        d.text((x + bw + 8, 469), h["source"], font=f_sans_b(11), fill=GREY)


def numbers_bar(d, s):
    rule(d, 490, width=1)
    cell = CW // 4
    for i, n in enumerate(s["numbers"]):
        x = M + i * cell
        d.text((x + 6, 498), n["value"], font=f_serif_b(24), fill=RED)
        d.text((x + 6, 528), cut(d, n["caption"], f_sans(11), cell - 12),
               font=f_sans(11), fill=GREY)
        if i:
            d.line([(x, 496), (x, 540)], fill=LINE, width=1)
    rule(d, 540, width=1)


def secondary(d, s):
    colw, gap = 187, 10
    for i, sec in enumerate(s["secondary"]):
        row, col = divmod(i, 5)
        x = M + col * (colw + gap)
        y = 548 + row * 90
        d.text((x, y), sec["tag"], font=f_sans_b(10), fill=RED)
        d.text((x, y + 13), sec["region"], font=f_sans_b(9), fill=GREY)
        title = wrap(d, sec["title"], f_serif_b(13), colw, 2)
        for j, line in enumerate(title):
            d.text((x, y + 27 + j * 15), line, font=f_serif_b(13), fill=INK)
        icon(d, x, y + 56, sec["icon"])
        body = cut(d, sec["body"], f_sans(10), colw - 34)
        d.text((x + 36, y + 63), body, font=f_sans(10), fill=GREY)
        bw = badge(d, x, y + 76, sec["badge"])
        d.text((x + bw + 6, y + 77), sec["source"], font=f_sans(9),
               fill=GREY)
    rule(d, 734, width=1)


def bottom_band(d, s):
    d.text((M, 742), "WHERE IT HAPPENED", font=f_sans_b(12), fill=RED)
    draw_map(d, M, 760)
    d.text((M, 872), "1 Khan Younis  2 Seoul  3 Moscow", font=f_sans(10),
           fill=GREY)
    d.text((M, 886), "Dot grid: 62 x 26, one dot per 4 px.", font=f_sans(9),
           fill=GREY)
    d.text((M, 900), "N. AMERICA 8 · EUROPE 7 · ASIA 10", font=f_sans_b(10),
           fill=INK)
    d.text((M, 912), "M. EAST 8 · AFRICA 2 · S. AMERICA 3 · OCEANIA 3",
           font=f_sans_b(10), fill=INK)
    x = 332
    d.text((x, 742), "THE REST OF THE DAY", font=f_sans_b(12), fill=RED)
    for i, b in enumerate(s["briefs"]):
        col, r = divmod(i, 14)
        bx = x + col * 330
        by = int(760 + r * 11.5)
        t = f"{b['n']}. {b['text']}"
        d.text((bx, by), cut(d, t, f_sans(11), 328), font=f_sans(11),
               fill=INK)


def datecheck(d, s):
    """DATE CHECK box: 2 columns x 4 rows, below the briefs."""
    x, y, w, h = 332, 922, 668, 70
    d.rectangle([x, y, x + w, y + h], outline=RED, width=2, fill=CARD)
    dc = s["datecheck"]
    d.text((x + 10, y + 5), dc["title"], font=f_sans_b(11), fill=RED)
    items = [(f"\u2715 {e['text']}", e["date"]) for e in dc["excluded"]]
    items += [(f"Not yet: {e['text']}", e["date"]) for e in dc["notyet"]]
    for i, (txt, date) in enumerate(items):
        col, r = divmod(i, 4)
        ix = x + 10 + col * 334
        iy = y + 22 + r * 12
        d.text((ix, iy), cut(d, txt, f_sans(11), 240), font=f_sans(11),
               fill=INK)
        d.text((ix + 244, iy), date, font=f_sans(11), fill=GREY)


def footer(d, s):
    rule(d, 1000, width=1)
    d.text((M, 1006), s["oath"], font=f_serif(10), fill=GREY)
    d.text((M, 1014), s["sources"], font=f_sans(8), fill=GREY)


def main():
    with open(os.path.join(HERE, "stories.json"), encoding="utf-8") as f:
        s = json.load(f)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    header(d, s)
    timeline(d, s)
    headlines(d, s)
    numbers_bar(d, s)
    secondary(d, s)
    bottom_band(d, s)
    datecheck(d, s)
    footer(d, s)
    out = os.path.join(HERE, "entry.png")
    img.save(out)
    print(f"wrote {out} {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
