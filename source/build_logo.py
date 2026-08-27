"""Build the LuxTipps logo system.

Everything here is derived from his own site, not invented:
  palette  -> :root custom properties in https://luxtipps.com/assets/styles-CG4gm_Vo.css
  type     -> Barlow Condensed (display) + Barlow (sans), the families that CSS asks for

Wordmark text is converted to real outlines with fontTools, so the finished SVG
has no font dependency - it renders the same on a machine that has never heard
of Barlow. That is the difference between a logo file and a screenshot of one.
"""
import os, math
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(os.path.dirname(HERE), "fonts")
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)

# --- his palette, copied out of his stylesheet ---
INK       = "#07090D"
INK_2     = "#0E1217"
GOLD      = "#EBBD57"
GOLD_SOFT = "#C69E58"
CREAM     = "#F4F2EA"
MUTED     = "#9C988E"

BC_BOLD = os.path.join(FONTS, "BarlowCondensed-Bold.ttf")
BC_MED  = os.path.join(FONTS, "BarlowCondensed-Medium.ttf")
B_MED   = os.path.join(FONTS, "Barlow-Medium.ttf")

_cache = {}


def _font(path):
    if path not in _cache:
        f = TTFont(path)
        _cache[path] = (f, f["head"].unitsPerEm, f.getBestCmap(), f.getGlyphSet(), f["hmtx"])
    return _cache[path]


def text_path(font_path, text, size, tracking=0.0):
    """Outline `text` at cap-size `size`, baseline on y=0, starting at x=0.

    Returns (path_data, advance_width). Tracking is in the same units as size.
    """
    _, upem, cmap, gs, hmtx = _font(font_path)
    scale = size / upem
    x, parts = 0.0, []
    for ch in text:
        gname = cmap.get(ord(ch))
        if gname is None:
            x += size * 0.3
            continue
        pen = SVGPathPen(gs)
        gs[gname].draw(TransformPen(pen, Transform(scale, 0, 0, -scale, x, 0)))
        cmds = pen.getCommands()
        if cmds:
            parts.append(cmds)
        x += hmtx[gname][0] * scale + tracking
    return " ".join(parts), (x - tracking if text else 0.0)


def cap_height(font_path, size):
    _, upem, _, _, _ = _font(font_path)
    f = _cache[font_path][0]
    try:
        ch = f["OS/2"].sCapHeight
    except Exception:
        ch = upem * 0.72
    return ch * size / upem


# ---------------------------------------------------------------- the mark
# An L whose foot carries three ascending bars: the letter and the chart are
# the same silhouette. One idea, no ornament, still legible in a 32px favicon.
MARK_VB = 100.0

STEM_X, STEM_W = 10.0, 16.0
TOP_Y = 11.0
FOOT_TOP, FOOT_BOT = 73.0, 89.0
FOOT_R = 90.0
# The bars climb to just under the top of the stem, so the empty quarter in the
# top right closes up and the three tops draw a line pointing up and to the
# right. Tops chosen by eye at 32px, not by formula.
BARS = [(32.0, 56.0), (53.0, 38.0), (74.0, 20.0)]   # (x, top y)
BAR_W = 16.0
R = 2.0            # corner softening, just enough to look drawn not clipped


def _round_rect(x, y, w, h, r=R):
    r = min(r, w / 2, h / 2)
    return (f"M{x + r:.2f},{y:.2f} H{x + w - r:.2f} A{r},{r} 0 0 1 {x + w:.2f},{y + r:.2f} "
            f"V{y + h - r:.2f} A{r},{r} 0 0 1 {x + w - r:.2f},{y + h:.2f} "
            f"H{x + r:.2f} A{r},{r} 0 0 1 {x:.2f},{y + h - r:.2f} "
            f"V{y + r:.2f} A{r},{r} 0 0 1 {x + r:.2f},{y:.2f} Z")


def l_path():
    """Stem + foot as one L shape."""
    x0, x1 = STEM_X, STEM_X + STEM_W
    return (f"M{x0 + R:.2f},{TOP_Y:.2f} H{x1 - R:.2f} "
            f"A{R},{R} 0 0 1 {x1:.2f},{TOP_Y + R:.2f} "
            f"V{FOOT_TOP:.2f} H{FOOT_R - R:.2f} "
            f"A{R},{R} 0 0 1 {FOOT_R:.2f},{FOOT_TOP + R:.2f} "
            f"V{FOOT_BOT - R:.2f} A{R},{R} 0 0 1 {FOOT_R - R:.2f},{FOOT_BOT:.2f} "
            f"H{x0 + R:.2f} A{R},{R} 0 0 1 {x0:.2f},{FOOT_BOT - R:.2f} "
            f"V{TOP_Y + R:.2f} A{R},{R} 0 0 1 {x0 + R:.2f},{TOP_Y:.2f} Z")


