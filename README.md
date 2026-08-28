# LuxTipps logo kit

Built on the colours and type already used by [luxtipps.com](https://luxtipps.com) —
the palette below was read out of the site's own stylesheet, not chosen fresh.

## The mark

An **L** whose foot carries three ascending bars. The letter and the chart are the
same silhouette: the brand initial and "tips that go up" in one shape. It stays
readable down to a 16 px favicon, which a detailed mark would not.

## Which file do I use?

| I need… | Use |
|---|---|
| Website header, most things | `logo/luxtipps-horizontal-dark.svg` |
| A square space | `logo/luxtipps-stacked-dark.svg` |
| White or printed background | `logo/luxtipps-horizontal-light.svg` |
| Telegram / WhatsApp / IG / FB profile picture | `social/luxtipps-avatar-1024.png` |
| Link preview (Open Graph) | `social/luxtipps-og-1200.png` |
| App or store icon | `app/luxtipps-appicon-1024.png` |
| Browser tab | `favicon/favicon.ico` + `favicon/apple-touch-icon.png` |
| One colour only (stamp, invoice, embroidery) | `logo/luxtipps-mono-*.svg` |

The `.svg` files are the masters. They scale to any size with no loss, and the
lettering is already converted to outlines, so they render identically on a
machine that does not have the font installed.

## Colours

| | Hex | Use |
|---|---|---|
| Ink | `#07090D` | background |
| Ink 2 | `#0E1217` | cards |
| Gold | `#EBBD57` | the accent |
| Gold soft | `#C69E58` | gold on light backgrounds |
| Cream | `#F4F2EA` | text |
| Muted | `#9C988E` | small print |

## Type

**Barlow Condensed Bold** — the logo and headlines
**Barlow Medium** — everything else

Both are under the SIL Open Font License, so they are free for commercial use.

## Two rules

1. **Clear space** — keep a margin equal to the height of the tallest gold bar on all
   four sides. Nothing else in that space.
2. **Never redraw or re-type it.** Use the SVG. Below 120 px wide, drop the wordmark
   and use the square mark on its own.

## Avatars (added 28 Aug 2026)

One set per LuxTipps account, in `avatars/`.

**Profile picture version** — `luxtipps-tg-*`. Mark plus one word, both big. Use
these on Telegram and Instagram: an avatar is drawn at about 48px in a chat list
and three stacked lines do not survive that, so this version gives the room to
the label instead. Checked at 48px, not by shrinking the big one.

**Full name version** — `luxtipps-avatar-*`. The whole wordmark plus a sub-label
pill. Use where it is shown big: posts, channel headers, anything shared.

| account | file | plate |
|---|---|---|
| VIP channel | `luxtipps-tg-vip` / `luxtipps-avatar-vip` | ink, gold ring + gold VIP |
| Reviews channel | `luxtipps-tg-reviews` / `luxtipps-avatar-reviews` | ink, cream label |
| The bot | `luxtipps-tg-bot` / `luxtipps-avatar-bot` | ink-2, muted label |
| Personal | `luxtipps-tg-personal` / `luxtipps-avatar-personal` | cream — the odd one out on purpose |

Each comes as SVG plus PNG at 1024 / 512 / 320 / 200. `luxtipps-avatars.pdf` is
the one-page overview. Rebuild with `source/build_avatars.py` then
`source/export_avatars.py`; never hand-edit the output.
