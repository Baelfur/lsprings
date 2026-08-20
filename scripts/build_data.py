"""Build points.json from data/points.csv. Standard library only."""

import csv
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "points.csv"
OUTPUT = ROOT / "points.json"


def build():
    points = []
    with SOURCE.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            points.append(
                {
                    "name": row["name"],
                    "lat": float(row["lat"]),
                    "lon": float(row["lon"]),
                    "note": row.get("note", ""),
                }
            )

    OUTPUT.write_text(json.dumps(points, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(points)} points to {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    build()
