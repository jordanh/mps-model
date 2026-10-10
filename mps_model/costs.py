"""What it costs to run a school, and what closing its building saves.

Staffing follows the "MPS student experience" floors in the district's Sept. 15, 2026 deck
(slides 84-90): every building needs a minimum staff (for an elementary, at least three specialists,
two interventionists, a social worker, a principal, an office) no matter how small it is, and more as
enrollment grows. That fixed floor is why consolidating two small schools saves money.

    FTE for a role  = max(floor, enrollment / students_per_FTE)
                      (roles with no floor only start at a full ratio: floor(enrollment / students_per_FTE))
    classroom teachers = grades x ceil(students per grade / class-size cap)

Building savings count utilities, routine maintenance (net of the cost of keeping a closed building
secure and heated), half of custodial staff, and the building engineer.
"""
import math

from .schools import ELEMENTARY, HIGH_SCHOOL, HS_PROGRAM, K8, MIDDLE

DEFAULT_GRADES = {ELEMENTARY: 6, MIDDLE: 3, K8: 9, HS_PROGRAM: 4, HIGH_SCHOOL: 4}


def class_size_cap(level, assumptions):
    if level == ELEMENTARY:
        return assumptions.get("class_size", "elementary")
    if level == K8:
        return assumptions.get("class_size", "k8")
    return assumptions.get("class_size", "middle")  # middle schools and high school programs


def classroom_sections(enrollment, level, n_grades, assumptions):
    """Classes needed so no grade exceeds the class-size cap (enrollment spread evenly across grades)."""
    if enrollment <= 0:
        return 0
    return n_grades * math.ceil((enrollment / n_grades) / class_size_cap(level, assumptions))


def school_staffing_cost(enrollment, level, n_grades, assumptions):
    """Annual cost of a school's building staff (at the floors) plus its classroom teachers."""
    if enrollment <= 0:
        return 0.0
    salaries = assumptions.raw["staff_cost"]
    floors = assumptions.raw["staff_floors"]["middle" if level in (MIDDLE, HS_PROGRAM) else "elementary"]
    total = 0.0
    for role, rule in floors.items():
        if role.startswith("_"):
            continue
        if rule["floor"] > 0:
            fte = max(rule["floor"], enrollment / rule["per"])
        else:
            fte = math.floor(enrollment / rule["per"])
        total += fte * salaries[rule["cost"]]["value"]
    if level == K8:  # a K-8 also needs a middle-grade counselor
        total += assumptions.get("staff_cost", "teacher_loaded")
    sections = classroom_sections(enrollment, level, n_grades or DEFAULT_GRADES[level], assumptions)
    total += sections * assumptions.get("staff_cost", "teacher_loaded")
    return total


def building_operating_savings(school, assumptions):
    """Annual savings from closing (mothballing) a building."""
    get = lambda key: assumptions.get("building", key)
    utilities = school.sqft * get("utilities_per_sqft")
    maintenance = school.sqft * (get("maintenance_per_sqft") - get("mothball_cost_per_sqft"))
    custodians = (school.sqft / get("sqft_per_custodian")
                  * assumptions.get("staff_cost", "custodian_loaded") * get("custodial_savings_share"))
    engineer = assumptions.get("staff_cost", "engineer_loaded")
    return utilities + maintenance + custodians + engineer
