"""Rasterise the SVG masters into the sizes each platform actually asks for.

Nothing here is decorative: every size below is a real requirement somewhere
(Telegram/WhatsApp avatars, apple-touch-icon, favicon, Open Graph, Play/App
Store icon), so he can upload without opening an editor.
"""
import os, cairosvg
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "out")
DST = os.path.join(HERE, "dist")

TREE = {
    "logo": [
        ("luxtipps-horizontal-dark.svg", [1600, 800, 400]),
        ("luxtipps-horizontal-dark-tagline.svg", [1600, 800]),
        ("luxtipps-horizontal-light.svg", [1600, 800, 400]),
        ("luxtipps-stacked-dark.svg", [1200, 600]),
        ("luxtipps-stacked-light.svg", [1200, 600]),
        ("luxtipps-horizontal-on-transparent-forDark.svg", [1600, 800]),
        ("luxtipps-horizontal-on-transparent-forLight.svg", [1600, 800]),
        ("luxtipps-mono-gold.svg", [1600]),
        ("luxtipps-mono-cream.svg", [1600]),
        ("luxtipps-mono-ink.svg", [1600]),
    ],
    "mark": [
        ("luxtipps-mark.svg", [1024, 512, 256, 128, 64]),
        ("luxtipps-mark-ink.svg", [1024, 512, 256]),
        ("luxtipps-mark-gold.svg", [1024, 512, 256]),
    ],
    "social": [
        ("luxtipps-avatar.svg", [1024, 640, 512, 320, 200]),
        ("luxtipps-og.svg", [1200]),
    ],
    "app": [
        ("luxtipps-appicon.svg", [1024, 512, 192, 180, 152, 120]),
    ],
}

FAVICON_SIZES = [16, 32, 48, 64]


def out_name(svg_name, w):
    return "%s-%d.png" % (svg_name[:-4], w)


def dither(path, amp=2):
    """Break up the banding rings a wide dark gradient shows in 8-bit.

    A gradient from near-black to near-black crosses very few distinct values,
    so the steps become visible rings. A couple of levels of noise scatters the
    boundary and the rings stop reading. Invisible at ±2.
    """
    import random
    im = Image.open(path).convert("RGB")
    px = im.load()
    rnd = random.Random(20260827)          # fixed, so rebuilds are identical
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            n = rnd.randint(-amp, amp)
            px[x, y] = (max(0, min(255, r + n)),
                        max(0, min(255, g + n)),
                        max(0, min(255, b + n)))
    im.save(path)


def run():
    made = []
    for folder, items in TREE.items():
        d = os.path.join(DST, folder)
        os.makedirs(d, exist_ok=True)
        for name, widths in items:
            src = os.path.join(SRC, name)
            # copy the vector master next to its rasters - the SVG is the real
            # deliverable, the PNGs are conveniences
            with open(src) as fh:
                svg_txt = fh.read()
            with open(os.path.join(d, name), "w") as fh:
                fh.write(svg_txt)
            made.append(os.path.join(folder, name))
            for w in widths:
                p = os.path.join(d, out_name(name, w))
                cairosvg.svg2png(url=src, write_to=p, output_width=w)
                if "-og" in name:
                    dither(p)
                made.append(os.path.join(folder, out_name(name, w)))

    # favicons: square, on the ink plate, so they do not vanish on a dark tab bar
    fav = os.path.join(DST, "favicon")
    os.makedirs(fav, exist_ok=True)
    pngs = []
    for s in FAVICON_SIZES:
        p = os.path.join(fav, "favicon-%d.png" % s)
        cairosvg.svg2png(url=os.path.join(SRC, "luxtipps-appicon.svg"),
                         write_to=p, output_width=s, output_height=s)
        pngs.append(Image.open(p).convert("RGBA"))
        made.append("favicon/favicon-%d.png" % s)
    ico = os.path.join(fav, "favicon.ico")
    pngs[-1].save(ico, format="ICO",
                  sizes=[(s, s) for s in FAVICON_SIZES])
    made.append("favicon/favicon.ico")

    # apple-touch-icon is a fixed filename, so ship it under that name
    cairosvg.svg2png(url=os.path.join(SRC, "luxtipps-appicon.svg"),
                     write_to=os.path.join(fav, "apple-touch-icon.png"),
                     output_width=180, output_height=180)
    made.append("favicon/apple-touch-icon.png")

    for m in sorted(made):
        print(m)
    print("\n%d files in %s" % (len(made), DST))


if __name__ == "__main__":
    run()
