#!/usr/bin/env python3
"""Material 3 isometric contribution skyline with a 3D snake that eats each day I committed.

Input is the GitHub GraphQL contribution calendar (see .github/workflows/skyline.yml):

    python3 tools/skyline3d.py calendar.json assets/   # writes skyline-light.svg and skyline-dark.svg
    python3 tools/skyline3d.py check                   # self-check on synthetic data

Stdlib only. GitHub READMEs run no JS, so all motion is SMIL baked into the SVG.
"""
import json
import math
import sys
from pathlib import Path

W, H = 1200, 470
S = 12                                   # cell size
A, B = S * math.cos(math.pi / 6), S / 2  # isometric x / y step
OX, OY = 573, 92                         # screen position of week 0, day 0
SPEED = 9.0                              # snake speed, cells per second
SEGMENTS, GAP = 7, 0.11                  # snake body segments and seconds between them
FONT = "'Roboto Flex','Google Sans','Segoe UI',Roboto,Helvetica,Arial,sans-serif"

THEMES = {
    "light": dict(bg="#F3EDF7", on="#1D1B20", sub="#49454F", accent="#6750A4",
                  chip_bg="#EADDFF", chip_fg="#21005D",
                  levels=["#E7E0EC", "#D0BCFF", "#9A82DB", "#6750A4", "#4F378B"],
                  snake=("#FFD8E4", "#7D5260", "#31111D")),
    "dark": dict(bg="#211F26", on="#E6E0E9", sub="#CAC4D0", accent="#D0BCFF",
                 chip_bg="#4F378B", chip_fg="#EADDFF",
                 levels=["#36343B", "#4F378B", "#6750A4", "#9A82DB", "#D0BCFF"],
                 snake=("#FFD8E4", "#EFB8C8", "#633B48")),
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


def snake_route(cells, heights):
    """Head route: start at the first cell, then visit every active day week by week
    (serpentine within a week), stepping one cell at a time so the snake rides over blocks.
    Returns screen points and, for each active cell, the fraction of the route at which it is eaten."""
    active = sorted((c for c in cells if c[2]), key=lambda c: (c[0], c[1] if c[0] % 2 == 0 else -c[1]))
    pos, grid, eaten = (0, 0), [(0, 0)], []
    top = lambda w, d: heights.get((w, d), 3) + 4
    for w, d, _, _ in active:
        while pos != (w, d):                 # walk the day axis first, then the week axis
            pos = (pos[0], pos[1] + (d > pos[1]) - (d < pos[1])) if pos[1] != d else (pos[0] + (w > pos[0]) - (w < pos[0]), pos[1])
            grid.append(pos)
        eaten.append(((w, d), len(grid) - 1))
    for _ in range(4):                       # run off past the last block before the loop restarts
        pos = (pos[0] + 1, pos[1])
        grid.append(pos)
    pts = [iso(w, d, top(w, d)) for w, d in grid]   # the snake climbs onto each block's top face
    # paced animateMotion moves at constant screen speed, so eat times follow screen distance
    dist = [0.0]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        dist.append(dist[-1] + math.hypot(x1 - x0, y1 - y0))
    return pts, [(cell, dist[i] / dist[-1]) for cell, i in eaten], grid


def block(w, d, h, colour, extra=""):
    g = 0.09                                  # gap between tiles so the floor reads as a grid
    w0, w1, d0, d1 = w + g, w + 1 - g, d + g, d + 1 - g
    t0, t1, t2, t3 = iso(w0, d0, h), iso(w1, d0, h), iso(w1, d1, h), iso(w0, d1, h)
    b1, b2, b3 = iso(w1, d0), iso(w1, d1), iso(w0, d1)
    pts = lambda *p: " ".join(f"{x:.1f},{y:.1f}" for x, y in p)
    return (f'<g{extra}><polygon points="{pts(t3, t2, b2, b3)}" fill="{shade(colour, .22)}"/>'
            f'<polygon points="{pts(t1, t2, b2, b1)}" fill="{shade(colour, .38)}"/>'
            f'<polygon points="{pts(t0, t1, t2, t3)}" fill="{colour}"/></g>')


def svg(cal, theme):
    c = THEMES[theme]
    cells, total = load(cal)
    top = max([n for *_, n, _ in cells] + [1])
    heights = {(w, d): height(n, top) for w, d, n, _ in cells}
    pts, eaten, _ = snake_route(cells, heights)
    dur =max(8.0, (len(pts) - 1) / SPEED)

    # painter's order: back (small w+d) to front
    order = sorted(cells, key=lambda c: (c[0] + c[1], c[0]))
    blocks = "".join(block(w, d, heights[w, d], c["levels"][lv]) for w, d, _, lv in order)

    # When the head reaches a block, a flat "eaten" tile covers it; the tiles clear as the loop restarts.
    eat_at = dict(eaten)
    covers = []
    for w, d, n, _ in order:
        if not n:
            continue
        t = eat_at[(w, d)]
        t1, t2 = min(t + 0.004, 0.96), 0.985
        key = f"0;{t:.4f};{t1:.4f};{t2};1"
        covers.append(block(w, d, heights[w, d], c["levels"][0], extra=' opacity="0"')
                      .replace("</g>", f'<animate attributeName="opacity" dur="{dur:.2f}s" repeatCount="indefinite" '
                               f'keyTimes="{key}" values="0;0;1;1;0"/></g>'))

    path = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    hi, mid, lo = c["snake"]
    body = "".join(
        f'<circle r="{7.5 - 0.6 * k:.1f}" fill="url(#ball-{theme})">'
        f'<animateMotion dur="{dur:.2f}s" repeatCount="indefinite" begin="{-k * GAP:.2f}s" path="{path}"/></circle>'
        for k in range(SEGMENTS - 1, -1, -1))
    # Segment k runs k*GAP seconds behind the head. The motion path is in absolute coordinates,
    # so the circles must have no transform of their own (animateMotion adds to it).

    legend = "".join(f'<rect x="{56 + 22 * i}" y="356" width="16" height="16" rx="5" fill="{col}"/>'
                     for i, col in enumerate(c["levels"]))

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{total} contributions in the last year, drawn as a 3D isometric skyline. A snake crawls over the blocks and eats each day with a commit.">
<title>{total} contributions in the last year as a 3D skyline, with a snake eating each day I committed</title>
<defs>
<radialGradient id="ball-{theme}" cx="35%" cy="30%" r="70%"><stop offset="0" stop-color="{hi}"/><stop offset=".55" stop-color="{mid}"/><stop offset="1" stop-color="{lo}"/></radialGradient>
</defs>
<style>
.grow{{transform-box:view-box;transform-origin:50% 100%;animation:grow 1.2s cubic-bezier(.34,1.56,.64,1) both}}
@keyframes grow{{from{{transform:scaleY(.2);opacity:0}}}}
@media (prefers-reduced-motion:reduce){{.motion{{display:none}}.grow{{animation:none}}}}
</style>
<rect width="{W}" height="{H}" rx="48" fill="{c["bg"]}"/>
<rect x="56" y="56" width="128" height="36" rx="18" fill="{c["chip_bg"]}"/>
<text x="120" y="80" font-family="{FONT}" font-size="14" font-weight="800" fill="{c["chip_fg"]}" text-anchor="middle" letter-spacing=".5">LAST 12 MONTHS</text>
<text x="52" y="210" font-family="{FONT}" font-size="112" font-weight="900" fill="{c["accent"]}" letter-spacing="-4">{total}</text>
<text x="56" y="252" font-family="{FONT}" font-size="24" font-weight="700" fill="{c["on"]}">contributions</text>
<text x="56" y="290" font-family="{FONT}" font-size="16" fill="{c["sub"]}">The snake eats every day I shipped,</text>
<text x="56" y="314" font-family="{FONT}" font-size="16" fill="{c["sub"]}">then the year grows back.</text>
<text x="56" y="346" font-family="{FONT}" font-size="13" font-weight="600" fill="{c["sub"]}">Less</text>
{legend}
<text x="170" y="369" font-family="{FONT}" font-size="13" font-weight="600" fill="{c["sub"]}">More</text>
<g class="grow">{blocks}</g>
<g class="motion">{"".join(covers)}{body}</g>
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
        heights = {(w, d): height(n, max([n for *_, n, _ in cells] + [1])) for w, d, n, _ in cells}
        pts, eaten, grid = snake_route(cells, heights)
        assert len(eaten) == sum(1 for c in cells if c[2]), "every active day gets eaten"
        times = [t for _, t in eaten]
        assert times == sorted(times) and all(0 < t < 1 for t in times), "eat times rise inside the loop"
        for (w0, d0), (w1, d1) in zip(grid, grid[1:]):
            assert abs(w1 - w0) + abs(d1 - d0) == 1, "snake moves one cell per step"
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
