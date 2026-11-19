#!/usr/bin/env python3
"""Render entry.png for make.fun news-image-20261119.

Build-time script only: it renders the newspaper front page with Pillow
from the system fonts and writes entry.png beside it. The graded entry is
main.py, which only copies entry.png to the output directory (stdlib only,
no network, deterministic). Run: python3 gen_image.py

Content: 32 verified stories of Thursday 19 November 2026 — lead GTA VI
launch day, 4 feature panels (Jeffries historic nomination, Anthropic's
record $81.3bn IPO, Crimean Bridge struck a third time, Trump-Xi-Putin
trilateral at the APEC summit in Shenzhen) + 27 briefs across six
continents, all events of / first reported on 19 Nov 2026.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (20, 20, 20)
NAVY = (20, 33, 61)
NAVY2 = (27, 45, 82)
GOLD = (201, 162, 39)
RED = (185, 28, 28)
PURPLE = (120, 40, 180)
WHITE = (255, 255, 255)
GREY = (90, 90, 90)
CARD = (255, 255, 255)
RULE = (214, 204, 178)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def one_line(draw, text, fnt, max_w, what):
    """Wrap and assert the text fits on exactly one line."""
    lines = wrap(draw, text, fnt, max_w)
    assert len(lines) == 1, (what, lines)
    return lines[0]


def draw_gamepad(d, cx, cy, s):
    """Simple game controller icon, centred at (cx, cy), size s."""
    w, h = int(s * 1.5), int(s * 0.85)
    x0, y0 = cx - w // 2, cy - h // 2
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=18, fill=PURPLE)
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=18, outline=(70, 20, 110), width=3)
    # d-pad (plus sign) on the left
    px, py = x0 + 26, y0 + h // 2
    d.rectangle([px - 4, py - 12, px + 4, py + 12], fill=WHITE)
    d.rectangle([px - 12, py - 4, px + 12, py + 4], fill=WHITE)
    # four buttons on the right
    for bx, by in [(x0 + w - 34, y0 + 14), (x0 + w - 20, y0 + 28),
                   (x0 + w - 48, y0 + 28), (x0 + w - 34, y0 + 42)]:
        d.ellipse([bx - 5, by - 5, bx + 5, by + 5], fill=GOLD)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.rectangle([0, 118, W, 122], fill=GOLD)
    f_title = font(SERIF, 56)
    t = "THE WORLD IN ONE PAGE"
    d.text(((W - d.textlength(t, font=f_title)) / 2, 14), t, font=f_title, fill=WHITE)
    f_date = font(SANS_B, 23)
    t2 = "THURSDAY, 19 NOVEMBER 2026  •  32 STORIES  •  SIX CONTINENTS"
    if d.textlength(t2, font=f_date) > 990:
        f_date = font(SANS_B, 21)
    d.text(((W - d.textlength(t2, font=f_date)) / 2, 80), t2, font=f_date, fill=GOLD)

    # ---- lead story: GTA VI launch day ----
    x0, y0, x1, y1 = 28, 134, 996, 318
    d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=CARD, outline=(200, 190, 160), width=2)
    f_kick = font(SANS_B, 19)
    kick = "LEAD STORY  •  CULTURE"
    d.rectangle([x0 + 14, y0 + 14, x0 + 14 + d.textlength(kick, font=f_kick) + 20, y0 + 40], fill=PURPLE)
    d.text((x0 + 24, y0 + 17), kick, font=f_kick, fill=WHITE)
    f_head = font(SERIF, 38)
    d.text((x0 + 16, y0 + 46), "Vice City opens: GTA VI", font=f_head, fill=INK)
    d.text((x0 + 16, y0 + 90), "launches worldwide", font=f_head, fill=INK)
    f_body = font(SANS, 20)
    body = ("Rockstar's epic lands on PS5 and Xbox; first reviews score 99/100 "
            "as 2.3m watch on Twitch.")
    lines = wrap(d, body, f_body, 680)
    assert len(lines) <= 2, lines
    yy = y0 + 134
    for ln in lines[:2]:
        d.text((x0 + 16, yy), ln, font=f_body, fill=(40, 40, 40))
        yy += 24
    # gamepad icon, right side
    draw_gamepad(d, 880, 222, 110)
    d.ellipse([818, 160, 942, 284], outline=PURPLE, width=4)

    # ---- four feature panels, 2 cols x 2 rows ----
    panels = [
        ("USA  •  POLITICS", (185, 28, 28),
         "Jeffries makes history",
         "Democrats nominate Hakeem Jeffries 251–11; first Black Speaker in January.", "ballot"),
        ("MARKETS  •  TECH", NAVY2,
         "Anthropic's $81.3bn IPO",
         "Biggest IPO ever: priced at $83, valued at $1.5tn; shares debut on Nasdaq today.", "chart"),
        ("EUROPE  •  UKRAINE WAR", (185, 28, 28),
         "Bridge hit a third time",
         "Crimean Bridge struck overnight again; traffic halted, third attack in a week.", "bridge"),
        ("ASIA  •  DIPLOMACY", NAVY2,
         "Trump, Xi and Putin meet",
         "APEC summit hosts a trilateral; Trump arrives as leaders meet in Shenzhen.", "summit"),
    ]
    px, py = 28, 330
    pw, ph, gap = 478, 144, 12
    f_pk = font(SANS_B, 16)
    f_ph = font(SERIF, 26)
    f_pb = font(SANS, 18)
    for i, (kick, col, head, body, icon) in enumerate(panels):
        cx = px + (i % 2) * (pw + gap)
        cy = py + (i // 2) * (ph + gap)
        d.rounded_rectangle([cx, cy, cx + pw, cy + ph], radius=10, fill=CARD,
                            outline=(200, 190, 160), width=2)
        d.rectangle([cx, cy, cx + pw, cy + 6], fill=col)
        d.text((cx + 14, cy + 14), kick, font=f_pk, fill=col)
        hl = wrap(d, head, f_ph, pw - 28)
        assert len(hl) <= 2, (head, hl)
        yy = cy + 40
        for ln in hl[:2]:
            d.text((cx + 14, yy), ln, font=f_ph, fill=INK)
            yy += 31
        bl = wrap(d, body, f_pb, pw - 28)
        assert len(bl) <= 2, (head, bl)
        for ln in bl[:2]:
            d.text((cx + 14, yy), ln, font=f_pb, fill=(40, 40, 40))
            yy += 23
        ix, iy = cx + pw - 44, cy + 32
        if icon == "bridge":
            d.line([ix - 30, iy + 14, ix - 10, iy - 2, ix + 12, iy - 2, ix + 32, iy + 14],
                   fill=NAVY, width=4)
            d.line([ix - 30, iy + 14, ix + 32, iy + 14], fill=NAVY, width=4)
            d.line([ix - 2, iy - 2, ix + 5, iy + 14], fill=RED, width=3)
        elif icon == "summit":
            for j, c in enumerate([(185, 28, 28), (30, 90, 160), (201, 162, 39)]):
                d.ellipse([ix - 28 + j * 24, iy - 6 + (0 if j == 1 else 8), ix - 6 + j * 24,
                           iy + 16 + (0 if j == 1 else 8)], fill=c)
        elif icon == "ballot":
            d.rectangle([ix - 28, iy - 4, ix + 26, iy + 26], outline=NAVY, width=4)
            d.line([ix - 20, iy + 10, ix - 6, iy + 22, ix + 22, iy - 12], fill=(6, 120, 90), width=5)
        elif icon == "chart":
            for j, hgt in enumerate([14, 24, 36]):
                d.rectangle([ix - 26 + j * 18, iy + 30 - hgt, ix - 12 + j * 18, iy + 30],
                            fill=NAVY2 if j < 2 else GOLD)
            d.line([ix - 28, iy - 2, ix - 8, iy - 12, ix + 12, iy - 22], fill=RED, width=3)

    # ---- briefs: 27 one-liners, 3 cols x 9 rows ----
    briefs = [
        ("ICJ", "Rohingya ruling due", "Court to decide Myanmar genocide case."),
        ("KOREA", "North Korea fires missiles", "Missiles fly after US-South Korea drill."),
        ("GAZA", "Aid access demanded", "Flooded Gaza needs open crossings."),
        ("ISRAEL", "Eisenkot tapped to lead", "President bypasses Netanyahu for PM."),
        ("VENEZUELA", "US details $12bn oil", "Report tracks Maduro-era revenues."),
        ("FRANCE", "Fourth week of protests", "Cost-of-living rallies roll on."),
        ("EU", "Indonesia trade pact cleared", "Deal counters US tariffs."),
        ("UKRAINE", "EU plans €45bn loan", "Kyiv aid tied to Russian reparations."),
        ("USA", "NSA outage hits Iran intel", "Middle East links disrupted."),
        ("USA", "Iran 'seeks bioweapons'", "President raises the stakes."),
        ("USA", "Senators warn on AI cyber", "AI threats outpace US defences."),
        ("CANADA", "Carney rethinks China", "Ottawa seeks the right US deal."),
        ("FRANCE", "Mélenchon 'could win'", "Justice minister's warning."),
        ("SAUDI", "Danger passed", "Alerts lifted in three cities."),
        ("LIBYA", "Cocaine, pills seized", "Millions of pills found in east."),
        ("KENYA", "Drought hits milk supply", "Prices climb as herds suffer."),
        ("SOMALIA", "Reforms spark row", "Constitution crisis deepens."),
        ("INDIA", "Sindhu back in top five", "Badminton star climbs again."),
        ("INDIA", "Cyclone Akvan nears coast", "Odisha braces for landfall."),
        ("JAPAN", "India-Japan defence talks", "2+2 dialogue opens in Tokyo."),
        ("UK", "Lords debate Jewish safety", "Security tensions aired."),
        ("ALPS", "Climber survives 100m fall", "German climber's miracle escape."),
        ("BERLIN", "Woman charged as spy", "Ilona W. 'fed Russia secrets'."),
        ("SPACE", "ESA chief wants space laws", "Call for satellite surveillance."),
        ("AUSTRALIA", "General Pants folds", "Retailer enters administration."),
        ("USA", "Helicopter flew too low", "NTSB on Biscayne Bay crash."),
        ("USA", "Palantir spy charge", "Russian held over staff spying."),
    ]
    assert len(briefs) == 27, len(briefs)

    bx0, by0 = 28, 642
    f_bh = font(SANS_B, 18)
    d.text((bx0, by0), "MORE FROM THE DAY", font=f_bh, fill=NAVY)
    f_bs = font(SANS, 16)
    d.text((bx0 + d.textlength("MORE FROM THE DAY  ", font=f_bh), by0 + 2),
           "— 27 briefs, six continents", font=f_bs, fill=GREY)
    d.line([bx0, by0 + 26, 996, by0 + 26], fill=NAVY, width=2)

    cols, rows = 3, 9
    cw = (996 - 28 - (cols - 1) * 12) // cols
    rh = 35
    gy = by0 + 34
    f_b1 = font(SANS_B, 15)
    f_b2 = font(SANS, 13)
    for i, (tag, head, sub) in enumerate(briefs):
        col, row = i % cols, i // cols
        x = bx0 + col * (cw + 12)
        y = gy + row * rh
        line1 = one_line(d, tag + " — " + head, f_b1, cw, ("brief head", head))
        # draw the tag in red, the headline in ink, on the same line
        tag_txt = tag + " — "
        d.text((x, y), tag_txt, font=f_b1, fill=RED)
        d.text((x + d.textlength(tag_txt, font=f_b1), y), head, font=f_b1, fill=INK)
        one_line(d, sub, f_b2, cw, ("brief sub", sub))
        d.text((x, y + 18), sub, font=f_b2, fill=(60, 60, 60))
        if row < rows - 1:
            d.line([x, y + rh - 6, x + cw, y + rh - 6], fill=RULE, width=1)

    # ---- footer ----
    f_f = font(SANS, 17)
    ft = "All events happened or were first reported on Thursday, 19 November 2026  •  Compiled from wire reports"
    d.text(((W - d.textlength(ft, font=f_f)) / 2, 994), ft, font=f_f, fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
