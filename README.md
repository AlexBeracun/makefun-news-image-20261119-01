# makefun-news-image-20261119-01

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/AlexBeracun/makefun-news-image-20261119-01/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/AlexBeracun/makefun-news-image-20261119-01/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One image summing up Thursday 19 November 2026's world news, as a
newspaper front page: "THE WORLD IN ONE PAGE" — 32 verified stories
across six continents.

Lead story: GTA VI launch day — Rockstar's Vice City epic lands on PS5
and Xbox, first reviews score 99/100 as 2.3m watch on Twitch. Then four
feature panels (Hakeem Jeffries nominated 251–11, set to become the first
Black Speaker of the US House; Anthropic's record $81.3bn IPO, priced at
$83 and valued at $1.5tn, debuting on Nasdaq; the Crimean Bridge struck
overnight for the third time in a week; the Trump–Xi–Putin trilateral at
the APEC summit in Shenzhen) plus 27 briefs: the ICJ's Rohingya genocide
ruling, North Korea's missile launches, four nations demanding aid access
to flooded Gaza, Eisenkot tapped to lead Israel's next government, the
$12bn Venezuelan oil report, France's fourth week of cost-of-living
protests, the EU's Indonesia trade pact and €45bn Ukraine loan, the NSA
outage, Cyclone Akvan, PV Sindhu's return to badminton's top five, and
more. Every event happened or was first reported on 19 November 2026.

## How it is built

`gen_image.py` renders `entry.png` (1024×1024, Pillow + system fonts)
from the day's wire reports. `main.py` is the graded entry: Python 3.13,
standard library only, no network — it just copies `entry.png` to the
output directory, so two runs write identical bytes.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# out/entry.png — 1024x1024 PNG, under 1 MiB
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=ajkq5baq&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
