"""Build aquifers.json from a TWDB aquifer GeoJSON export. Standard library only.

The statewide TWDB layer is tens of megabytes -- far too big to fetch on page
load. This trims it to what the map actually shows: the aquifers we name, clipped
to a box around Leander, with the outlines simplified.

Download the source first (this repo's build environment has no network access
to twdb.texas.gov, so it is a manual step):

    https://www.twdb.texas.gov/mapping/gisdata.asp  ->  Major Aquifers

Take the GeoJSON export and save it as data/aquifers_source.geojson, then:

    python3 scripts/build_aquifers.py [path/to/source.geojson]
"""

import json
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_SOURCE = ROOT / "data" / "aquifers_source.geojson"
OUTPUT = ROOT / "aquifers.json"

# Clip box around the map's contents: roughly 40 mi either side of CENTER.
# (min lon, min lat, max lon, max lat)
BBOX = (-98.40, 30.20, -97.20, 31.00)

# Douglas-Peucker tolerance in degrees. ~0.001 deg is ~110 m, which is well
# under a pixel at the zoom levels this map opens at.
TOLERANCE = 0.001

# Drop clipped rings smaller than this (square degrees) -- slivers along the
# clip edge that would only add bytes.
MIN_RING_AREA = 1e-6

# Ordered: the first rule whose keywords all appear in the name wins, so
# "Edwards-Trinity" and "Edwards (Balcones Fault Zone)" are both settled
# before the bare "Trinity" rule can claim them.
RULES = [
    ("edwards-trinity", "Edwards-Trinity (Plateau)", "#6b8f3a", ("edwards", "trinity")),
    ("edwards-bfz", "Edwards (Balcones Fault Zone)", "#2a7a9b", ("edwards", "balcones")),
    ("trinity", "Trinity", "#8a6d3b", ("trinity",)),
    ("carrizo-wilcox", "Carrizo-Wilcox", "#9b4a6f", ("carrizo",)),
]


def find_name_field(features):
    """TWDB has shipped this attribute as AQ_NAME, AQUIFER, and AQUIFER_NAME
    across releases, so look rather than assume."""
    keys = []
    for f in features[:50]:
        for k in (f.get("properties") or {}):
            if k not in keys:
                keys.append(k)
    for want in ("aq_name", "aquifer_name", "aquifer", "aq_nam", "name"):
        for k in keys:
            if k.lower() == want:
                return k
    for k in keys:  # last resort: anything name-ish
        if "name" in k.lower() or "aquifer" in k.lower():
            return k
    return None


def classify(name):
    low = (name or "").lower()
    for key, label, color, words in RULES:
        if all(w in low for w in words):
            return key, label, color
    return None


def clip_ring(ring, bbox):
    """Sutherland-Hodgman against the (convex) clip box."""
    min_x, min_y, max_x, max_y = bbox

    def inside(p, edge):
        if edge == 0: return p[0] >= min_x
        if edge == 1: return p[0] <= max_x
        if edge == 2: return p[1] >= min_y
        return p[1] <= max_y

    def cut(a, b, edge):
        (x1, y1), (x2, y2) = a, b
        if edge < 2:  # vertical edge: x is fixed
            x = min_x if edge == 0 else max_x
            t = (x - x1) / (x2 - x1)
            return (x, y1 + t * (y2 - y1))
        y = min_y if edge == 2 else max_y
        t = (y - y1) / (y2 - y1)
        return (x1 + t * (x2 - x1), y)

    out = [tuple(p[:2]) for p in ring]
    if out and out[0] == out[-1]:
        out.pop()
    for edge in range(4):
        if not out:
            return []
        buf, prev = [], out[-1]
        for cur in out:
            if inside(cur, edge):
                if not inside(prev, edge):
                    buf.append(cut(prev, cur, edge))
                buf.append(cur)
            elif inside(prev, edge):
                buf.append(cut(prev, cur, edge))
            prev = cur
        out = buf
    return out


