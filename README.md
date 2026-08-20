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
  (~26–36 in/yr), before crediting the claimed 50–80% VVater reduction. Plausible, but
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
| MM-North Austin Quarry | 9.0 | 74 | 24 | Edwards-BFZ | 1 | 9× |
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

### Scale, for comparison

| Site | AF/yr | vs lagoon |
|---|---|---|
| Texas Crushed Stone | 1,107 (reported) | 130× |
| Twin Creeks | ~189 (est) | 22× |
| Crystal Falls | ~180 (est) | 21× |
| Cimarron Hills | ~162 (est) | 19× |
| **Leander Springs lagoon** | **8.5 (developer)** | 1× |
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
