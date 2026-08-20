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

### Golf courses — estimated volumes

None of the three publish a facility-level figure. Each is estimated the same way:
course polygon from OpenStreetMap → irrigated turf → × ~1.8 AF/acre, where the rate is
derived from Central Texas ET (ETo ~62 in × Kc 0.60) less effective rainfall, at 75%
irrigation efficiency. Because the method is identical and all three are 18-hole courses,
the results cluster — the spread between them is noise, not signal.

| Course | Polygon | Turf | Est. AF/yr | Est. gal/yr | Water source |
|---|---|---|---|---|---|
| [Cimarron Hills](https://www.openstreetmap.org/way/104049185) (Georgetown) | 131 ac | ~90 ac | ~162 | ~53M | Reclaimed — Georgetown ✅ |
| [Crystal Falls](https://www.openstreetmap.org/relation/7363676) (Leander) | 155 ac | ~100 ac | ~180 | ~59M | Reclaimed — Travisso WRP ⚠️ |
| [Twin Creeks](https://www.openstreetmap.org/relation/3203627) (Cedar Park) | 247 ac | ~105 ac | ~189 | ~62M | Not documented ❌ |

✅ documented and named · ⚠️ documented but course not named explicitly · ❌ unknown

Combined, the three courses come to ~531 AF/yr — about **48% of the quarry alone**.

Sources: [Georgetown Water Resources FAQ](https://georgetowntexas.gov/utilities/water/resources/faqs/index.php) ·
[Leander Water & Wastewater](https://www.leandertx.gov/506/Water-Wastewater) ·
[Leander Golf Course directory](https://www.leandertx.gov/Directory.aspx?did=71) ·
[Cedar Park Water Conservation Plan](https://ecode360.com/38630314) ·
[GCSAA Phase III water report](https://www.gcsaa.org/docs/default-source/environment/22_waterreport_web.pdf) ·
[TWDB BMP 5.2](https://www.twdb.texas.gov/conservation/BMPs/Mun/doc/5.2.pdf)