def bars_paths():
    return [_round_rect(x, top, BAR_W, FOOT_TOP - top) for x, top in BARS]


def mark_svg(l_col, bar_cols, x=0.0, y=0.0, size=MARK_VB, idp=""):
    """The mark as a <g>, scaled to `size` and placed at x,y."""
    s = size / MARK_VB
    g = [f'<g transform="translate({x:.2f},{y:.2f}) scale({s:.5f})">']
    g.append(f'<path d="{l_path()}" fill="{l_col}"/>')
    for p, c in zip(bars_paths(), bar_cols):
        g.append(f'<path d="{p}" fill="{c}"/>')
    g.append("</g>")
    return "\n".join(g)


GOLD_RAMP = [GOLD_SOFT, "#D9AE58", GOLD]     # bars lift toward the brightest gold
FLAT_GOLD = [GOLD, GOLD, GOLD]


def svg(w, h, body, bg=None, extra=""):
    b = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}">{extra}{b}\n{body}\n</svg>')


# ------------------------------------------------------------- the wordmark
WORD_SIZE = 100.0
TRACK = 1.2


def wordmark(lux_col, tipps_col, size=WORD_SIZE, tracking=TRACK):
    """LUX in gold, TIPPS in cream/ink. Baseline y=0, returns (body, width)."""
    d1, w1 = text_path(BC_BOLD, "LUX", size, tracking)
    d2, w2 = text_path(BC_BOLD, "TIPPS", size, tracking)
    body = (f'<path d="{d1}" fill="{lux_col}"/>'
            f'<g transform="translate({w1 + tracking:.2f},0)">'
            f'<path d="{d2}" fill="{tipps_col}"/></g>')
    return body, w1 + tracking + w2


def tagline(col, text="DAILY FOOTBALL TIPS", size=20.0, tracking=4.2):
    d, w = text_path(B_MED, text, size, tracking)
    return f'<path d="{d}" fill="{col}"/>', w


# ------------------------------------------------------------------ lockups
def horizontal(bg, l_col, lux_col, tipps_col, bar_cols, tag_col=None, pad=48):
    """Mark left, wordmark right, optical centres aligned on the cap height."""
    ms = 132.0
    ws = 104.0
    cap = cap_height(BC_BOLD, ws)
    body, ww = wordmark(lux_col, tipps_col, ws)

    gap = 34.0
    tag_h = 0.0
    tg = ""
    if tag_col:
        tg_body, tw = tagline(tag_col)
        tag_h = 34.0

    content_w = ms + gap + ww
    w = content_w + pad * 2
    h = ms + pad * 2

    my = pad
    # sit the wordmark's cap box centred against the mark
    base_y = my + ms / 2 + cap / 2 - (tag_h / 2 if tag_col else 0)
    parts = [mark_svg(l_col, bar_cols, pad, my, ms)]
    parts.append(f'<g transform="translate({pad + ms + gap:.2f},{base_y:.2f})">{body}</g>')
    if tag_col:
        parts.append(f'<g transform="translate({pad + ms + gap + 2:.2f},{base_y + 30:.2f})">{tg_body}</g>')
    return svg(round(w), round(h), "\n".join(parts), bg)


def stacked(bg, l_col, lux_col, tipps_col, bar_cols, tag_col=None, pad=56):
    ms = 168.0
    ws = 96.0
    cap = cap_height(BC_BOLD, ws)
    body, ww = wordmark(lux_col, tipps_col, ws)
    tg_body = tw = None
    if tag_col:
        tg_body, tw = tagline(tag_col, size=17.0, tracking=3.8)

    content_w = max(ms, ww, tw or 0)
    w = content_w + pad * 2
    h = pad + ms + 30 + cap + (30 if tag_col else 0) + pad

    cx = w / 2
    parts = [mark_svg(l_col, bar_cols, cx - ms / 2, pad, ms)]
    by = pad + ms + 30 + cap
    parts.append(f'<g transform="translate({cx - ww / 2:.2f},{by:.2f})">{body}</g>')
    if tag_col:
        parts.append(f'<g transform="translate({cx - tw / 2:.2f},{by + 32:.2f})">{tg_body}</g>')
    return svg(round(w), round(h), "\n".join(parts), bg)


def app_icon(size=512, bg=INK, l_col=CREAM, bar_cols=None, radius_pct=0.22):
    bar_cols = bar_cols or GOLD_RAMP
    r = size * radius_pct
    ms = size * 0.60
    off = (size - ms) / 2
    body = (f'<rect width="{size}" height="{size}" rx="{r:.1f}" ry="{r:.1f}" fill="{bg}"/>'
            + mark_svg(l_col, bar_cols, off, off, ms))
    return svg(size, size, body)


