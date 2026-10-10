"""Where the students of a closed school go.

Rules, in order of priority:
  1. A split-grade campus (e.g. a K-2 paired with a 3-5) merges into its partner first.
  2. A high school program (FAIR, Heritage, Longfellow, Wellstone) moves intact into the comprehensive
     high school the district names for it.
  3. Everyone else goes to the nearest compatible open school by driving time, preferring
       - a school in the same high school pathway (citywide magnets only go to magnets, preferably
         with the same theme);
       - a single school that can take the whole student body, so classmates stay together, as long
         as that does not mean leaving the pathway.
     If no single school has room, students fill the nearest schools in turn ("split").
  4. A K-8 moves as two groups: grades K-5 to an elementary or K-8, grades 6-8 to a middle or K-8.

"Room" is the receiving school's design capacity, less room held back for its community's projected
growth, and never more than 90% of MPS's 2024 design enrollment (policy settings in assumptions.json).
Closed schools are processed paired campuses first, then largest first.
"""
import math
from dataclasses import dataclass, replace

from .policy import HS_PROGRAM_RECEIVER
from .schools import ELEMENTARY, HIGH_SCHOOL, HS_PROGRAM, K8, MIDDLE

MIN_USEFUL_ROOM = 5       # a receiver with 5 or fewer open seats is skipped
ROUNDING_SLACK = 0.5      # fewer than half a student left over counts as everyone placed


@dataclass(frozen=True)
class StudentMove:
    from_school: str
    to_school: str
    students: float
    road_miles: float         # road miles from the closed building to the receiving one
    drive_minutes: float      # driving minutes along that route
    effective_miles: float    # road miles / circuity, for coefficients set per straight-line mile
    keeps_pathway: bool       # students stay in their high school pathway
    body_split: bool          # the closed school's students land in more than one building


@dataclass(frozen=True)
class Receiver:
    name: str
    keeps_pathway: bool


def receiving_capacity(schools, assumptions):
    """Seats each school can fill up to when it receives students."""
    hold_for_growth = assumptions.get("policy", "receiver_growth_reserve")
    max_share = assumptions.get("policy", "receiver_max_share_of_mps_design")
    capacity = {}
    for s in schools:
        growth_reserve = s.enrollment * max(0.0, s.growth) if hold_for_growth and not math.isnan(s.growth) else 0
        seats = s.design_capacity - growth_reserve
        if max_share and not math.isnan(s.mps_design_2024):
            seats = min(seats, max_share * s.mps_design_2024)
        capacity[s.name] = seats
    return capacity


def _grade_compatible(closing, receiver):
    """Can the receiver's building serve the closing school's grades?"""
    if closing.level == ELEMENTARY:
        if receiver.level not in (ELEMENTARY, K8):
            return False
        # a split-grade campus (K-2, 3-5, ...) only takes students from its own partner
        return receiver.paired_with is None or receiver.name == closing.paired_with
    if closing.level == MIDDLE:
        return receiver.level in (MIDDLE, K8)
    if closing.level == K8:
        return receiver.level in (K8, ELEMENTARY, MIDDLE)
    return True


def ranked_receivers(closing, open_schools, schools, distances):
    """Compatible open schools for a closing school, best first.

    Ranking: same pathway before a pathway change, same magnet theme before a different one,
    then shortest drive first. A paired campus always comes first.
    """
    if closing.level == HS_PROGRAM:
        return [Receiver(HS_PROGRAM_RECEIVER[closing.name], True)]
    ranked = []
    for name in open_schools:
        other = schools[name]
        if name == closing.name or other.level in (HIGH_SCHOOL, HS_PROGRAM):
            continue
        if closing.is_magnet:
            if not (other.is_magnet or other.program_type == "community_magnet"):
                continue
            keeps_pathway = True  # magnets draw citywide, so there is no pathway to break
            different_theme = 0 if (closing.magnet_theme is not None and closing.magnet_theme == other.magnet_theme) else 1
        else:
            if other.is_magnet:
                continue
            keeps_pathway = other.pathway == closing.pathway or closing.pathway in str(other.hs_pathway)
            different_theme = 0
        if not _grade_compatible(closing, other):
            continue
        ranked.append((0 if keeps_pathway else 1, different_theme, distances.drive_minutes(closing.name, name), name, keeps_pathway))
    ranked.sort()
    receivers = [Receiver(name, keeps) for _, _, _, name, keeps in ranked]
    if closing.paired_with is not None and closing.paired_with in open_schools:
        receivers = [Receiver(closing.paired_with, True)] + [r for r in receivers if r.name != closing.paired_with]
    return receivers


