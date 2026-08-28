"""Named avatars - one per LuxTipps account, so four channels are told apart at a glance.

Same mark and same palette as the main kit (build_logo.py is imported, not copied,
so the mark can never drift between the two). What changes per variant is the
sub-label and the colour of the plate.

Everything is laid out against the circle Telegram/Instagram mask to, not the
square: text sits inside 62% of the diameter, because the corners of the square
are cut off and a wordmark that fills the width loses its first and last letter.
"""
import os

import build_logo as B
from build_logo import (INK, INK_2, GOLD, GOLD_SOFT, CREAM, MUTED,
                        BC_BOLD, B_MED, GOLD_RAMP, mark_svg, text_path,
                        cap_height, svg)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out_avatars")
os.makedirs(OUT, exist_ok=True)


def fit(font, text, target_w, tracking_ratio=0.06):
    """Cap size that makes `text` come out `target_w` wide, plus its path.

    Measured, not guessed: the string is outlined once at a reference size and
    the result scaled, so tracking is included in the width instead of being a
    fudge factor added afterwards.
    """
    ref = 100.0
    _, w_ref = text_path(font, text, ref, ref * tracking_ratio)
    size = ref * target_w / w_ref
    d, w = text_path(font, text, size, size * tracking_ratio)
    return d, w, size


def pill(x, y, w, h, fill, stroke=None, sw=0.0):
    r = h / 2
    st = f' stroke="{stroke}" stroke-width="{sw:.2f}"' if stroke else ""
    f = fill if fill else "none"
    return (f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" '
            f'rx="{r:.2f}" ry="{r:.2f}" fill="{f}"{st}/>')


def named_avatar(size, bg, l_col, bar_cols, lux_col, tipps_col,
                 sub=None, sub_text_col=None, sub_fill=None, sub_stroke=None):
    """Circular avatar: mark, LUXTIPPS, and an optional sub-label pill."""
    S = float(size)
    parts = [f'<circle cx="{S/2:.2f}" cy="{S/2:.2f}" r="{S/2:.2f}" fill="{bg}"/>']

    if sub:
        mark_s = S * 0.275
        mark_y = S * 0.135
        word_target = S * 0.540
        word_base = S * 0.590
        sub_gap = S * 0.045
    else:
        # no third line, so the two remaining elements get the room back
        mark_s = S * 0.345
        mark_y = S * 0.175
        word_target = S * 0.620
        word_base = S * 0.760

    parts.append(mark_svg(l_col, bar_cols, (S - mark_s) / 2, mark_y, mark_s))

    # LUX + TIPPS as one fitted unit, then split so the two halves keep the
    # kerning they were measured with
    d_all, w_all, ws = fit(BC_BOLD, "LUXTIPPS", word_target)
    tr = ws * 0.06
    d1, w1 = text_path(BC_BOLD, "LUX", ws, tr)
    d2, w2 = text_path(BC_BOLD, "TIPPS", ws, tr)
    total = w1 + tr + w2
    x0 = (S - total) / 2
    parts.append(f'<g transform="translate({x0:.2f},{word_base:.2f})">'
                 f'<path d="{d1}" fill="{lux_col}"/>'
                 f'<g transform="translate({w1 + tr:.2f},0)">'
                 f'<path d="{d2}" fill="{tipps_col}"/></g></g>')

    if sub:
        # Set the letter height first and let the pill grow around it. Sizing the
        # pill first and fitting text into it is what made VIP - three fat
        # letters - burst straight out of its own badge.
        ss = S * 0.075 / (cap_height(B_MED, 100.0) / 100.0)
        d, w = text_path(B_MED, sub, ss, ss * 0.16)
        max_w = S * 0.40
        if w > max_w:                       # long labels shrink, they never spill
            ss *= max_w / w
            d, w = text_path(B_MED, sub, ss, ss * 0.16)
        cap = cap_height(B_MED, ss)
        pad_x, ph = cap * 1.15, cap * 2.30
        pw = w + pad_x * 2
        px = (S - pw) / 2
        py = word_base + sub_gap
        parts.append(pill(px, py, pw, ph, sub_fill, sub_stroke, S * 0.008))
        parts.append(f'<g transform="translate({px + pad_x:.2f},'
                     f'{py + ph / 2 + cap / 2:.2f})">'
                     f'<path d="{d}" fill="{sub_text_col}"/></g>')

    return svg(size, size, "\n".join(parts))


