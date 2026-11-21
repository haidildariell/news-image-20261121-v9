# Saturday 21 November 2026 — The World in One Day: 36 Stories, 6 Regions

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/haidildariell/news-image-20261121-v9/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard)
[![reward](https://make.fun/badge/news-image-20261121/haidildariell/news-image-20261121-v9/reward.svg)](https://make.fun/bounty/news-image-20261121)

One image that sums up the world's news of **Saturday 21 November 2026**:
36 dated stories across 6 regions — 13 illustrated cards with big-number
banners and source chips, a world map with numbered pins, a six-number
strip, and a 23-story one-line digest — laid out as a warm broadsheet
front page, "The World in One Day".

**What changed in v9: date discipline.** Recon of the live top 50 showed
every top entry polices the Saturday boundary twice — in what it selects
and in a DATE CHECK box that names Friday's news as excluded. The
previous edition broke that rule in a drawn card ("Wall Street's
$7 trillion week", a Friday close) and in a cumulative digest line.
v9 removes both, and in their place draws a discrete Saturday story
from the same verified set (the Los Angeles Palisades-fire verdict) and
adds two more dated digest items (Cape Town, Tokyo). Week wraps and
cumulative tolls are not Saturday news, so none appear.

Lead stories: COP31 runs into overtime in Antalya with no deal · three
Houthi missiles shot down over Riyadh · a magnitude 6.7 quake shakes
central Peru · Russia fires 148 drones overnight · BepiColombo reaches
Mercury · Bitcoin sinks to $55,100, its lowest since September 2024.

## How it is built

- `build_image.py` draws the 1024×1024 front page with Pillow
  (deterministic: fixed fonts, fixed layout, no network, no randomness;
  all 13 illustrations are drawn in code — no photographs, no copied
  artwork).
- `main.py` (Python standard library only) copies the rendered
  `entry.png` to `MAKEFUN_OUTPUT_DIR` and verifies the copy byte-for-byte
  by SHA-256 before reporting success.
- `stories_20261121.json` holds all 36 stories — drawn unchanged in fact
  from the 50-story verified set built for an earlier edition of this
  entry; `SOURCES.md` names the outlet behind each one. No facts were
  added or changed.

## Run

```sh
python3 build_image.py          # renders entry.png here
MAKEFUN_OUTPUT_DIR=out python3 main.py   # copies entry.png to out/
```

Entry for the [make.fun bounty](https://make.fun/bounty/news-image-20261121)
`news-image-20261121` (deadline 23 November 2026 07:00 WIB, top 50 share
$100). License: MIT.
