"""Two-page PDF showing the logo and where every file goes.

He cannot open images in the Freelancer chat, so the PDF is the only preview
that reaches him. Everything drawn here is the real artwork, pulled from the
same functions that wrote the deliverables - not a mock-up of them.
"""
import os, io, cairosvg
from PIL import Image
import build_logo as B

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1400, 1980

INK, INK2, GOLD, GOLD_SOFT, CREAM, MUTED = (B.INK, B.INK_2, B.GOLD, B.GOLD_SOFT,
                                            B.CREAM, B.MUTED)
PAPER = "#FFFFFF"
BODY = "#2b2f36"
FAINT = "#9aa0a8"
HAIR = "#e3e5e8"


def t(text, x, y, size, col, font=None, track=0.0, anchor="start"):
    font = font or B.B_MED
    d, w = B.text_path(font, text, size, track)
    if anchor == "middle":
        x -= w / 2
    elif anchor == "end":
        x -= w
    return f'<g transform="translate({x:.2f},{y:.2f})"><path d="{d}" fill="{col}"/></g>', w


def T(*a, **k):
    return t(*a, **k)[0]


def rule(x1, y, x2, col=HAIR, w=1.0):
    return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{col}" stroke-width="{w}"/>'


def panel(x, y, w, h, fill, r=14):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"/>'


def embed(svg_text, x, y, box_w, box_h):
    """Drop a finished logo SVG into the sheet, scaled to fit its box."""
    import re
    m = re.match(r'<svg[^>]*viewBox="0 0 ([\d.]+) ([\d.]+)"', svg_text)
    vw, vh = float(m.group(1)), float(m.group(2))
    s = min(box_w / vw, box_h / vh)
    inner = svg_text.split(">", 1)[1].rsplit("</svg>", 1)[0]
    ox = x + (box_w - vw * s) / 2
    oy = y + (box_h - vh * s) / 2
    return f'<g transform="translate({ox:.2f},{oy:.2f}) scale({s:.5f})">{inner}</g>'


def header(title, sub, page):
    p = [panel(0, 0, W, 132, INK, 0)]
    p.append(B.mark_svg(CREAM, B.GOLD_RAMP, 64, 32, 68))
    p.append(T(title, 156, 70, 34, CREAM, B.BC_BOLD, 1.0))
    p.append(T(sub, 156, 98, 16, MUTED, B.B_MED, 1.4))
    p.append(T(page, W - 64, 84, 16, MUTED, B.B_MED, 1.2, "end"))
    return "\n".join(p)


def footer(txt):
    return (rule(64, H - 74, W - 64) +
            T(txt, 64, H - 46, 15, FAINT, B.B_MED, 0.6))


def section(label, x, y):
    return (T(label, x, y, 15, GOLD_SOFT, B.BC_BOLD, 2.6) +
            rule(x, y + 12, W - 64, HAIR))


