# lsprings

A very simple map app. Static page served by GitHub Pages, data prepared by Python.

## How it works

GitHub Pages only serves static files — no Python runs at request time. So:

- **`index.html`** — the whole UI. Leaflet + OpenStreetMap tiles, loaded from a CDN. No build step, no framework. Draws two radius rings around a fixed center point (`CENTER` at the top of the script): 3 mi in dark green, 5 mi in light green. Every site on the map is a JS literal in this file — `SITES` (red circles) and `GROUNDWATER` (dashed purple circles).
- **`scripts/build_data.py`** — standard library only. Reads `data/points.csv`, writes `points.json`.
- **`scripts/build_aquifers.py`** — standard library only. Trims a TWDB aquifer download into `aquifers.json`. See [Aquifer extents](#aquifer-extents).
- **`points.json`**, **`aquifers.json`** — what the page fetches at load time. Committed, so Pages can serve them. Both are optional; the map still draws without either.

Everything on the map is grouped into toggles in the top-right control: the four
feature groups (Leander Springs, water use sites, groundwater pumpage, the rings)
and one entry per aquifer extent.

The 3 and 5 mile rings are context, not data. They draw in their own pane between the
aquifer washes and the site circles, so nothing ever hides behind them, and each ring is
two paths: an inert filled wash (`interactive: false`, so the square miles it covers never
swallow a click meant for a site) plus a stroke-only outline that takes a hover and names
the radius. Neither has a popup.

## Adding points

Note the map's own contents are **not** built from the CSV — `SITES` and `GROUNDWATER`
are hardcoded in `index.html`, and that is where a new water user with figures, a
provenance badge, and sources belongs. The CSV pipeline below adds plain unstyled pins
on top, for scratch or reference locations.

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

**Leander Springs** sits at `CENTER` (30.580361, -97.837383) — the SW corner of US 183A
and RM 2243 — drawn as a blue point. The 3 mi (dark green) and 5 mi (light green) rings
are measured from it. Everything else on the map is a large water user around it.

### Leander Springs — developer estimate

| | |
|---|---|
| Lagoon evaporation | **8–9 acre-feet/yr** |
| Approx. | 2.6–2.9 million gal/yr (~7,600 gal/day) |
| Source | On-site 800 ft well, Lower Trinity Aquifer |
| City backup | up to 200,000 gal/day, Dec–Feb off-peak only |
| Loop | Closed, recycles 80–95% |

77.9-acre mixed-use PUD anchored by a 4-acre Crystal Lagoon. Amended PUD approved by
Planning & Zoning 5-1 on June 25, 2026; advancing to City Council. Lagoon is now
classified "non-essential" and can be withheld during severe drought.

Two caveats the headline number hides:

- **8–9 AF is lagoon evaporation only**, not the development's total demand. 1,200
  apartments at ~150 gpd/unit is ~202 AF/yr on its own — roughly 24× the lagoon figure,
  before hotel, retail, and office. *(That multiplier is our arithmetic, not from their studies.)*
- **~25 in/yr over 4 acres** is at or just below ordinary Central Texas net evaporation
  (~26–36 in/yr), before crediting the claimed 50–80% evaporation reduction from VVater's technology. Plausible, but
  not conservative. The city backup allowance (200,000 gal/day × ~90 days ≈ 55 AF) is
  ~6× the claimed annual loss.

Sources: [Community Impact, Jun 2026](https://communityimpact.com/austin/leander-liberty-hill/development/2026/06/29/lagoon-anchored-leander-springs-development-advances-to-leander-city-council/) ·
[Community Impact, Jan 2021 water agreement](https://communityimpact.com/austin/cedar-park-leander/development/2021/01/22/council-oks-1b-leander-springs-development-addresses-water-concerns-in-agreement/) ·
[Crystal Lagoons](https://www.crystal-lagoons.com/leander-city-texas-reveals-4-acre-amenity-by-crystal-lagoons-to-anchor-1b-mixed-use-development/)

### Verified groundwater withdrawals within ~15 mi

From the TWDB Water Use Survey, **Detailed Groundwater Pumpage by County** (Williamson,
reporting year 2024) — self-reported by each entity to the state, with aquifer and well count.

| Entity | mi | AF/yr | Mgal | Aquifer | Wells | vs lagoon |
|---|---:|---:|---:|---|---:|---:|
| City of Georgetown | 10.2 | 8,244 | 2,686 | Edwards-BFZ | 4 | 970× |
| City of Round Rock | 10.7 | 1,450 | 472 | Edwards-BFZ | 3 | 171× |
| Texas Crushed Stone | 8.4 | 1,344 | 438 | Edwards-BFZ | 1 | 158× |
| City of Liberty Hill | 7.7 | 188 | 61 | **Trinity** | 4 | 22× |
| MM-North Austin Quarry | 9.0 | 74 | 24 | Edwards-BFZ | 1 | 8.7× |
| Brushy Creek MUD | 6.5 | 11.5 | 3.7 | Edwards-BFZ | 3 | 1.4× |

Combined: **~11,300 AF/yr**, about 1,300× the Leander Springs lagoon estimate.

Just outside the radius, for reference: Jonah Water SUD (18.0 mi, 1,479 AF, 9 wells) and
City of Hutto (17.5 mi, 900 AF, Carrizo-Wilcox, 6 wells).

Municipal rows are **system-wide** pumpage across multiple well fields — the map marker is a
representative location for the service area, not a wellhead.

**Texas Crushed Stone updated**: the 2024 pumpage report gives 1,343.5 AF (437,788,200 gal),
up 21% from the 1,106.82 AF in the 2019 mining survey. The map now shows the 2024 figure.

**Regulatory context**: Williamson County has **no groundwater conservation district**, so
wells here are not permitted or metered by any district. Everything above is self-reported
to TWDB, and the "non-surveyed estimate" rows in the same report — TWDB's own estimate of
unmetered domestic, livestock, and irrigation pumping — add several hundred million gallons
a year countywide on top.

Sources: [TWDB Detailed Groundwater Pumpage by County](https://www3.twdb.texas.gov/apps/reports/WU_REP/SumFinal_CountyPumpage) ·
[TWDB Historical Groundwater Pumpage](https://www.twdb.texas.gov/waterplanning/waterusesurvey/historical-pumpage.asp) ·
[Williamson County — why the county needs a GCD](https://www.wilcotx.gov/CivicAlerts.aspx?AID=42)

### Aquifer extents

Off by default — tick them in the top-right control. Each is the TWDB **mapped extent**,
outcrop and downdip together: where the aquifer *exists*, not where anyone is pumping it.
They draw in their own map pane beneath every ring, circle and label, so turning one on
never hides a data point.

Four are carried, the same four the figures above name: **Trinity** (the Leander Springs
well and Liberty Hill), **Edwards (Balcones Fault Zone)** (Georgetown, Round Rock, Texas
Crushed Stone, MM-North, Brushy Creek), **Edwards-Trinity (Plateau)**, and
**Carrizo-Wilcox** (the Hutto reference).

Building `aquifers.json` takes one manual download, because the source is far too large
to fetch at page load — the statewide layer is tens of megabytes, and the trimmed result
is a few dozen KB:

1. Get **Major Aquifers** from [TWDB GIS Data](https://www.twdb.texas.gov/mapping/gisdata.asp) as GeoJSON.
2. Save it as `data/aquifers_source.geojson` (gitignored).
3. Run `python3 scripts/build_aquifers.py`, and commit the regenerated `aquifers.json`.

The script clips to a box around Leander (`BBOX`), simplifies the outlines
(`TOLERANCE`), and drops everything outside the four aquifers in `RULES` — all four
constants are at the top of the file. It finds the aquifer-name attribute by looking
rather than assuming, since TWDB has shipped it as `AQ_NAME`, `AQUIFER`, and
`AQUIFER_NAME` across releases; it prints which field it used and every name it saw, so
a mismatch is obvious. To have a layer start switched **on**, add it to the map in the
`fetch('aquifers.json')` block in `index.html`.

Simplified outlines are for display. Anything that turns on an exact boundary should go
back to the TWDB source.

### Scale, for comparison

| Site | AF/yr | vs lagoon |
|---|---|---|
| Texas Crushed Stone | 1,343.5 (reported, 2024) | 158× |
| Twin Creeks | ~189 (est) | 22× |
| Crystal Falls | ~180 (est) | 21× |
| Cimarron Hills | ~162 (est) | 19× |
| **Leander Springs lagoon** | **8.5 (developer)** | 1× |

Four water-use sites, each drawn as a **half-mile red circle** with a label and a popup
carrying the figures and source links.

### Texas Crushed Stone — Georgetown Quarry

30.576111, -97.696666 · TCEQ RN102016482 · **reported figure**

| | |
|---|---|
| Total | 1,343.5 acre-feet (2024) |
| Approx. | 438 million gal/yr (~1.20M/day) |
| Source | Groundwater, Edwards-BFZ Aquifer |
| Wells | 1 reported (2024) |
| 2019 | 1,106.82 AF — up 21% since |

The 2019 mining survey broke that year down as 1,105.64 AF groundwater (99.9%) and
1.17 AF surface water — ~85% of all aggregate-mining water use in Williamson County
(county total 1,308 AF).

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

Combined, the three courses come to ~531 AF/yr — about **40% of the quarry alone**.

Sources: [Georgetown Water Resources FAQ](https://georgetowntexas.gov/utilities/water/resources/faqs/index.php) ·
[Leander Water & Wastewater](https://www.leandertx.gov/506/Water-Wastewater) ·
[Leander Golf Course directory](https://www.leandertx.gov/Directory.aspx?did=71) ·
[Cedar Park Water Conservation Plan](https://ecode360.com/38630314) ·
[GCSAA Phase III water report](https://www.gcsaa.org/docs/default-source/environment/22_waterreport_web.pdf) ·
[TWDB BMP 5.2](https://www.twdb.texas.gov/conservation/BMPs/Mun/doc/5.2.pdf)
