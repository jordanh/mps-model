"""How full each affected building gets, and its average class size, before and after each plan.

For every school a plan closes or sends students to: enrollment, design capacity, utilization,
classroom sections and average class size, before and after. Sections use the same rule as the cost
model (each grade gets enough sections to stay at or under the class-size cap). "After" counts every
moved student, before any family leaves, so it is the most crowded case.
"""
import math

import pandas as pd

from ..closure_model import GRADES_IN_MERGED_PAIR
from ..costs import class_size_cap, classroom_sections
from ..reassignment import reassign_students


def _plan_moves(model, closed):
    return reassign_students(closed, model.schools, model.distances, model.assumptions, model.district_splits_for(closed))


def school_rows(model, label, closed):
    a = model.assumptions
    moves, enrollment_after = _plan_moves(model, closed)
    affected = list(dict.fromkeys(list(closed) + [m.to_school for m in moves]))
    rows = []
    for name in affected:
        s = model.schools[name]
        grades_after = GRADES_IN_MERGED_PAIR if s.paired_with in closed else s.n_grades
        before = float(s.enrollment)
        after = 0.0 if name in closed else enrollment_after[name]
        lo, hi = s.design_capacity_low, s.design_capacity
        midpoint = (lo + hi) / 2
        sections_before = classroom_sections(before, s.level, s.n_grades, a)
        sections_after = classroom_sections(after, s.level, grades_after, a)
        mps_design = s.mps_design_2024
        has_mps_design = not math.isnan(mps_design)
        rows.append(dict(
            plan=label, school=name, role="closes" if name in closed else "receives",
            sends_to="; ".join(sorted({m.to_school for m in moves if m.from_school == name})) if name in closed else "",
            receives_from="; ".join(sorted({m.from_school for m in moves if m.to_school == name})) if name not in closed else "",
            students_before=round(before), students_after=round(after),
            design_capacity=f"{lo:.0f}-{hi:.0f}" if lo != hi else f"{hi:.0f}",
            mps_design_2024=round(mps_design) if has_mps_design else None,
            util_2024_design_before=round(before / mps_design, 2) if has_mps_design else None,
            util_2024_design_after=round(after / mps_design, 2) if has_mps_design and after else None,
            seats_left_2024_design=round(mps_design - after) if has_mps_design and after else None,
            utilization_before=round(before / midpoint, 2),
            utilization_after=round(after / midpoint, 2) if after else None,
            open_seats_after=round(lo - after) if after else None,
            sections_before=sections_before, sections_after=sections_after if after else None,
            class_size_before=round(before / sections_before, 1) if sections_before else None,
            class_size_after=round(after / sections_after, 1) if sections_after else None,
            class_size_cap=class_size_cap(s.level, a),
        ))
    return rows


def system_summary(model, labelled_plans):
    """Buildings, seats, utilization and average class size across the whole district, today and per plan."""
    a, schools = model.assumptions, model.schools
    sections_today = sum(classroom_sections(s.enrollment, s.level, s.n_grades, a) for s in schools)
    rows = []
    for label, closed in [("Today", [])] + labelled_plans:
        if closed:
            _, enrollment = _plan_moves(model, closed)
        else:
            enrollment = {s.name: float(s.enrollment) for s in schools}
        open_schools = [s for s in schools if s.name not in closed]
        seats = sum((s.design_capacity_low + s.design_capacity) / 2 for s in open_schools)
        sections = sum(classroom_sections(enrollment[s.name], s.level,
                                          GRADES_IN_MERGED_PAIR if s.paired_with in closed else s.n_grades, a)
                       for s in open_schools)
        students = sum(enrollment[s.name] for s in open_schools)
        rows.append(dict(plan=label, buildings=len(open_schools), students=round(students), design_seats=round(seats),
                         utilization=round(students / seats, 2), sections=sections,
                         avg_class_size=round(students / sections, 1), sections_saved=sections_today - sections))
    return pd.DataFrame(rows)


def capacity_tables(model, labelled_plans):
    """labelled_plans: [(label, closed schools)]. Returns (school-by-school table, system summary)."""
    rows = [row for label, closed in labelled_plans for row in school_rows(model, label, closed)]
    return pd.DataFrame(rows), system_summary(model, labelled_plans)
