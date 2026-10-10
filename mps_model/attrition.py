"""Families who leave MPS because of closures.

Two effects, both growing faster than the number of closures N:

  direct     students at a closed school who leave the district. Each move's leave rate is
                 base + growth_per_closure x (N - 1)^exponent       (more closures, less trust)
               + per_extra_mile x miles moved (road miles / circuity: the coefficient was set
                                                per straight-line mile)
               + split_body_penalty     if classmates are split across buildings
               + pathway_break_penalty  if students lose their high school pathway
             capped at direct_cap. High school programs move intact, so their rate is halved.
             Base rate: about 6% of displaced students left Chicago Public Schools after its 2013
             closures (UChicago Consortium), plus 2 points for Minneapolis's charter market.

  spillover  students at schools that stay open who leave because they lose confidence in the
             district: remaining students x spillover_scale x N^spillover_exponent.
"""
from .schools import HS_PROGRAM

HS_PROGRAM_RATE_FACTOR = 0.5


def families_lost(moves, closed, schools, assumptions):
    """Returns (students lost from closed schools, students lost from schools that stay open)."""
    get = lambda key: assumptions.get("attrition", key)
    n_closed = len(closed)
    base_rate = get("direct_base") + get("direct_growth_per_closure") * max(0, n_closed - 1) ** get("direct_growth_exponent")

    direct = 0.0
    for m in moves:
        rate = base_rate + get("direct_per_extra_mile") * m.effective_miles
        if m.body_split:
            rate += get("split_body_penalty")
        if not m.keeps_pathway:
            rate += get("pathway_break_penalty")
        if schools[m.from_school].level == HS_PROGRAM:
            rate *= HS_PROGRAM_RATE_FACTOR
        direct += m.students * min(get("direct_cap"), rate)

    students_still_in_open_schools = schools.total_enrollment - sum(schools[c].enrollment for c in closed)
    spillover = students_still_in_open_schools * get("spillover_scale") * n_closed ** get("spillover_exponent")
    return direct, spillover
