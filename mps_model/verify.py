"""Compare a results folder with reference_outputs/, table by table.

Numbers must agree to within one part in a billion (a run on another machine can differ in the last
digit of a float). Tables whose row order carries no meaning (specialist pairs) are compared as sets.
"""
import json
from pathlib import Path

import pandas as pd

from .paths import REFERENCE_OUTPUTS_DIR

TABLES = [
    "plans.json",
    "plan_comparison.csv",
    "three_plans_levers.csv",
    "net_savings_by_closures.csv",
    "sensitivity.csv",
    "lever_tradeoff_by_closures.csv",
    "plan_reassignments.csv",
    "plan_specialist_pairs.csv",
    "glide_path.csv",
    "capacity_class_size_impacts.csv",
    "capacity_summary.csv",
    "closure_school_profiles.csv",
]
UNORDERED = {"plan_specialist_pairs.csv"}
RELATIVE_TOLERANCE = 1e-9


def _normalize_pairs(df):
    """Each pair as (plan, sorted schools), so row order and which school is 'a' do not matter."""
    rows = []
    for r in df.itertuples(index=False):
        (s1, e1), (s2, e2) = sorted([(r.school_a, r.enr_a), (r.school_b, r.enr_b)])
        rows.append((r.plan, s1, s2, e1, e2, r.road_miles, r.travel_minutes, r.net_saving))
    return sorted(rows)


def compare_table(name, results_dir, reference_dir=REFERENCE_OUTPUTS_DIR):
    """Returns a list of differences (empty when the tables match)."""
    ours, ref = Path(results_dir) / name, Path(reference_dir) / name
    if not ours.exists():
        return [f"{name}: missing from results"]
    if name.endswith(".json"):
        return [] if json.loads(ours.read_text()) == json.loads(ref.read_text()) else [f"{name}: contents differ"]
    a, b = pd.read_csv(ours), pd.read_csv(ref)
    if list(a.columns) != list(b.columns):
        return [f"{name}: columns differ"]
    if len(a) != len(b):
        return [f"{name}: {len(a)} rows vs {len(b)} in the reference"]
    if name in UNORDERED:
        return [] if _normalize_pairs(a) == _normalize_pairs(b) else [f"{name}: pairs differ"]
    problems = []
    for col in a.columns:
        x, y = a[col], b[col]
        numeric = all(pd.api.types.is_numeric_dtype(c) and not pd.api.types.is_bool_dtype(c) for c in (x, y))
        if numeric:
            both_missing = x.isna() & y.isna()
            close = (x - y).abs() <= RELATIVE_TOLERANCE * y.abs().clip(lower=1)
            bad = ~(both_missing | close)
        else:
            bad = ~((x.isna() & y.isna()) | (x.astype(str) == y.astype(str)))
        for i in bad[bad].index[:3]:
            problems.append(f"{name}: row {i}, {col}: {x[i]!r} vs reference {y[i]!r}")
    return problems


def verify(results_dir, reference_dir=REFERENCE_OUTPUTS_DIR, log=print):
    all_problems = []
    for name in TABLES:
        problems = compare_table(name, results_dir, reference_dir)
        log(f"  {'OK  ' if not problems else 'DIFF'} {name}")
        for p in problems:
            log(f"       {p}")
        all_problems += problems
    return not all_problems