def simplify(pts, tol):
    """Douglas-Peucker, iterative so a long coastline-ish ring cannot blow the
    recursion limit."""
    if len(pts) < 3:
        return pts
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        lo, hi = stack.pop()
        if hi <= lo + 1:
            continue
        (x1, y1), (x2, y2) = pts[lo], pts[hi]
        dx, dy = x2 - x1, y2 - y1
        norm = math.hypot(dx, dy)
        far_i, far_d = -1, tol
        for i in range(lo + 1, hi):
            x0, y0 = pts[i]
            if norm == 0:
                d = math.hypot(x0 - x1, y0 - y1)
            else:
                d = abs(dy * x0 - dx * y0 + x2 * y1 - y2 * x1) / norm
            if d > far_d:
                far_i, far_d = i, d
        if far_i != -1:
            keep[far_i] = True
            stack.append((lo, far_i))
            stack.append((far_i, hi))
    return [p for p, k in zip(pts, keep) if k]


def ring_area(pts):
    a = 0.0
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        a += x1 * y2 - x2 * y1
    return abs(a) / 2


def prepare(ring):
    clipped = clip_ring(ring, BBOX)
    if len(clipped) < 3 or ring_area(clipped) < MIN_RING_AREA:
        return None
    pts = simplify(clipped, TOLERANCE)
    if len(pts) < 3:
        return None
    pts = [[round(x, 5), round(y, 5)] for x, y in pts]
    if pts[0] != pts[-1]:
        pts.append(pts[0])
    return pts


def polygons(geom):
    """Yield each polygon (list of rings) from a Polygon or MultiPolygon."""
    t = (geom or {}).get("type")
    if t == "Polygon":
        yield geom["coordinates"]
    elif t == "MultiPolygon":
        yield from geom["coordinates"]


def build(source):
    raw = json.loads(source.read_text(encoding="utf-8"))
    features = raw.get("features") or []
    if not features:
        sys.exit(f"no features in {source}")

    field = find_name_field(features)
    if not field:
        sys.exit(f"could not find an aquifer-name field in {source}; "
                 f"properties seen: {sorted((features[0].get('properties') or {}))}")
    print(f"name field: {field}")

    buckets, seen, skipped = {}, set(), set()
    for feat in features:
        name = (feat.get("properties") or {}).get(field)
        seen.add(name)
        hit = classify(name)
        if not hit:
            skipped.add(name)
            continue
        key, label, color = hit
        rings_out = []
        for poly in polygons(feat.get("geometry")):
            kept = [r for r in (prepare(ring) for ring in poly) if r]
            if kept:
                rings_out.append(kept)
        if not rings_out:
            continue
        b = buckets.setdefault(key, {"key": key, "name": label, "color": color,
                                     "geojson": {"type": "FeatureCollection", "features": []}})
        for rings in rings_out:
            b["geojson"]["features"].append(
                {"type": "Feature", "properties": {"aquifer": label},
                 "geometry": {"type": "Polygon", "coordinates": rings}})

    ordered = [buckets[k] for k, _, _, _ in RULES if k in buckets]
    OUTPUT.write_text(json.dumps({"bbox": list(BBOX), "aquifers": ordered}) + "\n",
                      encoding="utf-8")

    print(f"read {len(features)} features, {len(seen)} distinct aquifer names")
    for a in ordered:
        pts = sum(len(r) for f in a["geojson"]["features"] for r in f["geometry"]["coordinates"])
        print(f"  kept {a['name']:<32} {len(a['geojson']['features']):>3} polygons  {pts:>5} points")
    if skipped:
        print(f"  outside our four: {', '.join(sorted(str(s) for s in skipped))}")
    if not ordered:
        sys.exit("no aquifers matched -- check the name field values above")
    print(f"wrote {OUTPUT.relative_to(ROOT)} ({OUTPUT.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    src = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SOURCE
    if not src.exists():
        sys.exit(f"missing {src}\nDownload the TWDB Major Aquifers GeoJSON first "
                 f"-- see the docstring at the top of this file.")
    build(src)
