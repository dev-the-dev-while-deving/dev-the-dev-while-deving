"""Regenerate the project cards: python3 assets/cards.py (writes assets/card-*-{dark,light}.svg)."""
from pathlib import Path
from xml.sax.saxutils import escape

THEMES = {
    "dark": dict(bg="#10110e", ink="#f4f1ea", muted="#a19e96", sub="#c8c4ba", term="#171910"),
    "light": dict(bg="#f3f0e7", ink="#161616", muted="#5c5952", sub="#3c3a34", term="#e4e0d2"),
}
CARDS = [  # slug, name, label, tagline, command
    ("termbrowse", "termbrowse", "RUST", "The web, read from a terminal. No JavaScript.", "browse news.ycombinator.com"),
    ("rolldeep", "ROLLDEEP", "TYPESCRIPT", "One roll. One topic. Do the work. Never repeat.", "roll"),
    ("breakbench", "breakbench", "PYTHON", "Breaks agents on purpose and keeps the failure.", "break --replay"),
    ("cut", "CUT", "JAVASCRIPT", "A neon, hard-edged site with WebGL on scroll.", "open cut"),
    ("kokou", "Kokou", "MACOS", "孤高, a solitary ascent. Focus, on the Mac.", "ascend"),
    ("printquote", "PrintQuote", "TYPESCRIPT", "A drawing or WhatsApp RFQ in, a GST quote out.", "quote rfq.pdf"),
]


def card(name, label, tagline, cmd, t):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 580 220" role="img" aria-label="{escape(name)}: {escape(tagline)}">
  <style>
    .s {{ font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue", Helvetica, Arial, sans-serif; }}
    .m {{ font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace; }}
    @media (prefers-reduced-motion: reduce) {{ animate {{ display: none; }} }}
  </style>
  <rect width="580" height="220" fill="{t['bg']}"/>
  <path d="M14 14h20M14 14v20M566 14h-20M566 14v20M14 206h20M14 206v-20M566 206h-20M566 206v-20" fill="none" stroke="{t['ink']}" stroke-width="1.5"/>
  <rect x="36" y="38" width="12" height="12" fill="#d6ff00" stroke="{t['ink']}" stroke-width="1.5"/>
  <text class="m" x="58" y="49" font-size="12" letter-spacing="3" fill="{t['muted']}">{label}</text>
  <text class="s" x="34" y="104" font-size="46" font-weight="700" letter-spacing="-1.5" fill="{t['ink']}">{escape(name)}</text>
  <path d="M36 120h120" stroke="{t['ink']}" stroke-width="3"/>
  <text class="s" x="36" y="148" font-size="17" fill="{t['sub']}">{escape(tagline)}</text>
  <rect x="36" y="164" width="508" height="34" fill="{t['term']}"/>
  <text class="m" x="48" y="186" font-size="14"><tspan fill="#d6ff00" stroke="{t['ink']}" stroke-width="0.4">$</tspan><tspan fill="{t['ink']}" dx="10">{escape(cmd)}</tspan></text>
  <rect x="{70 + 8.45 * len(cmd):.0f}" y="173" width="2" height="17" fill="#d6ff00"><animate attributeName="opacity" values="1;0;1" dur="1.2s" calcMode="discrete" repeatCount="indefinite"/></rect>
</svg>
"""


out = Path(__file__).parent
for slug, *fields in CARDS:
    for theme, t in THEMES.items():
        (out / f"card-{slug}-{theme}.svg").write_text(card(*fields, t))
print(f"wrote {len(CARDS) * len(THEMES)} cards")
