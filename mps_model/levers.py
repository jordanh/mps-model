"""Three levers, three plans: how each plan closes the structural gap with closures, specialist
sharing and recruitment.

For each plan:
  1. the closure model gives net savings from closures and sharing, and the families lost;
  2. the gap left over must come from recruitment: solve for the recruits needed, given how full the
     buildings left open are (recruits are worth less as buildings fill) and how much trust the
     closures cost (recruiting gets more expensive);
  3. report the campaign cost, the gap left if recruiting falls short, and how many years and how much
     bridge funding it takes at the evidence-based and stretch recruiting paces.

The Footprint-First plans (district Options 1-3) are scored with the district's own recruitment
assumption (roughly flat enrollment), and also with the recruits they would need to balance.
"""
import math

import pandas as pd

from .plans import FAMILY_TRUST_N, THREE_CLOSURE_N
from .recruitment import Recruitment
from .schools import HS_PROGRAM

FULL_CAMPAIGN, DISTRICT_BASELINE = "full", "district"
FIRST_SCHOOL_YEAR = 2027   # the first year recruiting and bridge funding apply (2027-28)


def lever_plans(curve, middle_ground, district_options):
    """(name, closed schools, recruitment intent) for every plan in the lever comparison."""
    return [
        ("Family Trust plan", curve[FAMILY_TRUST_N].closed, FULL_CAMPAIGN),
        ("Middle Ground plan", middle_ground, FULL_CAMPAIGN),
        ("Footprint-First plan (District Option 1)", district_options[1], DISTRICT_BASELINE),
        ("Footprint-First plan (District Option 2)", district_options[2], DISTRICT_BASELINE),
        ("Footprint-First plan (District Option 3)", district_options[3], DISTRICT_BASELINE),
        ("Variant: zero closures (sharing only)", [], FULL_CAMPAIGN),
        ("Variant: 3 closures", curve[THREE_CLOSURE_N].closed, FULL_CAMPAIGN),
    ]


def enrollment_and_capacity_after(model, closed, students_lost):
    """District enrollment after families leave, and the design capacity of the buildings left open."""
    open_capacity = sum(s.design_capacity for s in model.schools if s.name not in closed)
    return model.schools.total_enrollment - students_lost, open_capacity


def recruiting_position(model, recruitment, closed, result=None):
    """Where a plan leaves recruiting: (closure result, spillover share, enrollment, capacity,
    recruits needed, whether recruiting can balance the budget)."""
    gap = model.assumptions.get("budget", "structural_gap")
    r = result or model.evaluate(closed)
    spillover_share = r.families_lost_spillover / model.schools.total_enrollment
    enrollment, capacity = enrollment_and_capacity_after(model, closed, r.students_lost)
    need, balances = recruitment.recruits_needed(gap - r.net_savings, spillover_share, enrollment, capacity)
    return r, spillover_share, enrollment, capacity, need, balances


