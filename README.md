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

Two reference rings around `CENTER` (30.580361, -97.837383): 3 mi dark green, 5 mi light green.
Two water-use sites, each drawn as a **half-mile red circle** with a label and a popup
carrying the figures and source links.

### Texas Crushed Stone — Georgetown Quarry

30.576111, -97.696666 · TCEQ RN102016482 · **reported figure**

| | |
|---|---|
| Total | 1,106.82 acre-feet (2019) |
| Groundwater | 1,105.64 AF (99.9%) |
| Surface water | 1.17 AF (0.1%) |
| Approx. | 361 million gal/yr (~988,000/day) |

~85% of all aggregate-mining water use in Williamson County (county total 1,308 AF).

Sources: [TWDB/TCEQ Aggregate Mining Water Use App. III](https://www.twdb.texas.gov/waterplanning/data/projections/MiningStudy/doc/Final%20TWDB%20Mining%20Water%20Use%20Appendix%20III%20Jun%2015%202022.PDF) ·
[App. IV](https://www.twdb.texas.gov/waterplanning/data/projections/MiningStudy/doc/Final%20TWDB%20Mining%20Water%20Use%20Appendix%20IV%20Jun%2015%202022.PDF) ·
[USGS site](https://waterdata.usgs.gov/monitoring-location/USGS-948491085135000/)

### Cimarron Hills Golf & Country Club

30.648033, -97.789618 · **estimated volume, documented source**

| | |
|---|---|
| Total | ~162 acre-feet/yr (range 135–225) |
| Approx. | ~53 million gal/yr (~145,000/day) |
| Source | Reclaimed water — City of Georgetown |

No facility-level volume is published. Estimate = 131-acre course polygon
(OSM way/104049185) → ~90 ac irrigated turf × ~1.8 AF/acre, where the rate comes from
Central Texas ET (ETo ~62 in × Kc 0.60) less effective rainfall, at 75% irrigation
efficiency. The **source** is documented, not estimated: all six Georgetown golf courses
irrigate with reclaimed water.

Sources: [Georgetown Water Resources FAQ](https://georgetowntexas.gov/utilities/water/resources/faqs/index.php) ·
[GCSAA Phase III water report](https://www.gcsaa.org/docs/default-source/environment/22_waterreport_web.pdf) ·
[TWDB BMP 5.2](https://www.twdb.texas.gov/conservation/BMPs/Mun/doc/5.2.pdf) ·
[OSM way/104049185](https://www.openstreetmap.org/way/104049185)
