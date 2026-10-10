"""Runs the whole analysis and writes every table to a results folder.

Order of work:
  1. search      best closure set for each N (search.py), or re-evaluate the sets in a saved curve
  2. plans       pick the Middle Ground optimum; compare it with the 3-closure variant and the
                 district's Options 1-3; sensitivity to attrition and busing assumptions (plans.py)
  3. levers      add recruitment: the three-plan comparison, the trade-off by N and the glide path
                 (levers.py)
  4. reports     school-by-school capacity and class size; profiles of schools proposed for closure
  5. figures     charts and maps drawn from the tables (figures/)
"""
import json
from pathlib import Path

import pandas as pd

from .assumptions import Assumptions
from .closure_model import ClosureModel
from .levers import glide_path_table, three_plans_table, tradeoff_table
from .paths import ResultsDir
from .plans import (FAMILY_TRUST_N, named_plans, plan_comparison_table, reassignment_rows, sensitivity_table,
                    sharing_pair_rows)
from .reports.capacity import capacity_tables
from .reports.profiles import closure_profiles
from .search import best_closure_sets

NO_GROWTH_PROTECTION = 99   # a growth threshold no community reaches: every school can close


def load_curve(model, path):
    """Re-evaluate the closure sets in a saved net_savings_by_closures.csv instead of searching again."""
    saved = pd.read_csv(path)
    curve = {}
    for row in saved.itertuples(index=False):
        closed = [] if pd.isna(row.closed) or row.closed == "" else row.closed.split("; ")
        curve[int(row.N)] = model.evaluate(closed)
    return curve


def closure_curve(model, results, reuse_curve=None, max_n=None, log=print):
    max_n = max_n or model.assumptions.get("policy", "extended_curve_max")
    log(f"Closure candidates ({len(model.candidates)}): {model.candidates}")
    if reuse_curve:
        log(f"Re-evaluating the closure sets in {reuse_curve}")
        curve = load_curve(model, reuse_curve)
    else:
        log(f"Searching for the best closure set for N = 1..{max_n}")
        curve = best_closure_sets(model, max_n, log=log)
    pd.DataFrame([r.summary_row() for r in curve.values()]).to_csv(results.table("net_savings_by_closures.csv"), index=False)
    return curve


def run_unconstrained_curve(assumptions, results_root, max_n=None, log=print):
    """The closure curve if growth areas were NOT protected (the dashed line in figure 1)."""
    unprotected = assumptions.with_values({("policy", "growth_protect_threshold"): NO_GROWTH_PROTECTION})
    results = ResultsDir(Path(results_root) / "unconstrained").create()
    return closure_curve(ClosureModel(unprotected), results, max_n=max_n, log=lambda *_: None)


def run(results_root, reuse_curve=None, max_n=None, unconstrained=True, figures=True, deck_images=False,
        assumptions_path=None, log=print):
    assumptions = Assumptions.load(assumptions_path) if assumptions_path else Assumptions.load()
    results = ResultsDir(results_root).create()
    model = ClosureModel(assumptions)
    circuity = assumptions.get("transport", "circuity")

    # 1. search
    curve = closure_curve(model, results, reuse_curve, max_n, log)

    # 2. plans
    n_optimum, plans = named_plans(model, curve)
    middle_ground_name = next(iter(plans))
    middle_ground = plans[middle_ground_name]
    comparison, details = plan_comparison_table(model, plans)
    comparison.to_csv(results.table("plan_comparison.csv"), index=False)
    sensitivity = sensitivity_table(model, curve, plans)
    sensitivity.to_csv(results.table("sensitivity.csv"), index=False)

    # Family Trust joins the plan list (it is the best 2-closure set)
    family_trust = curve[FAMILY_TRUST_N].closed
    plans["Family Trust plan"] = family_trust
    details["Family Trust plan"] = model.evaluate(family_trust, detail=True)
    reassignments = pd.DataFrame([row for name, r in details.items() for row in reassignment_rows(name, r, circuity)])
    reassignments.to_csv(results.table("plan_reassignments.csv"), index=False)
    pd.DataFrame([row for name, r in details.items() for row in sharing_pair_rows(name, r)]).to_csv(
        results.table("plan_specialist_pairs.csv"), index=False)
    with open(results.table("plans.json"), "w") as f:
        json.dump({"optimum_N": n_optimum, "plans": plans, "candidates": model.candidates,
                   "protected": model.protected}, f, indent=2)

    # 3. levers
    levers = three_plans_table(model, curve, middle_ground)
    levers.to_csv(results.table("three_plans_levers.csv"), index=False)
    max_closures = assumptions.get("policy", "max_closures")
    tradeoff_table(model, curve, max_closures).to_csv(results.table("lever_tradeoff_by_closures.csv"), index=False)
    glide_path_table(model, curve, middle_ground).to_csv(results.table("glide_path.csv"), index=False)

    # 4. reports
    labels = {"Family Trust plan": "Family Trust", middle_ground_name: "Middle Ground"}
    labelled = [(labels.get(name, name), closed) for name, closed in plans.items() if name != "3-closure plan"]
    by_school, summary = capacity_tables(model, labelled)
    by_school.to_csv(results.table("capacity_class_size_impacts.csv"), index=False)
    summary.to_csv(results.table("capacity_summary.csv"), index=False)
    profiles, profiles_md = closure_profiles(model, plans, reassignments, middle_ground_name)
    profiles.to_csv(results.table("closure_school_profiles.csv"), index=False)
    results.table("closure_school_profiles.md").write_text(profiles_md)

    pd.set_option("display.width", 250)
    log(comparison.drop(columns=["closed"]).to_string())
    log(levers.drop(columns=["closed"]).set_index("plan").T.to_string())

    if unconstrained:
        log("Searching again with growth areas unprotected (for figure 1)")
        run_unconstrained_curve(assumptions, results_root, max_n, log)

    # 5. figures
    if figures:
        from .figures import draw_all
        draw_all(results, assumptions, deck_images=deck_images, log=log)
    log(f"Results written to {results.root}")
    return results
