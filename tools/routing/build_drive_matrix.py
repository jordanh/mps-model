"""Step 3: driving miles and minutes between every pair of schools, on the real street network.

    python tools/routing/build_drive_matrix.py   # writes data/compiled/school_drive_matrix.csv (+ _meta.json)
    python tools/routing/build_drive_matrix.py --traffic-scale 0.8 --out /tmp/slower.csv   # a sensitivity case

Network: every drivable Overture road segment (OpenStreetMap data) in the settings.json box, split at
its connectors. Each piece gets
  * its posted speed limit, or a default for its road class where none is tagged, times a traffic
    factor for signals, stops and school-hour traffic (settings.json; an ESTIMATE);
  * one-way direction and closures from its access restrictions. Closures flagged
    "under construction" are ignored, since the plan runs from fall 2027 (in the 2026-09 data this
    reopens the Penn Avenue bridge over I-394 and a stretch of Nicollet Avenue).
Each school is attached to the nearest node on a local or arterial street (not a freeway, ramp or
driveway). Routes are fastest paths (Dijkstra on minutes); the table stores the time and the road
length of that path, in both directions.
"""
import argparse
import heapq
import json
import math
from datetime import date
from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd
import pyarrow.parquet as pq
import shapely

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
LOCATIONS = REPO / "data" / "compiled" / "school_locations.csv"
OUT = REPO / "data" / "compiled" / "school_drive_matrix.csv"
EARTH_RADIUS_MI = 3958.8
CONNECT_CLASSES = {"primary", "secondary", "tertiary", "unclassified", "residential", "living_street"}
CAR_MODES = {"motor_vehicle", "car", "vehicle"}


def haversine(lon1, lat1, lon2, lat2):
    p = math.pi / 180
    a = math.sin((lat2 - lat1) * p / 2) ** 2 + math.cos(lat1 * p) * math.cos(lat2 * p) * math.sin((lon2 - lon1) * p / 2) ** 2
    return EARTH_RADIUS_MI * 2 * math.asin(math.sqrt(a))


def applies(rule, position):
    between = rule.get("between")
    return between is None or between[0] <= position <= between[1]


def posted_mph(segment, position, defaults):
    for rule in segment["speed_limits"] or []:
        top = rule.get("max_speed") or {}
        if not rule.get("when") and applies(rule, position) and top.get("value"):
            return top["value"] * 0.621371 if top.get("unit") == "km/h" else top["value"]
    return defaults[segment["class"]]


def car_directions(segment, position, construction_log):
    """(forward allowed, backward allowed) for a car at this position along the segment."""
    under_construction = any("is_under_construction" in (f.get("values") or []) and applies(f, position)
                             for f in segment["road_flags"] or [])
    forward = backward = True
    for rule in segment["access_restrictions"] or []:
        when = rule.get("when") or {}
        if rule["access_type"] != "denied" or not applies(rule, position):
            continue
        if any(when.get(k) for k in ("during", "using", "recognized", "vehicle")):
            continue                      # time-of-day, purpose or vehicle-size rules: ignored
        if when.get("mode") and not CAR_MODES & set(when["mode"]):
            continue                      # applies to bikes, pedestrians or trucks only
        heading = when.get("heading")
        if heading == "backward":
            backward = False
        elif heading == "forward":
            forward = False
        elif under_construction:
            construction_log.add((segment["names"] or {}).get("primary") or segment["id"])
        else:
            forward = backward = False
    return forward, backward