def reassign_students(closed, schools, distances, assumptions, district_splits=None):
    """Move every closed school's students. Returns (moves, enrollment after the moves by school).

    district_splits: {closed school: {receiver: share}} for address-based splits the district itself
    specifies in one of its options; these replace the rules above for that school.
    """
    district_splits = district_splits or {}
    open_schools = [n for n in schools.names if n not in closed]
    enrollment = {s.name: float(s.enrollment) for s in schools}
    capacity = receiving_capacity(schools, assumptions)
    moves = []

    def move(closing, receiver, students, keeps_pathway, split):
        moves.append(StudentMove(closing, receiver, students, distances.road_miles(closing, receiver),
                                 distances.drive_minutes(closing, receiver), distances.effective_miles(closing, receiver),
                                 keeps_pathway, split))
        enrollment[receiver] += students

    processing_order = sorted(closed, key=lambda n: (not schools[n].has_partner, -schools[n].enrollment))
    for name in processing_order:
        closing = schools[name]
        students = enrollment[name]
        enrollment[name] = 0

        if name in district_splits:
            for receiver, share in district_splits[name].items():
                move(name, receiver, students * share, True, True)
            continue

        if closing.level == K8:  # grades K-5 and 6-8 move as two natural groups
            groups = [("K-5", students * 6 / 9), ("6-8", students * 3 / 9)]
        else:
            groups = [("all", students)]

        for group, group_size in groups:
            receivers = ranked_receivers(closing, open_schools, schools, distances)
            if group == "K-5":
                receivers = [r for r in receivers if schools[r.name].level in (ELEMENTARY, K8)]
            if group == "6-8":
                receivers = [r for r in receivers if schools[r.name].level in (MIDDLE, K8)]

            if closing.level == HS_PROGRAM:
                move(name, receivers[0].name, group_size, True, False)
                continue

            # Keep the student body together if one school has room, unless that breaks the pathway
            # when the top-ranked school would not.
            fits_whole = [r for r in receivers if capacity[r.name] - enrollment[r.name] >= group_size]
            if fits_whole and (fits_whole[0].keeps_pathway or not receivers[0].keeps_pathway):
                move(name, fits_whole[0].name, group_size, fits_whole[0].keeps_pathway, False)
                continue

            # Otherwise fill the best-ranked schools in turn.
            remaining = group_size
            for r in receivers:
                room = capacity[r.name] - enrollment[r.name]
                if room <= MIN_USEFUL_ROOM:
                    continue
                take = min(room, remaining)
                move(name, r.name, take, r.keeps_pathway, remaining < group_size or take < remaining)
                remaining -= take
                if remaining <= ROUNDING_SLACK:
                    break
            if remaining > ROUNDING_SLACK:  # nowhere has room: overflow into the top-ranked school
                fallback = receivers[0] if receivers else Receiver(open_schools[0], False)
                move(name, fallback.name, remaining, fallback.keeps_pathway, True)

            # Mark every move from this school as split if its students landed in more buildings than
            # its natural groups (one, or two for a K-8).
            n_buildings = len({m.to_school for m in moves if m.from_school == name})
            if n_buildings > (2 if closing.level == K8 else 1):
                moves = [replace(m, body_split=True) if m.from_school == name else m for m in moves]
    return moves, enrollment
