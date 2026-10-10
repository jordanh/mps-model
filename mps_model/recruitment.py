"""The recruitment lever: winning back students who live in Minneapolis but attend charters, other
districts, private schools or home school (about 25,000 students, district deck slide 96).

Value of a recruit. Each added student brings net revenue (revenue per pupil minus the share of
cost that follows the student, about $5,750). That holds while the district's open buildings are on
average below 80% full. From 80% to 90%, more of each new cohort has to be bused to buildings with
room, so the value falls linearly by the busing cost ($3,850). Above 90%, new classrooms or reopened
buildings are needed and each recruit costs money.

Cost of recruiting. A campaign costs about $1,000 per recruit for the easiest families, rising
linearly with volume (doubling at `volume_half_point` recruits). Closures make it harder: each 1% of
enrollment lost to spillover raises the cost by `trust_sensitivity` (25%). The campaign cost is
spread over `amortization_years`.

Pace. Recruiting adds a share of enrollment each year (2% is the best urban evidence, 3% a stretch),
slowed by the same trust multiplier. Until recruits reach the target, each year's shortfall must be
covered by bridge funding.
"""
import math

INTEGRATION_STEP = 10    # recruits are valued in steps of 10 students as utilization rises
MAX_RECRUITS = 20000     # search limit when solving for recruits needed
MAX_BRIDGE_YEARS = 12


class Recruitment:
    def __init__(self, assumptions):
        self.a = assumptions
        self.net_revenue = assumptions.net_revenue_per_student

    def get(self, key):
        return self.a.get("recruitment", key)

    # --- value -------------------------------------------------------------------------------

    def value_of_recruit(self, utilization):
        """Net annual value of one more student when open buildings are `utilization` full on average."""
        full_until = self.a.recruitment_capacity("full_benefit_until_util")
        taper_end = self.a.recruitment_capacity("taper_end_util")
        busing = self.a.recruitment_capacity("bus_cost_per_added_rider")
        if utilization <= full_until:
            return self.net_revenue
        if utilization <= taper_end:
            return self.net_revenue - busing * (utilization - full_until) / (taper_end - full_until)
        return self.net_revenue - busing - self.a.recruitment_capacity("new_capacity_cost_per_seat")

    def total_value(self, n_recruits, enrollment, capacity):
        """Total annual net value of n recruits added to a district with this enrollment and capacity."""
        total, added = 0.0, 0
        while added < n_recruits:
            step = min(INTEGRATION_STEP, n_recruits - added)
            total += step * self.value_of_recruit((enrollment + added + step / 2) / capacity)
            added += step
        return total

    # --- cost --------------------------------------------------------------------------------

    def trust_multiplier(self, spillover_share):
        """How much harder recruiting gets when closures have cost the district families' confidence.
        spillover_share is the fraction of enrollment lost to spillover (0.01 = 1%)."""
        return 1 + self.get("trust_sensitivity") * spillover_share * 100

    def cost_per_recruit(self, n_recruits, spillover_share):
        """Average one-time campaign cost per recruit, and the trust multiplier behind it."""
        trust = self.trust_multiplier(spillover_share)
        volume = 1 + n_recruits / self.get("volume_half_point")
        return self.get("base_cost_per_recruit") * trust * volume, trust

    def annual_net_value(self, n_recruits, spillover_share, enrollment, capacity):
        """Recruits' annual value less the campaign cost spread over the amortization period."""
        cost, _ = self.cost_per_recruit(n_recruits, spillover_share)
        return self.total_value(n_recruits, enrollment, capacity) - n_recruits * cost / self.get("amortization_years")

    # --- solving -----------------------------------------------------------------------------

    def recruits_needed(self, gap_to_close, spillover_share, enrollment, capacity):
        """Fewest recruits whose net annual value closes `gap_to_close`.

        Returns (recruits, balances). When buildings fill past 90% before the gap closes, no number
        of recruits balances the budget; then returns the number that comes closest and False.
        """
        if gap_to_close <= 0:
            return 0.0, True
        best_n, best_value = 0, -math.inf
        n, value = 0, 0.0
        cost_years = self.get("amortization_years")
        while n < MAX_RECRUITS:
            value += INTEGRATION_STEP * self.value_of_recruit((enrollment + n + INTEGRATION_STEP / 2) / capacity)
            n += INTEGRATION_STEP
            cost, _ = self.cost_per_recruit(n, spillover_share)
            net = value - n * cost / cost_years
            if net > best_value:
                best_n, best_value = n, net
            if net >= gap_to_close:
                # refine to the exact student within the last step
                for m in range(n - INTEGRATION_STEP, n + 1):
                    if self.annual_net_value(m, spillover_share, enrollment, capacity) >= gap_to_close:
                        return float(m), True
                return float(n), True
        return float(best_n), False

    def recruits_per_year(self, pace_key, spillover_share):
        """Recruits a year at the evidence ('evidence') or stretch ('stretch') pace."""
        return self.get(f"{pace_key}_pace_pct") * self.get("base_enrollment") / self.trust_multiplier(spillover_share)

    def yearly_shortfalls(self, recruits_needed, per_year, enrollment, capacity):
        """Shortfall in each school year until recruiting reaches its target (recruits counted each
        October): the value the full target would bring less the value of recruits so far."""
        full_value = self.total_value(recruits_needed, enrollment, capacity)
        shortfalls, year = [], 1
        while year <= MAX_BRIDGE_YEARS and per_year * year < recruits_needed:
            shortfalls.append(full_value - self.total_value(per_year * year, enrollment, capacity))
            year += 1
        return shortfalls