# --------------------------------------------------------------------- page 1
def page1():
    p = [f'<rect width="{W}" height="{H}" fill="{PAPER}"/>',
         header("LUXTIPPS", "logo kit  ·  built on the colours and type of luxtipps.com", "1 / 2")]

    y = 196
    p.append(section("PRIMARY LOGO", 64, y))
    y += 34
    p.append(panel(64, y, W - 128, 250, INK))
    p.append(embed(B.FILES["luxtipps-horizontal-dark.svg"], 64, y, W - 128, 250))
    y += 250
    p.append(T("This is the one to use almost everywhere. Dark background, cream L, gold bars.",
               64, y + 30, 17, BODY))

    y += 66
    p.append(section("STACKED  ·  FOR SQUARE SPACES", 64, y))
    y += 34
    p.append(panel(64, y, 640, 330, INK))
    p.append(embed(B.FILES["luxtipps-stacked-dark.svg"], 64, y, 640, 330))
    p.append(panel(724, y, 612, 330, CREAM))
    p.append(embed(B.FILES["luxtipps-stacked-light.svg"], 724, y, 612, 330))
    y += 330
    p.append(T("On his dark site, and on anything printed or white.", 64, y + 30, 17, BODY))

    y += 66
    p.append(section("ONE COLOUR  ·  WHEN COLOUR IS NOT AN OPTION", 64, y))
    y += 34
    p.append(panel(64, y, 420, 190, "#ffffff", 14))
    p.append(f'<rect x="64" y="{y}" width="420" height="190" rx="14" fill="none" stroke="{HAIR}"/>')
    p.append(embed(B.FILES["luxtipps-mono-ink.svg"], 84, y + 20, 380, 150))
    p.append(panel(504, y, 420, 190, INK))
    p.append(embed(B.FILES["luxtipps-mono-cream.svg"], 524, y + 20, 380, 150))
    p.append(panel(944, y, 392, 190, INK2))
    p.append(embed(B.FILES["luxtipps-mono-gold.svg"], 964, y + 20, 352, 150))
    y += 190
    for i, lab in enumerate(["black  ·  invoices, stamps, fax",
                             "cream  ·  on dark photos",
                             "gold  ·  on very dark only"]):
        p.append(T(lab, [64, 504, 944][i], y + 28, 15, FAINT))

    y += 74
    p.append(section("IN USE", 64, y))
    y += 40
    p.append(in_use(64, y))

    p.append(footer("LuxTipps logo kit  ·  vector SVG + PNG + favicon  ·  page 1 of 2"))
    return "".join(p)


def in_use(x, y):
    """Three places he will actually see it: Telegram, a browser tab, the site."""
    p = []
    cw = (W - 128 - 32) / 2

    # --- Telegram chat list row -------------------------------------------
    p.append(panel(x, y, cw, 300, "#17212b"))
    p.append(T("Telegram", x + 24, y + 40, 16, "#7d8b99", B.B_MED, 1.6))
    ry = y + 66
    for i, (name, msg, unread) in enumerate([
            ("LuxTipps", "Today's tip is up - 3 picks", "3"),
            ("Bayern Fans", "you: ok", ""),
            ("Marko", "Photo", "")]):
        if i == 0:
            p.append(embed(B.avatar(1024), x + 22, ry + 10, 62, 62))
        else:
            p.append(f'<circle cx="{x + 53}" cy="{ry + 41}" r="31" fill="#2b3a4a"/>')
        p.append(T(name, x + 100, ry + 34, 19, "#ffffff", B.B_MED, 0.2))
        p.append(T(msg, x + 100, ry + 60, 16, "#7d8b99"))
        if unread:
            p.append(f'<rect x="{x + cw - 74}" y="{ry + 26}" width="34" height="26" rx="13" fill="{GOLD}"/>')
            p.append(T(unread, x + cw - 57, ry + 45, 15, INK, B.B_MED, 0, "middle"))
        ry += 78
    p.append(T("the avatar, masked to a circle by Telegram itself",
               x, y + 328, 15, FAINT))

    # --- browser tab + site header ----------------------------------------
    x2 = x + cw + 32
    p.append(panel(x2, y, cw, 300, "#dfe3e8"))
    # tab
    p.append(f'<path d="M{x2 + 20},{y + 66} v-32 a10,10 0 0 1 10,-10 h250 a10,10 0 0 1 10,10 v32 z" fill="#ffffff"/>')
    p.append(embed(B.app_icon(512), x2 + 36, y + 34, 20, 20))
    p.append(T("LuxTipps — Free 30 Days of VIP", x2 + 66, y + 48, 14, "#3c4043"))
    p.append(f'<rect x="{x2}" y="{y + 66}" width="{cw}" height="42" fill="#ffffff"/>')
    p.append(f'<rect x="{x2 + 20}" y="{y + 76}" width="{cw - 40}" height="24" rx="12" fill="#f1f3f4"/>')
    p.append(T("luxtipps.com", x2 + 38, y + 93, 14, "#5f6368"))
    # site header on his ink
    p.append(f'<rect x="{x2}" y="{y + 108}" width="{cw}" height="192" fill="{INK}"/>')
    p.append(embed(B.FILES["luxtipps-horizontal-dark.svg"], x2 + 10, y + 122, 250, 56))
    for i, nav in enumerate(["Tips", "VIP", "Results"]):
        p.append(T(nav, x2 + cw - 230 + i * 76, y + 154, 15, CREAM, B.B_MED, 0.4))
    p.append(f'<rect x="{x2 + 24}" y="{y + 208}" width="{cw - 48}" height="10" rx="5" fill="#ffffff" opacity="0.12"/>')
    p.append(f'<rect x="{x2 + 24}" y="{y + 230}" width="{(cw - 48) * 0.7:.0f}" height="10" rx="5" fill="#ffffff" opacity="0.12"/>')
    p.append(f'<rect x="{x2 + 24}" y="{y + 258}" width="150" height="30" rx="15" fill="{GOLD}"/>')
    p.append(T("Join free", x2 + 99, y + 278, 15, INK, B.B_MED, 0.4, "middle"))
    p.append(T("favicon in the tab, primary logo in the header",
               x2, y + 328, 15, FAINT))
    return "".join(p)


