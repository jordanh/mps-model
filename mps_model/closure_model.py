"""The closure model: the net annual savings of closing a given set of schools.

    net savings = staffing savings + building savings + specialist sharing savings
                - extra busing - revenue lost with families who leave - one-time closure costs (amortized)

`ClosureModel.evaluate(closed)` runs the steps in order:
  1. reassignment.py   move each closed school's students to receiving schools
  2. costs.py          staffing cost of every affected school before and after; building savings
  3. transport.py      extra busing for the moved students
  4. attrition.py      students who leave the district, priced at the net revenue each one brings
  5. sharing.py        specialist sharing among the small schools left open
"""
from dataclasses import asdict, dataclass, field

from .assumptions import Assumptions
from .attrition import families_lost
from .costs import building_operating_savings, school_staffing_cost
from .geography import Distances
from .policy import closure_candidates, district_option_closures, protected_schools
from .reassignment import reassign_students
from .schools import load_schools
from .sharing import best_sharing_pairs
from .transport import busing_cost

GRADES_IN_MERGED_PAIR = 6   # a K-2 and 3-5 (or K-1 and 2-5) pair merged in one building serves K-5


@dataclass
class PlanResult:
    """Annual dollars unless noted. Field order is the column order of net_savings_by_closures.csv."""
    N: int                          # schools closed
    gross_closure_savings: float    # staffing + building savings
    staffing_savings: float
    building_savings: float
    sharing_savings: float          # specialist sharing among schools left open
    bus_cost: float
    new_riders: float               # students
    families_lost_direct: float     # students
    families_lost_spillover: float  # students
    students_lost: float            # students
    lost_family_cost: float         # revenue lost with the students who leave, net of their cost
    one_time_amortized: float
    total_costs: float              # busing + lost families + one-time
    gross_savings: float            # gross closure savings + sharing
    net_savings: float
    closed: list
    students_moved: int             # students
    moves: list = field(default=None, repr=False)          # detail: reassignment.StudentMove records
    pairs: list = field(default=None, repr=False)          # detail: specialist sharing pairs
    enrollment_after: dict = field(default=None, repr=False)

    def summary_row(self):
        """The curve-table row: every field except the detail, closed schools joined with '; '."""
        row = {k: v for k, v in asdict(self).items() if k not in ("moves", "pairs", "enrollment_after")}
        row["closed"] = "; ".join(self.closed)
        return row


class ClosureModel:
    def __init__(self, assumptions=None, schools=None):
        self.assumptions = assumptions or Assumptions.load()
        self.schools = schools or load_schools(self.assumptions)
        self.distances = Distances(self.schools)
        self.candidates = closure_candidates(self.schools, self.assumptions)
        self.protected = protected_schools(self.schools, self.assumptions)
        self.district_options = {k: district_option_closures(self.schools, k) for k in (1, 2, 3)}
        self._staffing_today = {
            s.name: school_staffing_cost(s.enrollment, s.level, s.n_grades, self.assumptions) for s in self.schools}

    def with_assumptions(self, assumptions):
        """The same schools under different assumptions (used for sensitivity runs)."""
        return ClosureModel(assumptions, self.schools)

    def district_splits_for(self, closed):
        """Address-based splits the district specifies for its own Option 2 or 3. They apply only when
        the closure set is exactly that option."""
        splits = self.assumptions.get("policy", "district_option_splits", {})
        for option, spec in splits.items():
            if set(closed) == set(self.district_options[int(option)]):
                return spec
        return {}

    def evaluate(self, closed, detail=False):
        closed = list(closed)
        a, schools = self.assumptions, self.schools
        moves, enrollment_after = reassign_students(closed, schools, self.distances, a, self.district_splits_for(closed))

        # Staffing: compare every school that closes or receives students, before and after.
        affected = set(closed) | {m.to_school for m in moves}
        affected = [n for n in schools.names if n in affected]
        staffing_before = sum(self._staffing_today[n] for n in affected)
        staffing_after = sum(
            school_staffing_cost(enrollment_after[n], schools[n].level, self._grades_after(n, closed), a)
            for n in affected if n not in closed)
        staffing_savings = staffing_before - staffing_after
        building_savings = sum(building_operating_savings(schools[c], a) for c in closed)
        gross_closure_savings = staffing_savings + building_savings

        one_time = len(closed) * a.get("building", "one_time_closure_cost") / a.get("building", "amortization_years")
        bus, new_riders = busing_cost(moves, schools, a)
        lost_direct, lost_spillover = families_lost(moves, closed, schools, a)
        lost_family_cost = (lost_direct + lost_spillover) * a.net_revenue_per_student
        sharing_savings, pairs = best_sharing_pairs(enrollment_after, closed, schools, self.distances, a)

        total_costs = bus + lost_family_cost + one_time
        result = PlanResult(
            N=len(closed),
            gross_closure_savings=gross_closure_savings,
            staffing_savings=staffing_savings,
            building_savings=building_savings,
            sharing_savings=sharing_savings,
            bus_cost=bus,
            new_riders=new_riders,
            families_lost_direct=lost_direct,
            families_lost_spillover=lost_spillover,
            students_lost=lost_direct + lost_spillover,
            lost_family_cost=lost_family_cost,
            one_time_amortized=one_time,
            total_costs=total_costs,
            gross_savings=gross_closure_savings + sharing_savings,
            net_savings=gross_closure_savings - total_costs + sharing_savings,
            closed=closed,
            students_moved=sum(schools[c].enrollment for c in closed),
        )
        if detail:
            result.moves, result.pairs, result.enrollment_after = moves, pairs, enrollment_after
        return result

    def _grades_after(self, name, closed):
        school = self.schools[name]
        return GRADES_IN_MERGED_PAIR if school.paired_with in closed else school.n_grades
