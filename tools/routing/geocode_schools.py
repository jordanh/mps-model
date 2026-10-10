"""Step 2: geocode each school's street address against Overture Maps address points.

    python tools/routing/geocode_schools.py     # reads school_addresses.csv, writes data/compiled/school_locations.csv

Matching: house number and street name after normalizing abbreviations (Avenue -> Ave, 46th -> 46,
"E 46th St" -> "46 St E"). If the address table omits a street direction that the address points
carry, the match is accepted only when every candidate lies within a few hundred feet. If the house
number itself has no point, the nearest number on the same street (within 60) is used.
Each result is then checked against the Overture "places" point of the same name, when one exists.
"""
import re
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq
import shapely

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
OUT = REPO / "data" / "compiled" / "school_locations.csv"
MILES_PER_DEG_LAT = 69.0

WORDS = {"AVENUE": "AVE", "AV": "AVE", "STREET": "ST", "BOULEVARD": "BLVD", "PARKWAY": "PKWY", "ROAD": "RD",
         "DRIVE": "DR", "PLACE": "PL", "LANE": "LN", "TERRACE": "TER", "CIRCLE": "CIR", "NORTH": "N", "SOUTH": "S",
         "EAST": "E", "WEST": "W", "NORTHEAST": "NE", "SOUTHEAST": "SE", "NORTHWEST": "NW", "SOUTHWEST": "SW"}
DIRECTIONS = {"N", "S", "E", "W", "NE", "SE", "NW", "SW"}


def normalize(street):
    words = [WORDS.get(w, w) for w in re.sub(r"[^A-Z0-9 ]", " ", str(street).upper()).split()]
    words = [re.sub(r"^(\d+)(ST|ND|RD|TH)$", r"\1", w) for w in words]
    if len(words) > 2 and words[0] in DIRECTIONS:   # "E 46 ST" -> "46 ST E"
        words = words[1:] + words[:1]
    return " ".join(words)


def without_direction(street):
    return " ".join(w for w in street.split() if w not in DIRECTIONS)


def points(table):
    geometry = shapely.from_wkb(table.geometry.values)
    return table.assign(lon=shapely.get_x(geometry), lat=shapely.get_y(geometry))


def miles_between(lat1, lon1, lat2, lon2):
    return np.hypot((lat1 - lat2) * MILES_PER_DEG_LAT, (lon1 - lon2) * MILES_PER_DEG_LAT * np.cos(np.radians(lat1)))


def geocode(address, book):
    number, street = re.match(r"\s*(\d+)\s+([^,]+),", address).groups()
    street = normalize(street)
    hit = book[(book.number == number) & (book.street_n == street)]
    if not hit.empty:
        return hit, "exact"
    hit = book[(book.number == number) & (book.street_nd == without_direction(street))]
    if not hit.empty and miles_between(hit.lat.min(), hit.lon.min(), hit.lat.max(), hit.lon.max()) < 0.4:
        return hit, "exact (street direction added)"
    same_street = book[(book.street_n == street) & book.number.str.fullmatch(r"\d+")]
    if not same_street.empty:
        gap = (same_street.number.astype(int) - int(number)).abs()
        nearest = same_street[gap == gap.min()]
        if gap.min() <= 60:
            return nearest.head(1), f"nearest house number ({nearest.number.iloc[0]})"
    return book.iloc[0:0], "not found"


def main():
    schools = pd.read_csv(HERE / "school_addresses.csv").fillna("")
    book = points(pq.read_table(HERE / "cache" / "addresses.parquet").to_pandas())
    book["number"] = book.number.astype(str).str.strip()
    book["street_n"] = book.street.map(normalize)
    book["street_nd"] = book.street_n.map(without_direction)
    places = points(pq.read_table(HERE / "cache" / "places.parquet").to_pandas())
    places["name"] = places.names.map(lambda n: (n or {}).get("primary") or "")

    rows = []
    for s in schools.itertuples():
        hit, how = geocode(s.address, book)
        if hit.empty:
            raise SystemExit(f"Could not geocode {s.school}: {s.address}")
        lat, lon = hit.lat.median(), hit.lon.median()
        key = {"HIA": "hmong", "FAIR": "fair"}.get(s.school, s.school.split()[0].lower())
        named = places[places.name.str.lower().str.contains(key, regex=False)]
        check = round(float(miles_between(lat, lon, named.lat, named.lon).min()), 2) if len(named) else np.nan
        rows.append({"school": s.school, "address": s.address, "lat": round(lat, 6), "lon": round(lon, 6),
                     "match": how, "miles_to_named_place": check, "address_source": s.source, "note": s.note})
    out = pd.DataFrame(rows)
    out.to_csv(OUT, index=False)
    print(out.match.value_counts().to_string())
    far = out[out.miles_to_named_place > 0.2]
    print(f"Wrote {OUT.relative_to(REPO)}. Named place more than 0.2 mi away for: "
          + (", ".join(f"{r.school} ({r.miles_to_named_place} mi)" for r in far.itertuples()) or "none"))


if __name__ == "__main__":
    main()
