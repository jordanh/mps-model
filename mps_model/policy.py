"""Policy rules: which schools may be closed, and the district's own Options 1-3.

A school is protected (never a closure candidate) when it is
  * a comprehensive high school, which anchors a high school pathway;
  * a neighborhood middle school we keep open on purpose (Anwatin, Kenwood's walkable middle school);
  * a new build approved by the Board (Anishinabe);
  * an elementary, middle or K-8 school in a community projected to grow 15% or more in ten years.
All of these are switches in config/assumptions.json under "policy".
"""
import math

from .schools import ELEMENTARY, HIGH_SCHOOL, K8, MIDDLE

# District proposal (Sept. 15, 2026 deck, slides 24 and 36-59): each specialty high school program
# merges into a comprehensive high school as an intact program.
HS_PROGRAM_RECEIVER = {"FAIR": "North", "Longfellow": "North", "Heritage": "Edison", "Wellstone": "South"}

# Anishinabe's building is blank in all three district options because the program moves to a new
# building, not because it closes. We do not count it as a closure.
NOT_A_CLOSURE_IN_DISTRICT_OPTIONS = {"Anishinabe"}


def protection_reason(school, assumptions):
    """Why a school cannot be closed, or None if it is a closure candidate."""
    if school.level == HIGH_SCHOOL and assumptions.get("policy", "protect_comprehensive_hs"):
        return "comprehensive high school (pathway anchor)"
    if school.name in assumptions.get("policy", "protect_neighborhood_middle", []):
        return "neighborhood middle school for Kenwood and Bryn Mawr"
    if school.name in assumptions.raw["policy"]["protect_new_builds"]:
        return "new build per Board Resolution 2026-0047"
    in_growth_area = not math.isnan(school.growth) and school.growth >= assumptions.get("policy", "growth_protect_threshold")
    if school.level in (ELEMENTARY, MIDDLE, K8) and in_growth_area:
        return f"{school.community} projected +{school.growth:.0%} growth"
    return None


def protected_schools(schools, assumptions):
    """{school name: reason} for every protected school, in workbook order."""
    reasons = {s.name: protection_reason(s, assumptions) for s in schools}
    return {name: why for name, why in reasons.items() if why}


def closure_candidates(schools, assumptions):
    return [s.name for s in schools if protection_reason(s, assumptions) is None]


def district_option_closures(schools, option):
    """Schools the district's Option 1, 2 or 3 closes (blank predicted enrollment), in workbook order."""
    return [s.name for s in schools
            if not s.open_in_option[option] and s.name not in NOT_A_CLOSURE_IN_DISTRICT_OPTIONS]