# One entry per account he named. The plate colour does as much work as the
# label: three dark and one light means the odd one out is his personal account.
VARIANTS = {
    "luxtipps-avatar-vip": dict(
        bg=INK, l_col=CREAM, bar_cols=GOLD_RAMP, lux_col=GOLD, tipps_col=CREAM,
        sub="VIP", sub_text_col=INK, sub_fill=GOLD, sub_stroke=None),
    "luxtipps-avatar-reviews": dict(
        bg=INK, l_col=CREAM, bar_cols=GOLD_RAMP, lux_col=GOLD, tipps_col=CREAM,
        sub="REVIEWS", sub_text_col=CREAM, sub_fill=None, sub_stroke=CREAM),
    "luxtipps-avatar-bot": dict(
        bg=INK_2, l_col=CREAM, bar_cols=GOLD_RAMP, lux_col=GOLD, tipps_col=CREAM,
        sub="BOT", sub_text_col=MUTED, sub_fill=None, sub_stroke=MUTED),
    "luxtipps-avatar-personal": dict(
        bg=CREAM, l_col=INK, bar_cols=GOLD_RAMP, lux_col=GOLD_SOFT, tipps_col=INK,
        sub=None),
}


def compact_avatar(size, bg, l_col, bar_cols, label, label_col, ring=None):
    """The profile-picture version: mark plus ONE word, both big.

    Telegram draws an avatar at about 48px in a chat list. Three stacked lines
    do not survive that - checked at 48px, not by scaling the big one down - so
    this drops the wordmark and gives the room to the label instead.
    """
    S = float(size)
    parts = [f'<circle cx="{S/2:.2f}" cy="{S/2:.2f}" r="{S/2:.2f}" fill="{bg}"/>']
    if ring:
        parts.append(f'<circle cx="{S/2:.2f}" cy="{S/2:.2f}" r="{S/2 - S*0.030:.2f}" '
                     f'fill="none" stroke="{ring}" stroke-width="{S*0.030:.2f}"/>')
    mark_s = S * 0.36
    parts.append(mark_svg(l_col, bar_cols, (S - mark_s) / 2, S * 0.185, mark_s))
    d, w, ss = fit(BC_BOLD, label, S * 0.62, tracking_ratio=0.05)
    # A short word like VIP hits the width limit at a size whose caps climb into
    # the mark. Clamp the height too and let the word be narrower than the room.
    max_cap = S * 0.185
    if cap_height(BC_BOLD, ss) > max_cap:
        ss *= max_cap / cap_height(BC_BOLD, ss)
        d, w = text_path(BC_BOLD, label, ss, ss * 0.05)
    parts.append(f'<g transform="translate({(S - w) / 2:.2f},{S * 0.795:.2f})">'
                 f'<path d="{d}" fill="{label_col}"/></g>')
    return svg(size, size, "\n".join(parts))


# Same four accounts, but for the profile picture slot. Distinguished by plate
# and ring as well as by word, because at 48px the word is the first thing to go.
COMPACT = {
    "luxtipps-tg-vip": dict(bg=INK, l_col=CREAM, bar_cols=GOLD_RAMP,
                            label="VIP", label_col=GOLD, ring=GOLD),
    "luxtipps-tg-reviews": dict(bg=INK, l_col=CREAM, bar_cols=GOLD_RAMP,
                                label="REVIEWS", label_col=CREAM, ring=None),
    "luxtipps-tg-bot": dict(bg=INK_2, l_col=CREAM, bar_cols=GOLD_RAMP,
                            label="BOT", label_col=MUTED, ring=MUTED),
    "luxtipps-tg-personal": dict(bg=CREAM, l_col=INK, bar_cols=GOLD_RAMP,
                                 label="LUXTIPPS", label_col=INK, ring=None),
}


def build():
    made = []
    for name, kw in COMPACT.items():
        p = os.path.join(OUT, name + ".svg")
        with open(p, "w") as fh:
            fh.write(compact_avatar(1024, **kw))
        made.append(p)
    for name, kw in VARIANTS.items():
        p = os.path.join(OUT, name + ".svg")
        with open(p, "w") as fh:
            fh.write(named_avatar(1024, **kw))
        made.append(p)
    print("wrote %d svg" % len(made))
    return made


if __name__ == "__main__":
    build()
