"""Loads config/assumptions.json, the single place where every number the model assumes is set.

Most entries look like {"value": ..., "src": "where the number comes from"}. Read them with
`assumptions.get("section", "key")`. A few entries (staff_floors, sharing.levels,
policy.protect_new_builds) are plain structures without a "value" wrapper; read those through
`assumptions.raw`.
"""
import copy
import json

from .paths import ASSUMPTIONS_FILE


class Assumptions:
    def __init__(self, raw):
        self.raw = raw

    @classmethod
    def load(cls, path=ASSUMPTIONS_FILE):
        with open(path) as f:
            return cls(json.load(f))

    def get(self, section, key, default=None):
        """The value of one assumption. Returns `default` if the entry does not exist."""
        entry = self.raw[section].get(key)
        if entry is None:
            return default
        return entry["value"] if isinstance(entry, dict) and "value" in entry else entry

    def recruitment_capacity(self, key):
        """Values under recruitment.capacity_response (how a recruit's value falls as buildings fill)."""
        return self.raw["recruitment"]["capacity_response"][key]["value"]

    def with_values(self, changes):
        """A copy with some values replaced: changes = {("section", "key"): new_value}."""
        raw = copy.deepcopy(self.raw)
        for (section, key), value in changes.items():
            raw[section][key]["value"] = value
        return Assumptions(raw)

    # --- derived quantities used in several places -------------------------------------------

    @property
    def net_revenue_per_student(self):
        """What the district keeps from one more (or loses from one fewer) student each year:
        state and local revenue per pupil minus the share of cost that follows the student."""
        return self.get("budget", "revenue_per_pupil") * (1 - self.get("budget", "variable_cost_share"))
