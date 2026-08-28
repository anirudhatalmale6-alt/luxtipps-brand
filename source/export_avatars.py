import os, cairosvg
from PIL import Image, ImageDraw
import build_avatars as A

SRC = A.OUT
DST = os.path.join(os.path.dirname(A.OUT), "dist_avatars")
os.makedirs(DST, exist_ok=True)
SIZES = [1024, 512, 320, 200]
names = list(A.COMPACT) + list(A.VARIANTS)
for n in names:
    for s in SIZES:
        cairosvg.svg2png(url=os.path.join(SRC, n + ".svg"),
                         write_to=os.path.join(DST, "%s-%d.png" % (n, s)),
                         output_width=s, output_height=s)
    open(os.path.join(DST, n + ".svg"), "w").write(open(os.path.join(SRC, n + ".svg")).read())
print("rasterised", len(names) * len(SIZES), "png")


def sheet(group, title, path):
    CELL, PAD = 300, 20
    h = PAD * 3 + CELL + 200
    im = Image.new("RGB", (CELL * 4 + PAD * 5, h), "#20242b")
    d = ImageDraw.Draw(im)
    d.text((PAD, 4), title, fill="#eaf0f6")
    for i, n in enumerate(group):
        big = Image.open(os.path.join(DST, "%s-512.png" % n)).convert("RGBA").resize((CELL, CELL))
        x = PAD + i * (CELL + PAD)
        im.paste(big, (x, PAD + 14), big)
        d.text((x + 4, PAD + CELL + 18), n, fill="#cfd4dc")
    y0 = PAD * 2 + CELL + 40
    d.text((PAD, y0 - 16), "at 48px, the size Telegram actually draws it, magnified 4x", fill="#cfd4dc")
    for i, n in enumerate(group):
        s = Image.open(os.path.join(DST, "%s-512.png" % n)).convert("RGBA").resize((48, 48), Image.LANCZOS)
        im.paste(s.resize((192, 192), Image.NEAREST), (PAD + i * (CELL + PAD), y0), s.resize((192, 192), Image.NEAREST))
    im.save(path)
    print(path, im.size)


sheet(list(A.COMPACT), "PROFILE PICTURE version - mark + one word", os.path.join(DST, "_sheet_compact.png"))
sheet(list(A.VARIANTS), "FULL NAME version - for posts, headers, sharing", os.path.join(DST, "_sheet_named.png"))