def plan_lever_row(model, recruitment, name, closed, intent):
    gap = model.assumptions.get("budget", "structural_gap")
    r, spillover_share, enrollment, capacity, need, balances = recruiting_position(model, recruitment, closed)
    avg_cost_at_need, trust = recruitment.cost_per_recruit(need, spillover_share)
    planned = need if intent == FULL_CAMPAIGN else recruitment.get("district_baseline_recruits")
    cost_per_planned, _ = recruitment.cost_per_recruit(planned, spillover_share)
    campaign_cost = planned * cost_per_planned
    amortized_campaign = campaign_cost / recruitment.get("amortization_years")
    recruitment_net = recruitment.total_value(planned, enrollment, capacity) - amortized_campaign
    gap_left = gap - r.net_savings - recruitment_net
    shortfall_recruits = planned * recruitment.get("underdelivery_test")
    gap_if_short = gap - r.net_savings - (recruitment.total_value(shortfall_recruits, enrollment, capacity) - amortized_campaign)
    value_at_need = recruitment.total_value(need, enrollment, capacity)

    pace = {}
    for tag in ("evidence", "stretch"):
        per_year = recruitment.recruits_per_year(tag, spillover_share)
        if not balances:
            years = math.nan
        else:
            years = need / per_year if need > 0 else 0.0
        bridge = sum(recruitment.yearly_shortfalls(need, per_year, enrollment, capacity))
        pace[tag] = (round(per_year), round(years, 1), round(bridge) if balances else math.nan)

    base_enrollment = recruitment.get("base_enrollment")
    return {
        "plan": name, "schools_closed": len(closed),
        "neighborhood_or_magnet_buildings_closed": sum(1 for c in closed if model.schools[c].level != HS_PROGRAM),
        "closed": "; ".join(closed), "students_moved": round(r.students_moved),
        "families_lost": round(r.students_lost), "families_lost_spillover": round(r.families_lost_spillover),
        "sharing_savings": round(r.sharing_savings), "closure_net_savings": round(r.net_savings - r.sharing_savings),
        "net_savings_closures_and_sharing": round(r.net_savings),
        "recruits_needed_to_balance": math.ceil(need) if balances else None, "recruitment_can_balance": balances,
        "best_attainable_recruits": math.ceil(need), "recruits_planned": math.ceil(planned),
        "students_after_departures": round(enrollment), "design_capacity_open_buildings": round(capacity),
        "utilization_before_recruiting": round(enrollment / capacity, 3),
        "utilization_after_recruiting": round((enrollment + need) / capacity, 3),
        "recruits_before_80pct": max(0, math.floor(0.8 * capacity - enrollment)),
        "recruits_before_90pct": max(0, math.floor(0.9 * capacity - enrollment)),
        "recruit_value_avg": round(value_at_need / need) if need else None,
        "recruitment_growth_pct": round(planned / base_enrollment * 100, 1),
        "share_of_outside_pool_pct": round(planned / recruitment.get("resident_pool") * 100, 1),
        "cost_per_recruit": round(cost_per_planned if planned else avg_cost_at_need),
        "trust_cost_multiplier": round(trust, 2),
        "recruitment_campaign_cost_total": round(campaign_cost),
        "recruitment_net_annual": round(recruitment_net),
        "gap_left_if_recruitment_as_planned": round(gap_left),
        "gap_left_if_recruitment_hits_60pct": round(gap_if_short),
        "recruits_per_year_evidence_pace": pace["evidence"][0], "years_to_balance_evidence_pace": pace["evidence"][1],
        "bridge_funding_evidence_pace": pace["evidence"][2],
        "recruits_per_year_stretch_pace": pace["stretch"][0], "years_to_balance_stretch_pace": pace["stretch"][1],
        "bridge_funding_stretch_pace": pace["stretch"][2],
    }


def three_plans_table(model, curve, middle_ground):
    recruitment = Recruitment(model.assumptions)
    rows = [plan_lever_row(model, recruitment, name, closed, intent)
            for name, closed, intent in lever_plans(curve, middle_ground, model.district_options)]
    return pd.DataFrame(rows)


def tradeoff_table(model, curve, max_n):
    """For each number of closures: net savings, families lost and recruits needed to balance."""
    recruitment = Recruitment(model.assumptions)
    rows = []
    for n in range(0, max_n + 1):
        r, spillover_share, enrollment, capacity, need, balances = recruiting_position(
            model, recruitment, curve[n].closed, result=curve[n])
        avg_cost, _ = recruitment.cost_per_recruit(need, spillover_share)
        rows.append({"N": n, "net_savings": round(r.net_savings), "students_moved": round(r.students_moved),
                     "families_lost": round(r.students_lost), "recruits_needed": math.ceil(need) if balances else None,
                     "can_balance": balances, "utilization_before_recruiting": round(enrollment / capacity, 3),
                     "cost_per_recruit": round(avg_cost), "campaign_cost": round(need * avg_cost)})
    return pd.DataFrame(rows)


def glide_path_table(model, curve, middle_ground):
    """Shortfall bridge funding must cover in each school year, at the evidence-based pace, for the
    Family Trust and Middle Ground plans. Years run until the slower plan balances."""
    recruitment = Recruitment(model.assumptions)
    schedules, years_to_balance = {}, []
    for label, closed in [("Family Trust", curve[FAMILY_TRUST_N].closed), ("Middle Ground", middle_ground)]:
        _, spillover_share, enrollment, capacity, need, _ = recruiting_position(model, recruitment, closed)
        per_year = recruitment.recruits_per_year("evidence", spillover_share)
        schedules[label] = recruitment.yearly_shortfalls(need, per_year, enrollment, capacity)
        years_to_balance.append(round(need / per_year, 1))
    n_years = math.ceil(max(years_to_balance))
    school_years = [f"{FIRST_SCHOOL_YEAR + i}-{(FIRST_SCHOOL_YEAR + 1 + i) % 100:02d}" for i in range(n_years)]
    rows = []
    for label, shortfalls in schedules.items():
        padded = shortfalls + [0.0] * (n_years - len(shortfalls))
        rows += [{"plan": label, "school_year": y, "shortfall_m": round(v / 1e6, 1)} for y, v in zip(school_years, padded)]
    return pd.DataFrame(rows)
