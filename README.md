# lsprings

A very simple map app. Static page served by GitHub Pages, data prepared by Python.

## How it works

GitHub Pages only serves static files — no Python runs at request time. So:

- **`index.html`** — the whole UI. Leaflet + OpenStreetMap tiles, loaded from a CDN. No build step, no framework. Draws two radius rings around a fixed center point (`CENTER` at the top of the script): 3 mi in dark green, 5 mi in light green.
- **`scripts/build_data.py`** — standard library only. Reads `data/points.csv`, writes `points.json`.
- **`points.json`** — what the page fetches at load time. Committed, so Pages can serve it.

## Adding points

Edit `data/points.csv`, then regenerate:

```sh
python3 scripts/build_data.py
```

Commit both the CSV and the regenerated `points.json`.

## Running locally

```sh
python3 -m http.server 8000
```

Then open http://localhost:8000 — a plain `file://` open will not work, because the page fetches `points.json`.

## Dependencies

None to install. Python 3 standard library; Leaflet from CDN.

## Map contents

- Two radius rings around `CENTER` (30.580361, -97.837383): 3 mi dark green, 5 mi light green.
- **Texas Crushed Stone, Georgetown Quarry** (30.576111, -97.696666) — TCEQ RN102016482,
  about 8.4 mi east of center, outside the 5 mi ring.

### Texas Crushed Stone water use

Reported figure, not an estimate:

| | 2019 |
|---|---|
| Total | 1,106.82 acre-feet |
| Groundwater | 1,105.64 AF (99.9%) |
| Surface water | 1.17 AF (0.1%) |
| Approx. gallons | 361 million/yr (~988,000/day) |

Source: [TWDB/TCEQ Aggregate Mining Industry Water Use, Appendix III](https://www.twdb.texas.gov/waterplanning/data/projections/MiningStudy/doc/Final%20TWDB%20Mining%20Water%20Use%20Appendix%20III%20Jun%2015%202022.PDF),
Table 3-2, reporting year 2019. This single site is ~85% of all aggregate-mining
water use in Williamson County (county total: 1,308 AF).
