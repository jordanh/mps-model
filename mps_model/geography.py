"""Distances and driving times between schools.

Two sources, chosen by `transport.distance_source` in assumptions.json:

  "routed" (default)  Road miles and driving minutes along the fastest route on the street network,
                      read from data/compiled/school_drive_matrix.csv. tools/routing/ builds that
                      table from OpenStreetMap roads (Overture Maps release 2026-09-23.1): one-way
                      streets and closed roads respected, posted speed limits slowed for signals and
                      school-hour traffic. School locations are geocoded street addresses
                      (data/compiled/school_locations.csv). A trip can take a different time in each
                      direction because of one-way streets.
  "straight_line"     The earlier method: straight lines between positions on the district's pathway
                      map (122 pixels per mile), times `transport.circuity` for road miles and
                      `sharing.avg_speed_mph` for minutes. Kept so earlier results can be reproduced.

Two coefficients were set per straight-line mile (the extra leave rate per mile moved, and how fast
the walking share falls). `effective_miles` puts a routed trip on that scale (road miles / circuity),
so switching to routing changes the distances, not the calibration.
"""
import numpy as np
import pandas as pd

from . import paths

PIXELS_PER_MILE = 122.0
ROUTED, STRAIGHT_LINE = "routed", "straight_line"


class Distances:
    def __init__(self, schools, assumptions, matrix_path=None):
        self.source = assumptions.get("transport", "distance_source", ROUTED)
        self.circuity = assumptions.get("transport", "circuity")
        self._index = {name: i for i, name in enumerate(schools.names)}
        xy = np.array([[schools[n].map_x, schools[n].map_y] for n in schools.names], dtype=float)
        dx = xy[:, None, 0] - xy[None, :, 0]
        dy = xy[:, None, 1] - xy[None, :, 1]
        self._map_miles = np.hypot(dx, dy) / PIXELS_PER_MILE
        if self.source == ROUTED:
            self._road, self._minutes = self._read_matrix(schools.names, matrix_path or paths.DRIVE_MATRIX)
        elif self.source == STRAIGHT_LINE:
            self._road = self._map_miles * self.circuity
            self._minutes = self._road / assumptions.get("sharing", "avg_speed_mph") * 60
        else:
            raise ValueError(f"transport.distance_source must be {ROUTED!r} or {STRAIGHT_LINE!r}, not {self.source!r}")

    def _read_matrix(self, names, path):
        table = pd.read_csv(path)
        missing = sorted(set(names) - set(table.from_school))
        if missing:
            raise ValueError(f"{path.name} has no routes from {', '.join(missing)}; rebuild it with tools/routing/")
        road, minutes = np.zeros((len(names), len(names))), np.zeros((len(names), len(names)))
        for r in table.itertuples(index=False):
            if r.from_school in self._index and r.to_school in self._index:
                i, j = self._index[r.from_school], self._index[r.to_school]
                road[i, j], minutes[i, j] = r.road_miles, r.drive_minutes
        return road, minutes

    def road_miles(self, a, b):
        """Road miles from school a to school b."""
        return float(self._road[self._index[a], self._index[b]])

    def drive_minutes(self, a, b):
        """Driving minutes from school a to school b."""
        return float(self._minutes[self._index[a], self._index[b]])

    def both_ways(self, a, b):
        """(road miles, driving minutes), averaged over the two directions, for a trip made both ways."""
        i, j = self._index[a], self._index[b]
        return float((self._road[i, j] + self._road[j, i]) / 2), float((self._minutes[i, j] + self._minutes[j, i]) / 2)

    def effective_miles(self, a, b):
        """Road miles / circuity: a routed trip on the straight-line scale that some coefficients use.
        Under the straight_line source this is the straight-line distance."""
        return self.road_miles(a, b) / self.circuity

    def map_miles(self, a, b):
        """Straight-line miles between the two schools' positions on the pathway map."""
        return float(self._map_miles[self._index[a], self._index[b]])
