# News — Tuesday 24 November 2026

[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/zhengxinjia82-dev/news-2026-11-24/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/zhengxinjia82-dev/news-2026-11-24/reward.svg)](https://make.fun/bounty/news-image-20261124)

A one-page newspaper front page for Tuesday 24 November 2026: **41 stories
from 7 regions**, all of which happened or were first reported on that day.

- 3 big headlines with code-drawn illustrations (Gaza, Asian markets, Russian
  war dead)
- 10 illustrated secondary stories
- 28 one-line briefs
- UTC timeline, dot-matrix world map, numbers bar, and a DATE CHECK box that
  leaves out older news (El Chapo Isidro's capture was 21 Nov; the federal
  executions memo, the Grok suits, the Ukraine warship sinking, Huang's
  Nvidia return and the Russian satellite warning were all 23 Nov) and items
  not yet happened (the Miss Universe final is tonight; the Bank of Korea
  rate call is Thursday).

## How to run

```sh
python3 draw.py   # renders entry.png (1024x1024)
```

`main.ts` copies the drawn image to `/output/entry.png`:

```sh
node --experimental-strip-types main.ts
```

## Sources

Every story carries a verification badge (CONFIRMED / REPORTED / CLAIM /
OFFICIAL) and a source. Sources used: Reuters, AP, AFP, Japan Times, SCMP,
Manila Times, Gulf News, JPost, UN News, NewsCord. No real photographs —
all illustrations are drawn in code.

## License

MIT — see [LICENSE](LICENSE).
