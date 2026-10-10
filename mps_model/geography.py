"""Distances between schools.

School positions are pixel coordinates on the district's current high school pathway map
(data/district/current_hs_pathways_map.png). We converted pixels to miles by fitting the map to the
Minneapolis street grid: 122 pixels per mile, median error about 0.15 miles. Distances are straight
lines; models that need road distance multiply by transport.circuity (about 1.35).
"""
import numpy as np

PIXELS_PER_MILE = 122.0


class Distances:
    def __init__(self, schools):
        self._index = {name: i for i, name in enumerate(schools.names)}
        xy = np.array([[schools[n].map_x, schools[n].map_y] for n in schools.names], dtype=float)
        dx = xy[:, None, 0] - xy[None, :, 0]
        dy = xy[:, None, 1] - xy[None, :, 1]
        self._miles = np.hypot(dx, dy) / PIXELS_PER_MILE

    def miles(self, a, b):
        """Straight-line miles between two schools."""
        return float(self._miles[self._index[a], self._index[b]])