def avatar(size=1024, bg=INK, l_col=CREAM, bar_cols=None):
    """Circular crop - Telegram, WhatsApp, IG, FB all mask to a circle."""
    bar_cols = bar_cols or GOLD_RAMP
    ms = size * 0.56
    off = (size - ms) / 2
    body = (f'<circle cx="{size/2}" cy="{size/2}" r="{size/2}" fill="{bg}"/>'
            + mark_svg(l_col, bar_cols, off, off, ms))
    return svg(size, size, body)


def og_image(w=1200, h=630):
    parts = [f'<rect width="{w}" height="{h}" fill="{INK}"/>']
    # a very quiet gold wash so it does not read as a black rectangle in a feed
    parts.append(f'<defs><radialGradient id="g" cx="50%" cy="34%" r="70%">'
                 f'<stop offset="0%" stop-color="{GOLD}" stop-opacity="0.16"/>'
                 f'<stop offset="100%" stop-color="{GOLD}" stop-opacity="0"/>'
                 f'</radialGradient></defs>'
                 f'<rect width="{w}" height="{h}" fill="url(#g)"/>')
    ms = 176.0
    ws = 112.0
    cap = cap_height(BC_BOLD, ws)
    body, ww = wordmark(GOLD, CREAM, ws)
    gap = 36.0
    total = ms + gap + ww
    x0 = (w - total) / 2
    my = h / 2 - ms / 2 - 34
    parts.append(mark_svg(CREAM, GOLD_RAMP, x0, my, ms))
    parts.append(f'<g transform="translate({x0 + ms + gap:.2f},{my + ms/2 + cap/2:.2f})">{body}</g>')
    tg, tw = tagline(MUTED, text="DAILY FOOTBALL TIPS  ·  LUXTIPPS.COM", size=26.0, tracking=5.0)
    parts.append(f'<g transform="translate({(w - tw)/2:.2f},{my + ms + 74:.2f})">{tg}</g>')
    return svg(w, h, "\n".join(parts))


def write(name, content):
    p = os.path.join(OUT, name)
    with open(p, "w") as fh:
        fh.write(content)
    return p


FILES = {}


def build():
    # full colour, on his dark background
    FILES["luxtipps-horizontal-dark.svg"] = horizontal(INK, CREAM, GOLD, CREAM, GOLD_RAMP)
    FILES["luxtipps-horizontal-dark-tagline.svg"] = horizontal(INK, CREAM, GOLD, CREAM, GOLD_RAMP, MUTED)
    FILES["luxtipps-stacked-dark.svg"] = stacked(INK, CREAM, GOLD, CREAM, GOLD_RAMP, MUTED)

    # on light / white, for invoices, print, anything not dark
    FILES["luxtipps-horizontal-light.svg"] = horizontal(CREAM, INK, GOLD_SOFT, INK, GOLD_RAMP)
    FILES["luxtipps-stacked-light.svg"] = stacked(CREAM, INK, GOLD_SOFT, INK, GOLD_RAMP, "#6b675f")

    # transparent versions - same art, no background plate
    FILES["luxtipps-horizontal-on-transparent-forDark.svg"] = horizontal(None, CREAM, GOLD, CREAM, GOLD_RAMP)
    FILES["luxtipps-horizontal-on-transparent-forLight.svg"] = horizontal(None, INK, GOLD_SOFT, INK, GOLD_RAMP)

    # one-colour, for stamps, embroidery, faxes, anywhere colour is not an option
    FILES["luxtipps-mono-gold.svg"] = horizontal(None, GOLD, GOLD, GOLD, FLAT_GOLD)
    FILES["luxtipps-mono-cream.svg"] = horizontal(None, CREAM, CREAM, CREAM, [CREAM] * 3)
    FILES["luxtipps-mono-ink.svg"] = horizontal(None, INK, INK, INK, [INK] * 3)

    # the mark on its own
    FILES["luxtipps-mark.svg"] = svg(100, 100, mark_svg(CREAM, GOLD_RAMP), None)
    FILES["luxtipps-mark-ink.svg"] = svg(100, 100, mark_svg(INK, GOLD_RAMP), None)
    FILES["luxtipps-mark-gold.svg"] = svg(100, 100, mark_svg(GOLD, FLAT_GOLD), None)

    FILES["luxtipps-appicon.svg"] = app_icon(512)
    FILES["luxtipps-avatar.svg"] = avatar(1024)
    FILES["luxtipps-og.svg"] = og_image()

    for n, c in FILES.items():
        write(n, c)
    print("wrote %d svg files to %s" % (len(FILES), OUT))


if __name__ == "__main__":
    build()
