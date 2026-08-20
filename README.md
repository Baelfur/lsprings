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

Figures below come from the **project's own FAQ** at [leandersprings.us](https://leandersprings.us/)
(the developer's advocacy site). They supersede the numbers in news coverage, which had both
the aquifer and the volume wrong.

| | |
|---|---|
| Lagoon make-up | **9,072 gal/day — 10.2 acre-feet/yr** (~3.31M gal) |
| Source | On-site well, **Middle Trinity** confined sandstone |
| Screened interval | 527–737 ft, under ~520 ft of Gray Shale |
| Pump test | 95 gpm for 48 h; static recovery in ~4 h |
| Projected drawdown @ 1 mi | 3.2 ft @ 1 yr · 4.3 ft @ 10 yr · 5 ft @ 30 yr |
| Loop | Closed, recovers up to 80% |

77.9-acre mixed-use PUD anchored by a 4-acre Crystal Lagoon, 1,200 residential units,
275-room hotel. Council **denied** the PUD amendment in August 2025; an amended version
passed Planning & Zoning 5-1 on June 25, 2026 and returns to Council. The lagoon is
classified "non-essential," withholdable during severe drought.

**Corrections against earlier reporting.** The FAQ states the well does **not** draw from the
Lower Trinity: that zone was tested, found high in dissolved solids, and *sealed with
concrete*. Production is Middle Trinity only, at 527–737 ft — not the "Lower Trinity" or
"800-foot" well reported in June 2026. Volume is 10.2 AF/yr, ~20% above the 8–9 AF
evaporation figure that circulated.

**An internal inconsistency in their own materials.** The FAQ gives modeled make-up demand as
"approximately 20 gallons per minute annually." Read as a continuous rate that is 28,800
gal/day — **32 AF/yr, 3.2× the 9,072 gal/day stated elsewhere on the same page**. The 9,072
figure is the one their pump-test arithmetic supports: 95 gpm described as "about 15×" the
long-term average implies 6.3 gpm ≈ 9,120 gal/day. Against 20 gpm the same ratio would be
4.75×, not 15×. We use 9,072 gal/day and flag the gap rather than picking the larger number.
The page also carries a blanket caveat that data "is being reviewed and adjusted."

**The lagoon still is not the development's water.** Their density-cut claim — dropping 400
units "saving roughly 80,000 gallons of city water per day" — implies **200 gal/day/unit**. The
1,200 remaining units therefore draw ~240,000 gal/day of *city* water, about **269 AF/yr, or
26× the lagoon well**, before hotel, retail and office. The lagoon is the small half of this
project's water story, and it is the half that does not touch municipal supply.

For context, the FAQ's own comparison for the same 4 acres: apartments 16,000–30,000 gal/day
(18–34 AF/yr), commercial retail 18,000–25,000 (20–28 AF/yr), lagoon 9,072 (10 AF/yr).

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

Off by default — tick them in the top-right control. They draw in their own map pane
beneath every ring, circle and label, so turning one on never hides a data point.

Each aquifer ships as **two layers**, because the TWDB file's `AQUIFER` column separates
them and merging the two is misleading:

| Part | Meaning | Style |
|---|---|---|
| **outcrop** | where the aquifer reaches the surface — its recharge zone, and where shallower wells tap it | solid fill |
| **downdip** | where it continues in the subsurface beneath younger rock — still pumped, by deeper wells | faint fill, dashed edge |

Downdip extents **legitimately overlap** the aquifers mapped above them; that is stacked
geology, not a rendering error. Trinity's downdip is the extreme case — within the clip
box it covers 2,231 sq mi against the outcrop's 1,193, and statewide it runs east to
longitude −94.8:

| Layer | sq mi in box | % of box |
|---|---:|---:|
| Trinity — downdip | 2,231 | 56.5% |
| Trinity — outcrop | 1,193 | 30.2% |
| Edwards-BFZ — outcrop | 410 | 10.4% |
| Edwards-BFZ — downdip | 254 | 6.4% |
| Carrizo-Wilcox — outcrop | 210 | 5.3% |
| Carrizo-Wilcox — downdip | 2 | 0.0% |

Drawn as one merged Trinity layer it covered **87% of the map**, which buried the
distinction the pumpage figures rest on. Ticking the two *outcrops* together is the view
that matches the data: Edwards-BFZ east of the escarpment under Georgetown, Round Rock,
Texas Crushed Stone, MM-North and Brushy Creek; Trinity west of it under Leander Springs
and Liberty Hill.

Polygons carrying `AQUIFER = 0` are dropped. Every one tested sits enclosed inside a code
1 or 2 polygon, so they are windows *through* the aquifer, and filling them in overstated
each extent slightly.

A fourth rule, **Edwards-Trinity (Plateau)**, matches in the source but falls entirely
outside `BBOX` — it stays in `RULES` so a wider box picks it up.

Building `aquifers.json` takes one download, because the source is far too large to fetch
at page load — the statewide shapefile is 11 MB and the trimmed result is 204 KB (56 KB
gzipped):

```sh
curl -L -o data/major_aquifers.zip \
    https://www.twdb.texas.gov/mapping/gisdata/doc/major_aquifers.zip
python3 scripts/build_aquifers.py data/major_aquifers.zip
```

Commit the regenerated `aquifers.json`; the zip is gitignored. TWDB publishes a
**shapefile**, not GeoJSON, so the script reads `.shp`/`.dbf` out of the zip directly —
about 100 lines of stdlib struct unpacking, no converter and no extraction step. A `.shp`
or `.geojson` path works too.

The script clips to a box around Leander (`BBOX`), simplifies the outlines (`TOLERANCE`),
and drops everything outside the aquifers in `RULES` — all constants are at the top of the
file. It finds the aquifer-name attribute by looking rather than assuming, since TWDB has
shipped it as `AQ_NAME`, `AQUIFER`, and `AQUIFER_NAME` across releases; it prints which
field it used and every name it saw, so a mismatch is obvious. That reporting is what
caught the 2006 file naming the Balcones Fault Zone Edwards simply `EDWARDS`, which an
`("edwards", "balcones")` keyword rule silently skipped. To have a layer start switched
**on**, add it to the map in the `fetch('aquifers.json')` block in `index.html`.

Simplified outlines are for display. Anything that turns on an exact boundary should go
back to the TWDB source.

### Flow rate key — gallons per minute

A second key, bottom right of the map. The developer quotes flow rates; every other source
here reports annual volume. This ladder puts both on one axis with household fixtures as
rungs, so a figure like "20 gpm" can be sized against something familiar.

| | gpm | |
|---|---:|---|
| *Bathroom faucet* | 2.2 | typical fixture |
| *Shower head* | 2.5 | typical fixture |
| **LS lagoon, average** | **6.3** | their 9,072 gal/day |
| *Garden hose* | 10 | varies 5–15 with pressure |
| LS "20 gpm" figure | 20 | the FAQ's other number |
| MM-North Quarry | 45.9 | |
| LS 48-hour pump test | 95 | stress test, not operation |
| Cimarron Hills golf | 100 | |
| *Fire hose, 1¾ in line* | 150 | |
| LS apartments | 167 | city water, developer-implied |
| Texas Crushed Stone | 833 | |
| *Fire hydrant* | 1,000 | common design target |
| Georgetown, city | 5,111 | |

Site rates are **continuous equivalent** — the year's volume spread evenly over every minute
of it. No real well runs that way; they cycle. It is a like-for-like comparison, not a pump
specification. Italic rows are everyday references; the rest derive from the same `SITES` and
`GROUNDWATER` objects the map draws, at 1 AF/yr = 0.61996 gpm.

What the ladder shows: the lagoon's average draw sits between a shower head and a garden
hose. The FAQ's alternative "20 gpm" is twice a garden hose. The 48-hour pump test — which
nobody proposes to run continuously — lands just under a golf course. And the apartments
attached to the same project outrun a fire hose.

### Scale, for comparison

Multiples are against the lagoon's 10.2 AF/yr. The map carries this as its own **scale key**
(bottom left), built from the same objects it draws so the two cannot drift apart. Bars are
log-scaled and labelled as such — the range spans four orders of magnitude, and a linear bar
would render everything below Round Rock as a single invisible sliver.

| Site | AF/yr | vs lagoon |
|---|---|---|
| City of Georgetown | 8,244 (reported, 2024) | 811× |
| City of Round Rock | 1,450 (reported, 2024) | 143× |
| Texas Crushed Stone | 1,343.5 (reported, 2024) | 132× |
| Leander Springs, 1,200 units | ~269 (developer-implied) | 26× |
| Twin Creeks | ~189 (est) | 19× |
| City of Liberty Hill | 188 (reported, 2024) | 19× |
| Crystal Falls | ~180 (est) | 18× |
| Cimarron Hills | ~162 (est) | 16× |
| MM-North Austin Quarry | 74 (reported, 2024) | 7.3× |
| Brushy Creek MUD | 11.5 (reported, 2024) | 1.1× |
| **Leander Springs lagoon** | **10.2 (developer)** | 1× |
