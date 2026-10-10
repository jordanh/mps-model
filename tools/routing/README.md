# Routing tools

These scripts build the two routing tables the model reads. Both are checked in, so the model runs
offline and you only need these tools to rebuild them (a new Overture release, a corrected address,
or different speed assumptions).

| Output | What it is |
|---|---|
| `data/compiled/school_locations.csv` | Each school's street address geocoded to an Overture address point, with how it matched and the distance to the named place of the same school |
| `data/compiled/school_drive_matrix.csv` | Road miles and driving minutes along the fastest route for every ordered pair of the 60 schools (3,600 rows) |
| `data/compiled/school_drive_matrix_meta.json` | When and how the table was built: release, network size, settings, construction closures ignored |

## Rebuild

```bash
pip install -r tools/routing/requirements.txt
python tools/routing/fetch_overture.py        # about 50 MB from the public Overture bucket, into tools/routing/cache/
python tools/routing/geocode_schools.py       # reads tools/routing/school_addresses.csv
python tools/routing/build_drive_matrix.py    # about 40 seconds
python -m mps_model run                       # rerun the model on the new table
```

`build_drive_matrix.py --traffic-scale 0.8 --out other.csv` writes a slower-traffic table without
touching the checked-in one.

## How it works

- **Roads.** Overture Maps transportation segments (OpenStreetMap data), release `2026-09-23.1`, in
  the box set in `settings.json` (Minneapolis plus about a mile of margin). Drivable classes only.
  Segments are split at their connectors into a directed graph; one-way streets and closures come
  from each segment's access restrictions. Closures tagged "under construction" are treated as open
  because the plan starts in fall 2027 (in this release: the Penn Avenue bridge over I-394 and a
  stretch of Nicollet Avenue).
- **Speed.** Posted limit where OpenStreetMap has one (about 40% of drivable segments), otherwise the class
  default in `settings.json` (Minneapolis's 20 mph residential and 25 mph city-street defaults),
  times a traffic factor for signals, stops and school-hour traffic (0.70 arterials, 0.75 local
  streets, 0.85 freeways). The factor is an ESTIMATE; no live traffic data is used.
- **Schools.** Each address in `school_addresses.csv` is matched to an Overture address point by
  house number and normalized street name, then attached to the nearest local or arterial street
  node. Two corrections came out of this: Las Estrellas is at 1201 University Ave NE (the earlier
  table gave Ella Baker's building), and Northrop's position on the pathway map was about 1.1 miles
  off. Anishinabe uses its planned site, as the district's plans do.
- **Routes.** Fastest path by minutes (Dijkstra) from each school to every other. The table keeps
  both directions, which can differ on one-way streets.

## Data licenses

Road data © OpenStreetMap contributors, available under the Open Database License (ODbL), via the
Overture Maps Foundation. The drive-time table is derived from it, so a published copy should carry
that attribution. Address points come from the open sources listed in each Overture record; places
are CDLA-Permissive-2.0.