def build_network(settings):
    defaults, factor = settings["default_speed_mph"], settings["traffic_factor"]
    drivable = {k for k in defaults if not k.startswith("_")}
    graph, position, local_street, construction = nx.DiGraph(), {}, set(), set()
    for seg in pq.read_table(HERE / "cache" / "segments.parquet").to_pylist():
        if seg["subtype"] != "road" or seg["class"] not in drivable or not seg["connectors"]:
            continue
        line = shapely.from_wkb(seg["geometry"])
        xy = list(line.coords)
        length = sum(haversine(*xy[i], *xy[i + 1]) for i in range(len(xy) - 1))
        if length == 0:
            continue
        connectors = sorted(seg["connectors"], key=lambda c: c["at"])
        for c in connectors:
            p = line.interpolate(c["at"], normalized=True)
            position[c["connector_id"]] = (p.x, p.y)
            if seg["class"] in CONNECT_CLASSES:
                local_street.add(c["connector_id"])
        for c0, c1 in zip(connectors, connectors[1:]):
            miles = (c1["at"] - c0["at"]) * length
            if miles <= 0:
                continue
            middle = (c0["at"] + c1["at"]) / 2
            minutes = miles / (posted_mph(seg, middle, defaults) * factor[seg["class"]]) * 60
            forward, backward = car_directions(seg, middle, construction)
            for u, v, allowed in ((c0["connector_id"], c1["connector_id"], forward),
                                  (c1["connector_id"], c0["connector_id"], backward)):
                if allowed and (not graph.has_edge(u, v) or graph[u][v]["minutes"] > minutes):
                    graph.add_edge(u, v, minutes=minutes, miles=miles)
    # Keep the part of the network where every node can reach every other.
    graph = graph.subgraph(max(nx.strongly_connected_components(graph), key=len)).copy()
    return graph, position, local_street & set(graph), sorted(construction)


def fastest_paths(graph, source, targets):
    """Dijkstra on minutes; returns {node: (minutes, miles)} for at least every target."""
    best, heap, done, left = {source: (0.0, 0.0)}, [(0.0, 0.0, source)], set(), set(targets)
    while heap and left:
        minutes, miles, u = heapq.heappop(heap)
        if u in done:
            continue
        done.add(u)
        left.discard(u)
        for v, edge in graph[u].items():
            t = minutes + edge["minutes"]
            if v not in best or t < best[v][0]:
                best[v] = (t, miles + edge["miles"])
                heapq.heappush(heap, (t, miles + edge["miles"], v))
    return best


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--traffic-scale", type=float, default=1.0,
                        help="multiply every traffic factor (0.8 = all travel 20%% slower)")
    parser.add_argument("--out", type=Path, default=OUT, help="output CSV (default: data/compiled/school_drive_matrix.csv)")
    args = parser.parse_args()
    settings = json.loads((HERE / "settings.json").read_text())
    settings["traffic_factor"] = {k: (v * args.traffic_scale if not k.startswith("_") else v)
                                  for k, v in settings["traffic_factor"].items()}
    out = args.out
    graph, position, local_street, construction = build_network(settings)
    schools = pd.read_csv(LOCATIONS)

    nodes = sorted(local_street)
    xy = np.array([position[n] for n in nodes])
    attach = {}
    for s in schools.itertuples():
        gap = np.hypot((xy[:, 0] - s.lon) * math.cos(math.radians(s.lat)), xy[:, 1] - s.lat) * 69.0
        attach[s.school] = (nodes[int(gap.argmin())], float(gap.min()))

    leg_mph = settings["access_leg_mph"]
    rows = []
    for a in schools.school:
        node_a, leg_a = attach[a]
        reached = fastest_paths(graph, node_a, {attach[b][0] for b in schools.school})
        for b in schools.school:
            if a == b:
                rows.append((a, b, 0.0, 0.0))
                continue
            node_b, leg_b = attach[b]
            minutes, miles = reached[node_b]
            legs = leg_a + leg_b
            rows.append((a, b, round(miles + legs, 3), round(minutes + legs / leg_mph * 60, 2)))
    pd.DataFrame(rows, columns=["from_school", "to_school", "road_miles", "drive_minutes"]).to_csv(out, index=False)

    meta = {"built": date.today().isoformat(), "overture_release": settings["overture_release"],
            "road_data": "OpenStreetMap contributors (ODbL), via Overture Maps Foundation",
            "network_nodes": graph.number_of_nodes(), "network_edges": graph.number_of_edges(),
            "construction_closures_ignored": construction,
            "attach_miles_max": round(max(v[1] for v in attach.values()), 3),
            "attach_miles_median": round(float(np.median([v[1] for v in attach.values()])), 3),
            "settings": settings}
    out.with_name(out.stem + "_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(f"Wrote {out}: {len(rows):,} routes on a network of {graph.number_of_nodes():,} nodes. "
          f"Construction closures ignored: {', '.join(construction) or 'none'}")


if __name__ == "__main__":
    main()
