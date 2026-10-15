"""Build the promises brand assets: mark SVGs, mascot SVG, README banner and social preview PNGs."""
import math
import os
import cairosvg
from shapely.geometry import LineString

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(OUT, exist_ok=True)

PAPER = "#EFEDE6"
BLUE = "#1D3FB8"
ORANGE = "#FF5A1F"
OVER = "#1D1616"   # multiply(ORANGE, BLUE)
STROKE = 9.0
MISREG = (1.6, -1.2)

# ---------- mark geometry ----------

def arc(cx, cy, r, t0, t1, n=40):
    return [(cx + r * math.cos(t0 + (t1 - t0) * i / n), cy + r * math.sin(t0 + (t1 - t0) * i / n)) for i in range(n + 1)]

def hook_a():
    pts = [(14, 4), (14, 34)] + arc(26, 34, 12, math.pi, 0)[1:] + [(38, 12)]
    return pts

def hook_b():
    pts = [(50, 60), (50, 30)] + arc(38, 30, 12, 0, -math.pi)[1:] + [(26, 52)]
    return pts

PATH_A = "M14 4 V34 a12 12 0 0 0 24 0 V12"
PATH_B = "M50 60 V30 a12 12 0 0 0 -24 0 V52"

def overlap_path(dx=MISREG[0], dy=MISREG[1]):
    a = LineString([(x + dx, y + dy) for x, y in hook_a()]).buffer(STROKE / 2, cap_style="round", join_style="round")
    b = LineString(hook_b()).buffer(STROKE / 2, cap_style="round", join_style="round")
    inter = a.intersection(b)
    polys = [inter] if inter.geom_type == "Polygon" else list(inter.geoms)
    d = []
    for p in polys:
        coords = list(p.exterior.coords)
        d.append("M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in coords) + " Z")
    return " ".join(d)

def mark_group(x=0, y=0, scale=1.0, ink_a=ORANGE, ink_b=BLUE, overprint=True, misreg=True):
    dx, dy = MISREG if misreg else (0, 0)
    parts = [f'<g transform="translate({x} {y}) scale({scale})" fill="none" stroke-width="{STROKE}" stroke-linecap="round" stroke-linejoin="round">']
    parts.append(f'<path d="{PATH_A}" stroke="{ink_a}" transform="translate({dx} {dy})"/>')
    parts.append(f'<path d="{PATH_B}" stroke="{ink_b}"/>')
    if overprint:
        parts.append(f'<path d="{overlap_path(dx, dy)}" fill="{OVER}" stroke="none"/>')
    parts.append("</g>")
    return "\n".join(parts)

def write(name, svg):
    path = os.path.join(OUT, name)
    with open(path, "w") as f:
        f.write(svg)
    return path

# mark.svg — two inks on transparent, with overprint
write("mark.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64" role="img" aria-label="promises mark: two hooks, linked">
{mark_group()}
</svg>
''')

# mark-mono.svg — one ink, for favicons and tiny sizes
write("mark-mono.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64" role="img" aria-label="promises mark">
{mark_group(ink_a=BLUE, ink_b=BLUE, overprint=False, misreg=False)}
</svg>
''')

# mark-on-ink.svg — for dark backgrounds: orange + paper, no overprint
write("mark-on-ink.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64" role="img" aria-label="promises mark">
<rect width="64" height="64" rx="14" fill="{BLUE}"/>
{mark_group(x=8, y=8, scale=0.75, ink_a=ORANGE, ink_b=PAPER, overprint=False, misreg=False)}
</svg>
''')

# ---------- the Witness ----------

def witness_group(x=0, y=0, scale=1.0):
    return f'''<g transform="translate({x} {y}) scale({scale})" fill="none" stroke-linecap="round" stroke-linejoin="round">
  <g transform="translate(3 -3)">
    <rect x="60" y="128" width="100" height="104" rx="26" fill="{ORANGE}"/>
    <rect x="22" y="170" width="18" height="10" rx="3" fill="{ORANGE}"/>
  </g>
  <g stroke="{BLUE}">
    <ellipse cx="110" cy="70" rx="48" ry="54" fill="{PAPER}" stroke-width="6"/>
    <path d="M78 26 Q110 2 142 26" stroke-width="6"/>
    <path d="M82 56 Q92 48 104 56" stroke-width="5"/>
    <path d="M116 58 H136" stroke-width="5"/>
    <path d="M84 74 H104" stroke-width="5"/>
    <path d="M116 74 H136" stroke-width="5"/>
    <path d="M86 78 Q94 86 102 78" stroke-width="4"/>
    <path d="M118 78 Q126 86 134 78" stroke-width="4"/>
    <path d="M100 104 H120" stroke-width="5"/>
    <rect x="60" y="128" width="100" height="104" rx="26" stroke-width="6"/>
    <path d="M92 128 L110 144 L128 128" stroke-width="5"/>
    <path d="M62 158 L30 190" stroke-width="6"/>
    <rect x="8" y="176" width="46" height="62" rx="5" fill="{PAPER}" stroke-width="5"/>
    <rect x="22" y="170" width="18" height="10" rx="3" stroke-width="4"/>
    <path d="M18 196 H44 M18 208 H44 M18 220 H36" stroke-width="4"/>
    <path d="M158 158 L192 118" stroke-width="6"/>
    <circle cx="196" cy="110" r="13" fill="{PAPER}" stroke-width="5"/>
    <path d="M202 100 L212 82" stroke-width="5"/>
    <path d="M90 232 V262 M130 232 V262" stroke-width="6"/>
    <path d="M80 262 H100 M120 262 H140" stroke-width="6"/>
  </g>
</g>'''

write("witness.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 300" width="260" height="300" role="img" aria-label="The Witness: a deadpan figure with a clipboard and a raised pinky">
<rect width="260" height="300" rx="20" fill="{PAPER}"/>
{witness_group(x=20, y=16)}
</svg>
''')

# ---------- banner (README hero) ----------

FONT_XB = "Bricolage Grotesque ExtraBold"
FONT_SB = "Bricolage Grotesque SemiBold"
FONT_MD = "Bricolage Grotesque Medium"
MONO = "JetBrains Mono"

banner = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 400" width="1280" height="400">
<rect width="1280" height="400" fill="{PAPER}"/>
{mark_group(x=64, y=58, scale=1.5)}
<text x="186" y="130" font-family="{FONT_XB}" font-size="92" letter-spacing="-3.5" fill="{BLUE}">promises</text>
<text x="66" y="222" font-family="{FONT_SB}" font-size="38" letter-spacing="-0.8" fill="{BLUE}">Your repos made promises.</text>
<text x="66" y="266" font-family="{FONT_SB}" font-size="38" letter-spacing="-0.8" fill="{BLUE}">Someone should have written them down.</text>
<text x="66" y="332" font-family="{MONO}" font-size="17" fill="{BLUE}">one file at the root of your workspace · read by any coding agent · no daemon, no server</text>
<text x="66" y="358" font-family="{MONO}" font-size="17" fill="{ORANGE}" font-weight="700">promises.yaml</text>
{witness_group(x=960, y=50, scale=1.1)}
</svg>
'''
bpath = write("banner.svg", banner)
cairosvg.svg2png(url=bpath, write_to=os.path.join(OUT, "banner.png"), output_width=2560)

# ---------- social preview ----------

social = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 640" width="1280" height="640">
<rect width="1280" height="640" fill="{PAPER}"/>
{mark_group(x=72, y=64, scale=0.75)}
<text x="134" y="104" font-family="{FONT_XB}" font-size="34" letter-spacing="-1.2" fill="{BLUE}">promises</text>
<text x="330" y="104" font-family="{MONO}" font-size="15" fill="{BLUE}">cross-repo contracts for coding agents</text>
<text x="72" y="300" font-family="{FONT_XB}" font-size="78" letter-spacing="-3" fill="{BLUE}">Your repos made</text>
<text x="72" y="378" font-family="{FONT_XB}" font-size="78" letter-spacing="-3" fill="{BLUE}">promises.</text>
<text x="72" y="456" font-family="{FONT_XB}" font-size="78" letter-spacing="-3" fill="{ORANGE}">Write them down.</text>
<text x="72" y="556" font-family="{MONO}" font-size="18" fill="{BLUE}">promises.yaml · one file · any agent · zero infrastructure</text>
{witness_group(x=930, y=160, scale=1.45)}
</svg>
'''
spath = write("social-preview.svg", social)
cairosvg.svg2png(url=spath, write_to=os.path.join(OUT, "social-preview.png"), output_width=2560)

# ---------- small lockup for the README footer ----------
lockup = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 96" width="360" height="96">
<rect width="360" height="96" rx="16" fill="{PAPER}"/>
{mark_group(x=20, y=16, scale=1.0)}
<text x="100" y="66" font-family="{FONT_XB}" font-size="52" letter-spacing="-2" fill="{BLUE}">promises</text>
</svg>
'''
lpath = write("lockup.svg", lockup)
cairosvg.svg2png(url=lpath, write_to=os.path.join(OUT, "lockup.png"), output_width=640)

for f in sorted(os.listdir(OUT)):
    print(f, os.path.getsize(os.path.join(OUT, f)))
