#!/usr/bin/env python3
"""Generate assets/built-{light,dark}.svg: a rotating wireframe icosahedron and
3D extruded "Things I built" lettering. GitHub READMEs run no JS, so the
rotation is precomputed and baked into SMIL <animate> keyframes.

    python3 tools/make_3d_banner.py          # writes the two SVGs
    python3 tools/make_3d_banner.py check    # self-check
"""
import math
import sys
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"
W, H = 1200, 300
CX, CY, R = 210, 150, 96        # shape centre and radius on screen
FRAMES, DUR = 48, 18            # keyframes per loop, seconds per loop
FONT = "'Roboto Flex','Google Sans','Segoe UI',Roboto,Helvetica,Arial,sans-serif"

THEMES = {
    "light": dict(bg="#F9FAEF", front="#386A20", back="#9CD67D", dot="#042100",
                  ring="#6FA350", grid="#D9E7CB", top="#386A20", side="#042100",
                  sub="#43483E", chip_bg="#B7F397", chip_fg="#042100"),
    "dark": dict(bg="#12140E", front="#9CD67D", back="#205107", dot="#B7F397",
                 ring="#6FA350", grid="#282B24", top="#9CD67D", side="#205107",
                 sub="#C3C8BB", chip_bg="#205107", chip_fg="#B7F397"),
}


def icosahedron():
    p = (1 + 5 ** 0.5) / 2
    v = [(-1, p, 0), (1, p, 0), (-1, -p, 0), (1, -p, 0),
         (0, -1, p), (0, 1, p), (0, -1, -p), (0, 1, -p),
         (p, 0, -1), (p, 0, 1), (-p, 0, -1), (-p, 0, 1)]
    n = math.sqrt(1 + p * p)
    v = [(x / n, y / n, z / n) for x, y, z in v]
    # edges join vertices at the minimum distance (2 / n on the unit sphere)
    d = 2 / n
    e = [(i, j) for i in range(12) for j in range(i + 1, 12)
         if abs(math.dist(v[i], v[j]) - d) < 1e-6]
    return v, e


def project(pt, t):
    """Rotate about Y (one full turn per loop) and a wobbling X, then perspective-project."""
    x, y, z = pt
    a, b = 2 * math.pi * t, 0.45 + 0.15 * math.sin(2 * math.pi * t)
    x, z = x * math.cos(a) + z * math.sin(a), -x * math.sin(a) + z * math.cos(a)
    y, z = y * math.cos(b) - z * math.sin(b), y * math.sin(b) + z * math.cos(b)
    s = 3.2 / (3.2 - z)                      # camera 3.2 units away
    return CX + x * R * s, CY + y * R * s, z


def frames():
    """Projected vertices for each keyframe; the last frame repeats the first so the loop is seamless."""
    v, e = icosahedron()
    return [[project(pt, (k % FRAMES) / FRAMES) for pt in v] for k in range(FRAMES + 1)], e


def depth(z):
    return (z + 1) / 2                       # 0 = far side, 1 = near side


