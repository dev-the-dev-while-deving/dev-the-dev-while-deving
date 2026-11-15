#!/usr/bin/env python3
"""Material 3 isometric contribution skyline: one 3D block per day, taller on busier days.

Input is the GitHub GraphQL contribution calendar (see .github/workflows/skyline.yml):

    python3 tools/skyline3d.py calendar.json assets/   # writes skyline-light.svg and skyline-dark.svg
    python3 tools/skyline3d.py check                   # self-check on synthetic data

Stdlib only. GitHub READMEs run no JS, so the only motion is a CSS grow-in.
"""
import json
import math
import sys
from pathlib import Path

W, H = 1200, 470
S = 12                                   # cell size
A, B = S * math.cos(math.pi / 6), S / 2  # isometric x / y step
OX, OY = 573, 92                         # screen position of week 0, day 0
FONT = "'Roboto Flex','Google Sans','Segoe UI',Roboto,Helvetica,Arial,sans-serif"

THEMES = {
    "light": dict(bg="#F3EDF7", on="#1D1B20", sub="#49454F", accent="#6750A4",
                  chip_bg="#EADDFF", chip_fg="#21005D",
                  levels=["#E7E0EC", "#D0BCFF", "#9A82DB", "#6750A4", "#4F378B"]),
    "dark": dict(bg="#211F26", on="#E6E0E9", sub="#CAC4D0", accent="#D0BCFF",
                 chip_bg="#4F378B", chip_fg="#EADDFF",
                 levels=["#36343B", "#4F378B", "#6750A4", "#9A82DB", "#D0BCFF"]),
}
LEVEL = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}


def shade(hex_colour, f):
    """Darken a #RRGGBB colour by factor f (0..1) for the block's side faces."""
    r, g, b = (int(hex_colour[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02X%02X%02X" % tuple(round(c * (1 - f)) for c in (r, g, b))


def iso(w, d, z=0.0):
    return OX + (w - d) * A, OY + (w + d) * B - z


def load(cal):
    """[(week, day, count, level)] plus the total, from the GraphQL calendar."""
    cells = [(w, day["weekday"], day["contributionCount"], LEVEL[day["contributionLevel"]])
             for w, week in enumerate(cal["weeks"]) for day in week["contributionDays"]]
    return cells, cal["totalContributions"]


def height(count, top):
    return 3 if count == 0 else 8 + 46 * math.sqrt(count / top)


def block(w, d, h, colour):
    g = 0.09                                  # gap between tiles so the floor reads as a grid
    w0, w1, d0, d1 = w + g, w + 1 - g, d + g, d + 1 - g
    t0, t1, t2, t3 = iso(w0, d0, h), iso(w1, d0, h), iso(w1, d1, h), iso(w0, d1, h)
    b1, b2, b3 = iso(w1, d0), iso(w1, d1), iso(w0, d1)
    pts = lambda *p: " ".join(f"{x:.1f},{y:.1f}" for x, y in p)
    return (f'<g><polygon points="{pts(t3, t2, b2, b3)}" fill="{shade(colour, .22)}"/>'
            f'<polygon points="{pts(t1, t2, b2, b1)}" fill="{shade(colour, .38)}"/>'
            f'<polygon points="{pts(t0, t1, t2, t3)}" fill="{colour}"/></g>')


def svg(cal, theme):
    c = THEMES[theme]
    cells, total = load(cal)
    top = max([n for *_, n, _ in cells] + [1])
    heights = {(w, d): height(n, top) for w, d, n, _ in cells}

    # painter's order: back (small w+d) to front
    order = sorted(cells, key=lambda c: (c[0] + c[1], c[0]))
    blocks = "".join(block(w, d, heights[w, d], c["levels"][lv]) for w, d, _, lv in order)

    legend = "".join(f'<rect x="{56 + 22 * i}" y="356" width="16" height="16" rx="5" fill="{col}"/>'
                     for i, col in enumerate(c["levels"]))

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{total} contributions in the last year, drawn as a 3D isometric skyline.">
<title>{total} contributions in the last year as a 3D skyline</title>
<style>
.grow{{transform-box:view-box;transform-origin:50% 100%;animation:grow 1.2s cubic-bezier(.34,1.56,.64,1) both}}
@keyframes grow{{from{{transform:scaleY(.2);opacity:0}}}}
@media (prefers-reduced-motion:reduce){{.grow{{animation:none}}}}
</style>
<rect width="{W}" height="{H}" rx="48" fill="{c["bg"]}"/>
<rect x="56" y="56" width="128" height="36" rx="18" fill="{c["chip_bg"]}"/>
<text x="120" y="80" font-family="{FONT}" font-size="14" font-weight="800" fill="{c["chip_fg"]}" text-anchor="middle" letter-spacing=".5">LAST 12 MONTHS</text>
<text x="52" y="210" font-family="{FONT}" font-size="112" font-weight="900" fill="{c["accent"]}" letter-spacing="-4">{total}</text>
<text x="56" y="252" font-family="{FONT}" font-size="24" font-weight="700" fill="{c["on"]}">contributions</text>
<text x="56" y="290" font-family="{FONT}" font-size="16" fill="{c["sub"]}">One block for every day of the year.</text>
<text x="56" y="314" font-family="{FONT}" font-size="16" fill="{c["sub"]}">Taller means more commits that day.</text>
<text x="56" y="346" font-family="{FONT}" font-size="13" font-weight="600" fill="{c["sub"]}">Less</text>
{legend}
<text x="170" y="369" font-family="{FONT}" font-size="13" font-weight="600" fill="{c["sub"]}">More</text>
<g class="grow">{blocks}</g>
</svg>
'''


def synthetic():
    import random
    rnd = random.Random(1)
    weeks = []
    for w in range(53):
        days = []
        for d in range(7):
            n = rnd.choice([0, 0, 0, 0, 1, 3, 9])
            lv = 0 if n == 0 else 1 if n < 2 else 2 if n < 4 else 4
            days.append({"weekday": d, "contributionCount": n, "contributionLevel": list(LEVEL)[lv]})
        weeks.append({"contributionDays": days})
    return {"weeks": weeks, "totalContributions": sum(d["contributionCount"] for w in weeks for d in w["contributionDays"])}


def check():
    import xml.dom.minidom
    for cal in (synthetic(), {"weeks": [{"contributionDays": [{"weekday": d, "contributionCount": 0, "contributionLevel": "NONE"} for d in range(7)]}] * 53, "totalContributions": 0}):
        cells, _ = load(cal)
        top = max([n for *_, n, _ in cells] + [1])
        heights = [height(n, top) for _, _, n, _ in cells]
        busiest = max(cells, key=lambda c: c[2])
        assert max(heights) == height(busiest[2], top), "busiest day is the tallest block"
        assert all(h >= 3 for h in heights), "empty days still show a floor tile"
        for t in THEMES:
            xml.dom.minidom.parseString(svg(cal, t).encode())
    print("check ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        check()
    else:
        data = json.loads(Path(sys.argv[1]).read_text())
        cal = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
        out = Path(sys.argv[2])
        for t in THEMES:
            (out / f"skyline-{t}.svg").write_text(svg(cal, t))
            print(f"skyline-{t}.svg", (out / f"skyline-{t}.svg").stat().st_size // 1024, "KB")