# --------------------------------------------------------------------- page 2
def page2():
    p = [f'<rect width="{W}" height="{H}" fill="{PAPER}"/>',
         header("WHERE EACH FILE GOES", "so nothing has to be re-cropped or re-made", "2 / 2")]

    y = 196
    p.append(section("PROFILE PICTURE, APP ICON, FAVICON", 64, y))
    y += 40

    # avatar
    p.append(embed(B.avatar(1024), 64, y, 220, 220))
    p.append(T("Telegram / WhatsApp", 174, y + 250, 15, BODY, B.B_MED, 0, "middle"))
    p.append(T("Instagram / Facebook", 174, y + 272, 15, BODY, B.B_MED, 0, "middle"))
    p.append(T("avatar-1024.png", 174, y + 296, 14, GOLD_SOFT, B.B_MED, 0, "middle"))

    # app icon
    p.append(embed(B.app_icon(512), 344, y, 220, 220))
    p.append(T("App / store icon", 454, y + 250, 15, BODY, B.B_MED, 0, "middle"))
    p.append(T("square, rounded", 454, y + 272, 15, FAINT, B.B_MED, 0, "middle"))
    p.append(T("appicon-1024.png", 454, y + 296, 14, GOLD_SOFT, B.B_MED, 0, "middle"))

    # favicons at true size
    p.append(panel(624, y, 300, 220, "#fbfbfc"))
    p.append(f'<rect x="624" y="{y}" width="300" height="220" rx="14" fill="none" stroke="{HAIR}"/>')
    fx = 664
    for s in [16, 32, 48, 64]:
        p.append(embed(B.app_icon(512), fx, y + 92 - s / 2, s, s))
        p.append(T(str(s), fx + s / 2, y + 150, 13, FAINT, B.B_MED, 0, "middle"))
        fx += s + 34
    p.append(T("actual size", 774, y + 44, 15, BODY, B.B_MED, 0, "middle"))
    p.append(T("favicon.ico  ·  16/32/48/64", 774, y + 250, 14, GOLD_SOFT, B.B_MED, 0, "middle"))
    p.append(T("apple-touch-icon.png 180", 774, y + 272, 14, FAINT, B.B_MED, 0, "middle"))

    # og
    p.append(embed(B.og_image(), 964, y + 26, 372, 196))
    p.append(T("Link preview when luxtipps.com", 1150, y + 250, 15, BODY, B.B_MED, 0, "middle"))
    p.append(T("is pasted anywhere  ·  og-1200.png", 1150, y + 272, 15, FAINT, B.B_MED, 0, "middle"))

    y += 340

    # palette
    p.append(section("COLOURS  ·  READ OUT OF HIS OWN STYLESHEET", 64, y))
    y += 40
    sw = [(INK, "Ink", "#07090D", "background"),
          (INK2, "Ink 2", "#0E1217", "cards"),
          (GOLD, "Gold", "#EBBD57", "the accent"),
          (GOLD_SOFT, "Gold soft", "#C69E58", "gold on light"),
          (CREAM, "Cream", "#F4F2EA", "text"),
          (MUTED, "Muted", "#9C988E", "small print")]
    x = 64
    bw = (W - 128 - 5 * 16) / 6
    for col, name, hexv, use in sw:
        p.append(panel(x, y, bw, 96, col))
        p.append(f'<rect x="{x}" y="{y}" width="{bw}" height="96" rx="14" fill="none" stroke="{HAIR}"/>')
        p.append(T(name, x, y + 124, 17, BODY, B.B_MED, 0.2))
        p.append(T(hexv, x, y + 148, 15, GOLD_SOFT, B.B_MED, 0.6))
        p.append(T(use, x, y + 170, 14, FAINT))
        x += bw + 16
    y += 216

    # type
    p.append(section("TYPE", 64, y))
    y += 44
    p.append(T("Barlow Condensed Bold", 64, y + 26, 40, INK, B.BC_BOLD, 0.6))
    p.append(T("the logo and headlines", 64, y + 54, 15, FAINT))
    p.append(T("Barlow Medium", 700, y + 26, 34, INK, B.B_MED, 0.4))
    p.append(T("everything else  ·  both are free for commercial use (OFL)",
               700, y + 54, 15, FAINT))
    y += 96

    # clear space + minimum size
    p.append(section("CLEAR SPACE  ·  MINIMUM SIZE", 64, y))
    y += 40
    p.append(clear_space(64, y, 600, 240))
    p.append(min_size(700, y, W - 64 - 700, 240))
    y += 336

    # what is in the folder
    p.append(section("WHAT IS IN THE FOLDER", 64, y))
    y += 38
    p.append(file_tree(64, y))

    p.append(footer("All files: github.com/anirudhatalmale6-alt/luxtipps-brand  ·  page 2 of 2"))
    return "".join(p)


