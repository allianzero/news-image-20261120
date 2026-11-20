#!/usr/bin/env python3
"""Draw the news-image-20261120 front page (1024x1024 PNG) with PIL.

A newspaper front page summing up Friday 20 November 2026's world news.
Every story below happened, or was first reported, on 20 November 2026
(any time zone), verified against live reporting before drawing:

  1. Cyclone Akvan makes landfall near Gopalpur, Odisha, around noon IST;
     winds 90-100 km/h gusting to 110; 300,000+ evacuated, 423 rescue
     teams deployed, 69 trains cancelled (IMD via The Hindu / The Daily Jagran).
  2. COP31 closes in Antalya, Turkiye, after 12 days; nearly 200 countries;
     the "implementation COP" (UN News, 9-20 Nov schedule).
  3. UK-EU summit in Brussels: PM Andy Burnham meets von der Leyen and
     Costa; agrifood trade, emissions-trading linkage and youth mobility
     on the table; package projected at +0.4% of UK GDP (AP / The Guardian).
  4. Cricket, Wellington: Glenn Phillips 118 and Henry Nicholls 146* take
     New Zealand to 317 for 6 at lunch on Day 2 of the first Test v India
     (Reuters, updated 20 Nov 05:50 IST).
  5. UK consumer confidence: GfK index rises 2 points to -22 after
     October's sharp fall (Reuters, 20 Nov 2026).
  Footer: 20 November is World Children's Day (UN observance).

The image is drawn entirely by this script: vector shapes and DejaVu
system fonts, no photograph, no copied artwork.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 242, 231)
INK = (20, 20, 20)
RED = (176, 42, 32)
NAVY = (28, 47, 94)
BLUE = (36, 86, 166)
TEAL = (14, 110, 110)
SKY = (208, 224, 236)
GOLD = (201, 162, 39)
GREY = (96, 90, 78)
LIGHT = (233, 226, 210)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SERIF = FONT_DIR + "DejaVuSerif.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w pixels."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, lines, fnt, fill, leading=None):
    lh = leading or int(fnt.size * 1.22)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- outer frame ----
d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=3)
d.rectangle([18, 18, W - 19, H - 19], outline=INK, width=1)

# ================= MASTHEAD =================
d.text((W // 2, 40), "T H E   W O R L D   I N   O N E   I M A G E",
       font=font(SANS_B, 23), fill=RED, anchor="ma")
d.text((W // 2, 74), "20 NOVEMBER 2026", font=font(SERIF_B, 74),
       fill=INK, anchor="ma")
d.line([(60, 164), (W - 60, 164)], fill=INK, width=3)
d.line([(60, 170), (W - 60, 170)], fill=INK, width=1)
d.text((W // 2, 182), "FRIDAY  \u2022  THE DAY'S WORLD NEWS, AT A GLANCE",
       font=font(SANS_B, 20), fill=NAVY, anchor="ma")

# ================= LEAD: CYCLONE AKVAN =================
lx, ly, lw, lh = 30, 212, W - 60, 202
d.rectangle([lx, ly, lx + lw, ly + lh], outline=INK, width=2)
d.text((48, 226), "INDIA  \u2022  SEVERE CYCLONE", font=font(SANS_B, 19),
       fill=RED)
d.text((48, 252), "CYCLONE AKVAN HITS", font=font(SERIF_B, 43), fill=INK)
d.text((48, 300), "INDIA'S EAST COAST", font=font(SERIF_B, 43), fill=INK)
lead_dek = ("Severe storm crosses the Odisha coast near Gopalpur at noon, "
            "winds 90\u2013100 km/h. Over 300,000 evacuated; 423 rescue "
            "teams out; 69 trains cancelled.")
block(d, 48, 350, wrap(d, lead_dek, font(SANS, 18), 556),
      font(SANS, 18), INK, leading=22)

# ---- cyclone illustration, right of the lead ----
ax0, ay0, ax1, ay1 = 622, 226, 978, 400
d.rectangle([ax0, ay0, ax1, ay1], fill=SKY, outline=NAVY, width=2)
cx, cy = 800, 312
# spiral bands
for i, r in enumerate(range(14, 86, 9)):
    a0 = 20 + i * 38
    col = NAVY if i % 3 == 0 else (TEAL if i % 3 == 1 else (255, 255, 255))
    d.arc([cx - r, cy - r, cx + r, cy + r], start=a0, end=a0 + 250,
          fill=col, width=6)
d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(255, 255, 255),
          outline=NAVY, width=2)
# rain streaks
for x0, y0 in [(650, 250), (690, 240), (730, 258), (880, 245), (920, 258),
               (950, 240)]:
    d.line([(x0, y0), (x0 - 8, y0 + 22)], fill=BLUE, width=3)
# sea + coast at the bottom of the panel
d.rectangle([ax0 + 2, 368, ax1 - 2, ay1 - 2], fill=NAVY)
for wx in range(ax0 + 12, ax1 - 10, 26):
    d.arc([wx, 372, wx + 22, 388], start=200, end=340, fill=(255, 255, 255),
          width=2)
d.ellipse([872 - 5, 372 - 5, 872 + 5, 372 + 5], fill=RED,
          outline=(255, 255, 255), width=2)
d.text((634, 336), "GOPALPUR", font=font(SANS_B, 15), fill=NAVY)

# ================= GRID: 2 x 2 =================
CELL_W, CELL_H = 467, 214
CELLS = [
    # (x, y, accent, kicker, headline, dek, icon)
    (30, 430, TEAL, "TURKIYE  \u2022  CLIMATE",
     "COP31 CLOSES IN ANTALYA",
     "UN climate talks end today after 12 days. Nearly 200 countries "
     "raced to land a deal on climate finance.", "globe"),
    (527, 430, NAVY, "BRUSSELS  \u2022  EUROPE",
     "BURNHAM MEETS EU LEADERS",
     "UK and EU sign off trade, emissions and youth-mobility deals; "
     "the package is put at +0.4% of GDP.", "stars"),
    (30, 660, (34, 120, 58), "WELLINGTON  \u2022  CRICKET",
     "PHILLIPS TON PUTS NZ ON TOP",
     "Glenn Phillips 118 and Henry Nicholls 146* take New Zealand to "
     "317 for 6 at lunch on Day 2.", "stumps"),
    (527, 660, GOLD, "LONDON  \u2022  ECONOMY",
     "UK SHOPPERS' MOOD LIFTS",
     "Consumer confidence rises 2 points to -22 after October's sharp "
     "fall, the GfK survey finds.", "bars"),
]


def draw_icon(kind, x, y):
    """Small 56x40 pictogram at the bottom-right of a cell."""
    if kind == "globe":
        d.ellipse([x + 6, y, x + 50, y + 40], outline=TEAL, width=3)
        d.ellipse([x + 18, y, x + 38, y + 40], outline=TEAL, width=2)
        d.line([(x + 6, y + 20), (x + 50, y + 20)], fill=TEAL, width=2)
        d.line([(x + 12, y + 10), (x + 44, y + 10)], fill=TEAL, width=1)
        d.line([(x + 12, y + 30), (x + 44, y + 30)], fill=TEAL, width=1)
    elif kind == "stars":
        import math
        for k in range(12):
            ang = 2 * math.pi * k / 12 - math.pi / 2
            sx = x + 28 + int(19 * math.cos(ang))
            sy = y + 20 + int(19 * math.sin(ang))
            d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=GOLD)
    elif kind == "stumps":
        d.ellipse([x + 2, y + 2, x + 54, y + 38], outline=(34, 120, 58),
                  width=2)
        for i, sx in enumerate((x + 20, x + 28, x + 36)):
            d.line([(sx, y + 8), (sx, y + 30)], fill=(201, 162, 39), width=3)
        d.ellipse([x + 42, y + 26, x + 52, y + 36], fill=RED)
    elif kind == "bars":
        for i, bh in enumerate((14, 24, 34)):
            bx = x + 6 + i * 16
            d.rectangle([bx, y + 40 - bh, bx + 11, y + 40], fill=NAVY)
        d.line([(x + 2, y + 6), (x + 52, y + 2)], fill=RED, width=3)


for (cx0, cy0, accent, kicker, head, dek, icon) in CELLS:
    d.rectangle([cx0, cy0, cx0 + CELL_W, cy0 + CELL_H], outline=INK, width=1)
    d.rectangle([cx0, cy0, cx0 + CELL_W, cy0 + 5], fill=accent)
    d.text((cx0 + 16, cy0 + 16), kicker, font=font(SANS_B, 16), fill=accent)
    head_lines = wrap(d, head, font(SERIF_B, 29), CELL_W - 32)
    hy = block(d, cx0 + 16, cy0 + 42, head_lines, font(SERIF_B, 29), INK,
               leading=34)
    block(d, cx0 + 16, hy + 6,
          wrap(d, dek, font(SANS, 18), CELL_W - 32),
          font(SANS, 18), INK, leading=23)
    draw_icon(icon, cx0 + CELL_W - 72, cy0 + CELL_H - 52)

# ================= FOOTER =================
d.line([(30, 902), (W - 30, 902)], fill=INK, width=2)
d.text((30, 916), "ALSO TODAY:  ", font=font(SANS_B, 19), fill=RED)
d.text((178, 916),
       "World Children's Day \u2014 20 November is the UN's day for "
       "children's rights.",
       font=font(SANS, 19), fill=INK)
d.text((30, 950),
       "Sources, Friday 20 November 2026: IMD / The Hindu \u2022 Reuters "
       "\u2022 AP \u2022 UN News \u2014 image drawn by hand with code.",
       font=font(SANS, 15), fill=GREY)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size, img.mode)
