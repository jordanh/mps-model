"""The named plans and the closure-only comparison tables.

  Middle Ground   5 closures (policy.middle_ground_closures, locked Oct. 10, 2026). Without the lock,
                  the fewest closures whose net savings are within 5% of the best closure set's
                  (policy.optimum_tolerance_share, with a $0.1M floor)
  Family Trust    the best 2-closure set (in practice two high school program merges)
  3-closure plan  a reference variant
  District Options 1-3  the district's own proposals (Footprint-First), evaluated with the same model

Plan names in the output files keep the labels used in the published plan ("Optimum plan (N closures)"
is the Middle Ground plan).
"""
import math

import pandas as pd

FAMILY_TRUST_N = 2
THREE_CLOSURE_N = 3

SENSITIVITY_CASES = [  # (label, multiplier on attrition assumptions, multiplier on busing cost per mile)
    ("Low attrition & bussing (x0.5)", 0.5, 0.5),
    ("Central", 1.0, 1.0),
    ("High attrition & bussing (x1.5)", 1.5, 1.5),
]
ATTRITION_KEYS_VARIED = ["direct_base", "direct_growth_per_closure", "spillover_scale"]


def optimum_tolerance(peak, assumptions):
    """How far below the peak a smaller plan may be and still count as the optimum: the larger of a
    fixed amount (policy.optimum_tolerance) and a share of the peak (policy.optimum_tolerance_share)."""
    return max(assumptions.get("policy", "optimum_tolerance", 0),
               assumptions.get("policy", "optimum_tolerance_share", 0) * peak)


def optimum_size(curve, assumptions):
    """The Middle Ground's number of closures: policy.middle_ground_closures when set (locked at 5 on
    Oct. 10, 2026), otherwise the fewest closures whose net savings are within the tolerance of the
    best, up to max_closures. Net savings are nearly flat around the peak, so the rule picks the least
    disruptive plan on that plateau."""
    locked = assumptions.get("policy", "middle_ground_closures")
    if locked is not None:
        return int(locked)
    max_closures = assumptions.get("policy", "max_closures")
    in_range = {n: r.net_savings for n, r in curve.items() if n <= max_closures}
    peak = max(in_range.values())
    tolerance = optimum_tolerance(peak, assumptions)
    return min(n for n, v in in_range.items() if v >= peak - tolerance)


def middle_ground_name(n_optimum):
    return f"Optimum plan ({n_optimum} closures)"


def named_plans(model, curve):
    """{plan name: closed schools} for the closure comparison (Family Trust is added by levers.py)."""
    n_opt = optimum_size(curve, model.assumptions)
    return n_opt, {
        middle_ground_name(n_opt): curve[n_opt].closed,
        "3-closure plan": curve[THREE_CLOSURE_N].closed,
        "District Option 1": model.district_options[1],
        "District Option 2": model.district_options[2],
        "District Option 3": model.district_options[3],
    }


def plan_comparison_table(model, plans):
    """One row per plan: savings, costs, net, and students to recruit if net revenue alone closed the gap."""
    a = model.assumptions
    gap = a.get("budget", "structural_gap")
    rows, details = [], {}
    for name, closed in plans.items():
        r = model.evaluate(closed, detail=True)
        details[name] = r
        remaining_gap = gap - r.net_savings
        rows.append({
            "plan": name, "schools_closed": len(closed), "closed": "; ".join(closed),
            "students_moved": round(r.students_moved),
            "gross_closure_savings": round(r.gross_closure_savings),
            "specialist_sharing_savings": round(r.sharing_savings),
            "gross_savings": round(r.gross_savings),
            "bus_cost": round(r.bus_cost),
            "lost_family_cost": round(r.lost_family_cost),
            "one_time_amortized": round(r.one_time_amortized),
            "total_costs": round(r.total_costs),
            "net_savings": round(r.net_savings),
            "students_lost": round(r.students_lost),
            "budget_gap": round(gap),
            "remaining_gap": round(remaining_gap),
            "new_students_to_recruit": max(0, math.ceil(remaining_gap / a.net_revenue_per_student)),
            "sharing_pairs": len(r.pairs),
        })
    return pd.DataFrame(rows), details


def reassignment_rows(plan_name, result):
    return [{"plan": plan_name, "closed_school": m.from_school, "receiving_school": m.to_school,
             "students": round(m.students), "road_miles": round(m.road_miles, 2),
             "drive_minutes": round(m.drive_minutes, 1), "keeps_hs_pathway": m.keeps_pathway,
             "student_body_split": m.body_split}
            for m in result.moves]


def sharing_pair_rows(plan_name, result):
    return [dict(p, plan=plan_name) for p in result.pairs]


def sensitivity_table(model, curve, plans):
    """Net savings with attrition and busing assumptions scaled down and up, same closure sets."""
    a = model.assumptions
    rows = []
    for label, attrition_factor, busing_factor in SENSITIVITY_CASES:
        changes = {("attrition", k): a.get("attrition", k) * attrition_factor for k in ATTRITION_KEYS_VARIED}
        changes[("transport", "cost_per_rider_mile")] = a.get("transport", "cost_per_rider_mile") * busing_factor
        varied = model.with_assumptions(a.with_values(changes))
        net_by_n = {n: varied.evaluate(curve[n].closed).net_savings for n in range(0, a.get("policy", "max_closures") + 1)}
        n_best = max(net_by_n, key=net_by_n.get)
        row = {"scenario": label, "optimum_N_on_curve": n_best, "optimum_net": round(net_by_n[n_best])}
        for name, closed in plans.items():
            row[name] = round(varied.evaluate(closed).net_savings)
        rows.append(row)
    return pd.DataFrame(rows)
