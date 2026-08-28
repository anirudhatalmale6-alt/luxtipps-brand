"""One-page PDF preview of the eight avatars - the format that opens for him."""
import base64, os, cairosvg
import build_avatars as A
from build_logo import BC_BOLD, B_MED, text_path, INK, GOLD, CREAM, MUTED

DST = os.path.join(os.path.dirname(A.OUT), "dist_avatars")
W, H = 842.0, 595.0     # A4 landscape, points


def img(path, x, y, s):
    b64 = base64.b64encode(open(path, "rb").read()).decode()
    return (f'<image x="{x:.1f}" y="{y:.1f}" width="{s:.1f}" height="{s:.1f}" '
            f'xlink:href="data:image/png;base64,{b64}"/>')


def txt(font, s, size, x, y, col, track=0.0, center_w=None):
    d, w = text_path(font, s, size, track)
    if center_w:
        x = x + (center_w - w) / 2
    return f'<g transform="translate({x:.1f},{y:.1f})"><path d="{d}" fill="{col}"/></g>'


parts = [f'<rect width="{W}" height="{H}" fill="{INK}"/>']
parts.append(txt(BC_BOLD, "LUXTIPPS AVATARS", 30, 46, 60, CREAM, 1.2))
parts.append(txt(B_MED, "one per account - profile picture version on top, full name version below",
                 12, 48, 82, MUTED, 0.6))

rows = [
    (list(A.COMPACT), "PROFILE PICTURE  -  use these on Telegram and Instagram", 120),
    (list(A.VARIANTS), "FULL NAME  -  posts, channel headers, anywhere it is shown big", 350),
]
S = 150.0
for names, title, y in rows:
    parts.append(txt(B_MED, title, 12, 48, y - 12, GOLD, 1.6))
    for i, n in enumerate(names):
        x = 48 + i * (S + 42)
        parts.append(img(os.path.join(DST, "%s-512.png" % n), x, y, S))
        label = n.split("-")[-1]
        parts.append(txt(B_MED, label.upper(), 11, x, y + S + 18, CREAM, 1.4, center_w=S))

parts.append(txt(B_MED, "luxtipps.com  -  built from the palette on your own site", 10,
                 48, H - 32, MUTED, 0.8))

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
       f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">' + "\n".join(parts) + "</svg>")
out = os.path.join(DST, "luxtipps-avatars.pdf")
cairosvg.svg2pdf(bytestring=svg.encode(), write_to=out)
print(out, os.path.getsize(out), "bytes")
