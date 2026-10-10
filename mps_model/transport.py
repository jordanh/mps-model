"""Extra busing cost when students move to a farther school.

Cost per rider per year = fixed cost + cost per road mile x road miles, calibrated so the average
MPS rider (about 2.5 road miles) costs about $3,850 (MPS $73M for about 19,000 riders, 2024-25).

For a community school's students, we compare before and after:
  * before: students live on average `attendance_radius_mi` from school; `share_riding_now` ride.
  * after:  the trip grows to sqrt(radius^2 + distance moved^2), and fewer students can walk
            (the walking share decays exponentially with the distance moved).
Rides longer than `max_ride_mi_before_premium` need dedicated routes and cost a premium per mile.
Once more new riders join than existing routes have spare seats, each extra rider costs
`congestion_multiplier` times as much (new routes, driver shortages).

Magnet students already ride from across the city, so they only add the longer distance.
High school program students ride Metro Transit, so only a small cost for longer trips is added.
"""
import math

from .schools import HS_PROGRAM, MIDDLE

MAGNET_HOME_DISTANCE_MI = 2.5        # typical home-to-magnet distance today
HS_TRANSIT_RIDER_SHARE = 0.25        # high school program students whose longer trip costs anything
HS_TRANSIT_COST_FACTOR = 0.3         # transit passes cost a fraction of a yellow-bus mile
HS_TRANSIT_FREE_MILES = 1.0          # first road mile of extra distance costs nothing


def busing_cost(moves, schools, assumptions):
    """Returns (extra annual busing cost, number of new bus riders)."""
    get = lambda key: assumptions.get("transport", key)
    fixed, per_mile, circuity = get("cost_per_rider_fixed"), get("cost_per_rider_mile"), get("circuity")
    radius, share_riding_now = get("attendance_radius_mi"), get("share_riding_now")
    long_ride_mi, long_ride_premium = get("max_ride_mi_before_premium"), get("long_ride_premium_per_mi")

    total, new_riders = 0.0, 0.0
    for m in moves:
        closing = schools[m.from_school]
        n = m.students
        if closing.level == HS_PROGRAM:
            total += n * HS_TRANSIT_RIDER_SHARE * per_mile * max(0, m.miles * circuity - HS_TRANSIT_FREE_MILES) * HS_TRANSIT_COST_FACTOR
            continue
        if closing.is_magnet:
            road_before = MAGNET_HOME_DISTANCE_MI * circuity
            road_after = math.hypot(MAGNET_HOME_DISTANCE_MI, m.miles) * circuity
            extra = n * per_mile * (road_after - road_before)
            extra += n * max(0, road_after - long_ride_mi) * long_ride_premium
            total += extra
            continue

        walk_zone = get("walk_zone_middle_mi") if closing.level == MIDDLE else get("walk_zone_elem_mi")
        road_before = radius * circuity
        road_after = math.hypot(radius, m.miles) * circuity
        walking_before = 1 - share_riding_now
        walking_after = walking_before * math.exp(-max(0.0, m.miles - 0.1) / walk_zone)
        riding_after = 1 - walking_after
        cost_before = n * share_riding_now * (fixed + per_mile * road_before)
        cost_after = (n * riding_after * (fixed + per_mile * road_after)
                      + n * riding_after * max(0, road_after - long_ride_mi) * long_ride_premium)
        total += cost_after - cost_before
        new_riders += n * (riding_after - share_riding_now)

    spare_seats = get("spare_rider_capacity")
    if new_riders > spare_seats:  # new routes needed: riders beyond spare capacity cost more
        average = total / max(new_riders, 1)
        total += (new_riders - spare_seats) * average * (get("congestion_multiplier") - 1)
    return total, new_riders
