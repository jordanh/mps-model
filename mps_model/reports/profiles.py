"""One profile per school proposed for closure in the Middle Ground and 3-closure plans: who the
students are, test-score trends, and where they would go.

Demographics and MCA scores come from secondary sources (SchoolDigger and allk12, which republish
Minnesota Department of Education data; exploremps.org for EL and special education shares). Check
them against the Minnesota Report Card (rc.education.mn.gov) before public use.
"""
import pandas as pd

from .. import paths
from ..schools import HIGH_SCHOOL, read_workbook

# Short names used in the workbook -> names used in data/compiled/school_profiles_public.csv
PROFILE_NAMES = {"HIA": "Hmong International Academy", "Olson": "Olson Middle", "Northeast": "Northeast Middle",
                 "Anwatin": "Anwatin Middle", "Franklin": "Franklin Middle", "Sanford": "Sanford Middle",
                 "Anthony": "Anthony Middle", "Justice Page": "Justice Page Middle", "Anishinabe": "Anishinabe Academy",
                 "Green": "Green Central", "FAIR": "FAIR School", "Heritage": "Heritage Academy",
                 "Longfellow": "Longfellow High", "Wellstone": "Wellstone International High"}
SCORE_YEARS = (2023, 2024, 2025, 2026)
SOURCES_NOTE = (
    "Sources: SY26 enrollment, building data and pathway from the district's Oct. 6, 2026 utilization workbook; "
    "demographics (NCES 2024-25) and MCA % proficient via SchoolDigger/allk12 (MDE data, approx.); EL and SpEd % "
    "from exploremps.org (older, approx.). Receiving schools and miles from the closure model.\n")


def _pct(value, suffix="%"):
    if pd.isna(value):
        return "n/a"
    return f"{value:.0f}{suffix}" if isinstance(value, float) else f"{value}{suffix}"


def _score_trend(profile, subject):
    """'14% (2025) -> 9% (2026)' and the change in points, or a reason there are no scores."""
    points = [(y, profile.get(f"{subject}_{y}")) for y in SCORE_YEARS]
    points = [(y, v) for y, v in points if not pd.isna(v)]
    if not points:
        grades = str(profile.get("grades", ""))
        reason = "not tested (grades below 3)" if grades.endswith(("K-1", "K-2")) else "not reported (too few tested students)"
        return reason, None
    trend = " -> ".join(f"{v:.0f}% ({y})" for y, v in points)
    change = points[-1][1] - points[0][1] if len(points) > 1 else None
    return trend, change


def closure_profiles(model, plans, reassignments, middle_ground_name):
    """Returns (profiles table, Markdown text)."""
    public = pd.read_csv(paths.SCHOOL_PROFILES).set_index("school")
    workbook = read_workbook().set_index("school")

    def profile(name):
        key = PROFILE_NAMES.get(name, name)
        return public.loc[key] if key in public.index else None

    profiled_plans = (middle_ground_name, "3-closure plan")
    schools = list(dict.fromkeys(s for plan in profiled_plans for s in plans[plan]))
    rows, md = [], ["# Profiles of schools proposed for closure\n", SOURCES_NOTE]
    for name in schools:
        p = profile(name)
        school = model.schools[name]
        in_plans = [k for k in profiled_plans if name in plans[k]]
        moves = reassignments[(reassignments.plan == in_plans[0]) & (reassignments.closed_school == name)]

        destinations = []
        for _, m in moves.iterrows():
            if model.schools[m.receiving_school].level == HIGH_SCHOOL:
                receiver_reading = "n/a (HS)"
            else:
                rp = profile(m.receiving_school)
                reading = float("nan") if rp is None else (rp.read_2026 if not pd.isna(rp.read_2026) else rp.read_2025)
                receiver_reading = _pct(reading)
            destinations.append(
                f"{m.receiving_school} ({int(m.students)} students, {m.road_miles_est:.1f} road mi, "
                f"{'same HS pathway' if m.keeps_hs_pathway else 'NEW pathway'}; receiver reading {receiver_reading})")
        if moves.receiving_school.nunique() == 1:
            together = "kept together in one building"
        elif school.grades in ("K-8", "PK-8"):
            together = "moves as K-5 and 6-8 cohorts"
        else:
            together = "split across receivers"

        reading_trend, reading_change = _score_trend(p, "read") if p is not None else ("n/a", None)
        math_trend, math_change = _score_trend(p, "math") if p is not None else ("n/a", None)
        w = workbook.loc[name]
        row = {
            "school": name, "in_plans": "; ".join(in_plans), "pathway": w.hs_pathway,
            "community": school.community, "grades": school.grades,
            "sy26_enrolled": int(w.enrollment), "design_capacity": w.modeled_design_range,
            "building_sqft": w.sqft, "year_built": w.year_built,
            "pct_students_of_color": None if p is None else p.pct_poc,
            "largest_groups": None if p is None else p.largest_groups,
            "pct_frl": None if p is None else p.pct_frl, "pct_el": None if p is None else p.pct_el,
            "pct_sped": None if p is None else p.pct_sped,
            "reading_trend": reading_trend, "reading_change_pts": reading_change,
            "math_trend": math_trend, "math_change_pts": math_change,
            "program": None if p is None else p.program,
            "students_go_to": " | ".join(destinations), "student_body": together,
            "closed_in_district_options": ", ".join(f"Option {k}" for k in (1, 2, 3)
                                                    if not pd.notna(w[f"option{k}_enrollment"])),
        }
        rows.append(row)

        building = (f" in a building designed for {row['design_capacity']}" if isinstance(row["design_capacity"], str) else "")
        building += (f" ({row['building_sqft']:,.0f} sq ft, built {row['year_built']})"
                     if pd.notna(row["building_sqft"]) else " (shared/leased site)")
        md += [f"## {name}  ({row['grades']}, {row['pathway']} pathway, {row['community']})",
               f"- In: {row['in_plans']}. Also closed in district: {row['closed_in_district_options'] or 'none'}",
               f"- SY26 enrollment {row['sy26_enrolled']}" + building,
               f"- Students: {_pct(row['pct_students_of_color'])} students of color ({row['largest_groups']}); "
               f"{_pct(row['pct_frl'])} free/reduced lunch; EL {_pct(row['pct_el'])}; SpEd {_pct(row['pct_sped'])}",
               f"- Reading proficient: {reading_trend}" + (f" (change {reading_change:+.0f} pts)" if reading_change is not None else ""),
               f"- Math proficient: {math_trend}" + (f" (change {math_change:+.0f} pts)" if math_change is not None else ""),
               f"- Program: {row['program']}",
               f"- Students go to: {row['students_go_to']} ({together})", ""]
    return pd.DataFrame(rows), "\n".join(md)