def clear_space(x, y, w, h):
    """The margin rule, drawn rather than described - one gold bar all round."""
    p = [panel(x, y, w, h, "#fafafb"),
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="none" stroke="{HAIR}"/>']
    lw, lh = 300.0, 108.0
    lx, ly = x + (w - lw) / 2, y + (h - lh) / 2
    m = 34.0                       # = height of the tallest gold bar at this scale
    p.append(f'<rect x="{lx - m}" y="{ly - m}" width="{lw + 2*m}" height="{lh + 2*m}" '
             f'fill="none" stroke="{GOLD_SOFT}" stroke-width="1.5" stroke-dasharray="7 6"/>')
    p.append(embed(B.FILES["luxtipps-horizontal-on-transparent-forLight.svg"], lx, ly, lw, lh))
    for ax, ay in [(lx - m / 2, ly + lh / 2), (lx + lw + m / 2, ly + lh / 2),
                   (lx + lw / 2, ly - m / 2), (lx + lw / 2, ly + lh + m / 2)]:
        p.append(T("x", ax, ay + 5, 15, GOLD_SOFT, B.B_MED, 0, "middle"))
    p.append(T("x = the height of the tallest gold bar. Keep that much space",
               x, y + h + 26, 15, FAINT))
    p.append(T("empty on all four sides - no text, no photo edge, no button.",
               x, y + h + 46, 15, FAINT))
    return "".join(p)


def min_size(x, y, w, h):
    p = [panel(x, y, w, h, "#fafafb"),
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="none" stroke="{HAIR}"/>']
    p.append(embed(B.FILES["luxtipps-horizontal-on-transparent-forLight.svg"],
                   x + 30, y + 40, 200, 72))
    p.append(T("120 px wide", x + 130, y + 138, 14, FAINT, B.B_MED, 0, "middle"))
    p.append(T("smallest for the full logo", x + 130, y + 158, 14, FAINT, B.B_MED, 0, "middle"))
    p.append(embed(B.app_icon(512), x + 300, y + 58, 40, 40))
    p.append(T("24 px", x + 320, y + 138, 14, FAINT, B.B_MED, 0, "middle"))
    p.append(T("below that, use the mark alone", x + 320, y + 158, 14, FAINT, B.B_MED, 0, "middle"))
    p.append(T("Under 120 px the two words start closing up. Swap to the",
               x, y + h + 26, 15, FAINT))
    p.append(T("square mark instead - it was drawn to survive a 16 px favicon.",
               x, y + h + 46, 15, FAINT))
    return "".join(p)


def file_tree(x, y):
    """Read the real dist folder, so the sheet cannot claim a file that is missing."""
    dist = os.path.join(HERE, "dist")
    groups = []
    for folder in ["logo", "mark", "social", "app", "favicon"]:
        d = os.path.join(dist, folder)
        if not os.path.isdir(d):
            continue
        names = sorted(os.listdir(d))
        svgs = [n for n in names if n.endswith(".svg")]
        rest = [n for n in names if not n.endswith(".svg")]
        groups.append((folder, svgs, rest))

    notes = {
        "logo": "the wordmark lockups - this is what goes on the site and on anything printed",
        "mark": "the square symbol on its own, transparent background",
        "social": "profile pictures and the link-preview image",
        "app": "rounded square icon, every size a store or a phone asks for",
        "favicon": "drop these in the root of luxtipps.com",
    }

    def png_sizes(names):
        """The distinct pixel widths present, so he can see the range at a glance
        without reading sixty filenames."""
        out = set()
        for n in names:
            stem = n[:-4]
            tail = stem.rsplit("-", 1)[-1]
            if tail.isdigit():
                out.add(int(tail))
        return sorted(out, reverse=True)

    p = []
    col_x = [x, x + 690]
    cy = [y, y]
    for i, (folder, svgs, rest) in enumerate(groups):
        c = 0 if i < 2 else 1
        yy = cy[c]
        p.append(T("/" + folder, col_x[c], yy + 18, 21, INK, B.BC_BOLD, 0.8))
        p.append(T(notes[folder], col_x[c] + 108, yy + 18, 14, FAINT))
        yy += 42
        for n in svgs:
            p.append(T("SVG", col_x[c], yy, 12, GOLD_SOFT, B.B_MED, 1.0))
            p.append(T(n, col_x[c] + 42, yy, 15, BODY))
            yy += 23
        sizes = png_sizes(rest)
        if sizes:
            p.append(T("PNG", col_x[c], yy, 12, FAINT, B.B_MED, 1.0))
            label = "same artwork at " + ", ".join(str(s) for s in sizes) + " px"
            if folder == "favicon":
                label = "favicon.ico (16/32/48/64) + apple-touch-icon 180 px"
            p.append(T(label, col_x[c] + 42, yy, 15, FAINT))
            yy += 23
        yy += 22
        cy[c] = yy
    total = sum(len(s) + len(r) for _, s, r in groups)
    p.append(T("%d files in total. The SVGs are the masters - if a size is ever missing, "
               "it can be made from those." % total,
               x, max(cy) + 8, 15, BODY))
    return "".join(p)


def render(body, scale=1.0):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}">{body}</svg>')
    png = cairosvg.svg2png(bytestring=svg.encode(), output_width=int(W * scale),
                           output_height=int(H * scale))
    return Image.open(io.BytesIO(png)).convert("RGB")


if __name__ == "__main__":
    B.build()
    p1 = render(page1())
    p2 = render(page2())
    out = os.path.join(HERE, "luxtipps-logo.pdf")
    p1.save(out, "PDF", resolution=150, save_all=True, append_images=[p2])
    p1.save(os.path.join(HERE, "png", "sheet1.png"))
    p2.save(os.path.join(HERE, "png", "sheet2.png"))
    print(out, os.path.getsize(out), "bytes", p1.size, p2.size)