def svg(theme):
    c = THEMES[theme]
    fr, edges = frames()
    times = ";".join(f"{k / FRAMES:.4f}" for k in range(FRAMES + 1))
    anim = lambda attr, vals: (f'<animate attributeName="{attr}" dur="{DUR}s" repeatCount="indefinite" '
                               f'calcMode="linear" keyTimes="{times}" values="{";".join(vals)}"/>')
    # One <line> per edge with a fixed identity, so SMIL interpolates each edge smoothly.
    # Depth fades the far edges and thins them, which is what reads as 3D.
    lines = "".join(
        f'<line stroke="{c["front"]}" stroke-linecap="round">'
        + anim("x1", [f"{p[i][0]:.1f}" for p in fr]) + anim("y1", [f"{p[i][1]:.1f}" for p in fr])
        + anim("x2", [f"{p[j][0]:.1f}" for p in fr]) + anim("y2", [f"{p[j][1]:.1f}" for p in fr])
        + anim("stroke-opacity", [f"{0.18 + 0.82 * depth((p[i][2] + p[j][2]) / 2):.2f}" for p in fr])
        + anim("stroke-width", [f"{1.2 + 2.3 * depth((p[i][2] + p[j][2]) / 2):.2f}" for p in fr])
        + "</line>" for i, j in edges)
    dots = "".join(
        f'<circle fill="{c["dot"]}">'
        + anim("cx", [f"{p[i][0]:.1f}" for p in fr]) + anim("cy", [f"{p[i][1]:.1f}" for p in fr])
        + anim("r", [f"{2.2 + 3 * depth(p[i][2]):.2f}" for p in fr])
        + anim("fill-opacity", [f"{0.3 + 0.7 * depth(p[i][2]):.2f}" for p in fr])
        + "</circle>" for i in range(12))

    # still frame for viewers who prefer reduced motion
    p0 = fr[0]
    still = "".join(
        f'<line x1="{p0[i][0]:.1f}" y1="{p0[i][1]:.1f}" x2="{p0[j][0]:.1f}" y2="{p0[j][1]:.1f}" stroke="{c["front"]}" '
        f'stroke-linecap="round" stroke-opacity="{0.18 + 0.82 * depth((p0[i][2] + p0[j][2]) / 2):.2f}" '
        f'stroke-width="{1.2 + 2.3 * depth((p0[i][2] + p0[j][2]) / 2):.2f}"/>' for i, j in edges)
    still += "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{2.2 + 3 * depth(z):.2f}" fill="{c["dot"]}"/>' for x, y, z in p0)

    # perspective floor grid that vanishes toward the shape
    grid = "".join(f'<line x1="{CX}" y1="{CY + 20}" x2="{CX + dx}" y2="{H}" />' for dx in range(-420, 421, 70))
    grid += "".join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" />' for y in (236, 254, 276))

    title = "Things I built"
    extrude = "".join(
        f'<text x="{430 + i}" y="{150 + i}" fill="{c["side"]}" opacity="{0.35 + 0.65 * i / 10:.2f}">{title}</text>'
        for i in range(10, 0, -1))
    text_attrs = f'font-family="{FONT}" font-size="72" font-weight="900" letter-spacing="-1.5"'

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Things I built: a rotating 3D wireframe icosahedron beside 3D extruded lettering">
<title>Things I built</title>
<style>
.still{{display:none}}
.float{{animation:float 6s ease-in-out infinite}}
@keyframes float{{50%{{transform:translateY(-6px)}}}}
@media (prefers-reduced-motion:reduce){{.spin{{display:none}}.still{{display:inline}}.float{{animation:none}}}}
</style>
<clipPath id="card"><rect width="{W}" height="{H}" rx="48"/></clipPath>
<g clip-path="url(#card)">
<rect width="{W}" height="{H}" fill="{c["bg"]}"/>
<g stroke="{c["grid"]}" stroke-width="1.5">{grid}</g>
<ellipse cx="{CX}" cy="{CY + 128}" rx="120" ry="14" fill="{c["back"]}" opacity="0.35"/>
<g class="spin">
<ellipse cx="{CX}" cy="{CY}" rx="150" ry="34" fill="none" stroke="{c["ring"]}" stroke-width="2" stroke-dasharray="4 8" transform="rotate(-14 {CX} {CY})"/>
{lines}
{dots}
<circle r="6" fill="{c["front"]}"><animateMotion dur="7s" repeatCount="indefinite" path="M{CX - 150} {CY} a150 34 0 1 0 300 0 a150 34 0 1 0 -300 0" rotate="0"/></circle>
</g>
<g class="still">{still}</g>
<g class="float" {text_attrs}>
{extrude}
<text x="430" y="150" fill="{c["top"]}">{title}</text>
</g>
<rect x="432" y="184" width="292" height="40" rx="20" fill="{c["chip_bg"]}"/>
<text x="578" y="210" font-family="{FONT}" font-size="16" font-weight="700" fill="{c["chip_fg"]}" text-anchor="middle">started as irritations · shipped</text>
</g>
</svg>
'''


def check():
    v, e = icosahedron()
    assert len(v) == 12 and len(e) == 30, (len(v), len(e))
    fr, _ = frames()
    assert fr[0] == fr[-1], "loop must be seamless"
    # every projected vertex stays inside the banner
    assert all(0 < x < W and 0 < y < H for p in fr for x, y, _ in p)
    import xml.dom.minidom
    for t in THEMES:
        xml.dom.minidom.parseString(svg(t).encode())
    print("check ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        check()
    else:
        for t in THEMES:
            out = ASSETS / f"built-{t}.svg"
            out.write_text(svg(t))
            print(out.name, len(out.read_bytes()) // 1024, "KB")
