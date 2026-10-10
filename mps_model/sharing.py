"""Specialist sharing: two small schools near each other split one team of specialists (art, music,
PE), each getting them half-days, instead of each paying for its own three-specialist floor.

For every pair of small open elementary or K-8 schools:
  * skip if their combined enrollment is too large for one team, or the midday drive is too long
    (routed driving minutes, averaged over both directions, plus a fixed time to park and set up);
  * specialist FTE recovered = min(FTE saved per pair, two floors - FTE the combined enrollment needs);
  * saving = recovered FTE x teacher cost
             - teaching time lost to the drive - mileage - coordination cost.
Then pick the set of pairs (each school in at most one pair) with the largest total saving: a
maximum-weight matching on the graph of feasible pairs.
"""
import itertools

import networkx as nx

SMALL_SCHOOL_MAX = 450   # only schools under this enrollment are considered for sharing


def best_sharing_pairs(enrollment, closed, schools, distances, assumptions):
    """Returns (total annual saving, list of pair records in workbook order)."""
    get = lambda key: assumptions.get("sharing", key)
    teacher = assumptions.get("staff_cost", "teacher_loaded")
    specialist_rule = assumptions.raw["staff_floors"]["elementary"]["specialist"]
    floor, students_per_specialist = specialist_rule["floor"], specialist_rule["per"]
    fte_per_pair = get("fte_saved_per_pair")

    eligible = [n for n in schools.names
                if n not in closed and schools[n].level in assumptions.raw["sharing"]["levels"]
                and 0 < enrollment[n] < SMALL_SCHOOL_MAX]
    graph = nx.Graph()
    for a, b in itertools.combinations(eligible, 2):
        if enrollment[a] + enrollment[b] > get("max_combined_enrollment"):
            continue
        road_miles, drive_minutes = distances.both_ways(a, b)
        minutes = drive_minutes + get("fixed_transfer_minutes")
        if minutes > get("max_travel_minutes"):
            continue
        lost_teaching_time = fte_per_pair * minutes / get("workday_minutes") * teacher
        mileage = fte_per_pair * road_miles * get("mileage_rate") * get("school_days")
        # A shared team still needs enough specialists for both schools' students together.
        fte_needed = enrollment[a] / students_per_specialist + enrollment[b] / students_per_specialist
        recovered = min(fte_per_pair, max(0.0, 2 * floor - max(floor, fte_needed)))
        saving = recovered * teacher - lost_teaching_time - mileage - get("coordination_cost_per_pair")
        if saving > 0:
            graph.add_edge(a, b, weight=saving, minutes=minutes, road=road_miles)

    position = {n: i for i, n in enumerate(schools.names)}
    matched = sorted((tuple(sorted(pair, key=position.get)) for pair in nx.max_weight_matching(graph)),
                     key=lambda pair: position[pair[0]])
    pairs = []
    for a, b in matched:
        edge = graph[a][b]
        pairs.append({"school_a": a, "school_b": b, "enr_a": round(enrollment[a]), "enr_b": round(enrollment[b]),
                      "road_miles": round(edge["road"], 2), "travel_minutes": round(edge["minutes"], 1),
                      "net_saving": round(edge["weight"])})
    return sum(p["net_saving"] for p in pairs), pairs
