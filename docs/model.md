# The model, step by step

All dollar figures are annual and steady-state unless noted. Parameter names in `code font` are keys
in `config/assumptions.json`; their values and sources are listed in [assumptions.md](assumptions.md).
The module that implements each step is named in its heading.

## 1. Schools (`schools.py`, `policy.py`)

Each of the 60 buildings in the district's Oct. 6, 2026 utilization workbook becomes one record. The
workbook supplies enrollment (column L, SY26), the 2024 Physical Space Study design enrollment
(column N), the modeled future design range (column O), square footage, pathway, and whether each
district option keeps the building open. Our compiled context table adds each school's position on
the district map, its community, program type, grades and paired campus.

**Capacity** used when a school receives students is column N. Where N is blank, the top of
column O is used; where both are blank, 1.3 times current enrollment.

**Protected schools** are never closure candidates:

| Rule | Setting |
|---|---|
| Comprehensive high schools anchor the pathways | `policy.protect_comprehensive_hs` |
| Anwatin stays open as Kenwood and Bryn Mawr's walkable middle school | `policy.protect_neighborhood_middle` |
| Anishinabe's new building (Board Resolution 2026-0047) | `policy.protect_new_builds` |
| Elementary, middle and K-8 schools in communities projected to grow 15% or more in ten years (Central, Phillips, University, Longfellow, Near North, Northeast) | `policy.growth_protect_threshold` |

That leaves 31 candidates. Kenwood is moved back to the Southwest pathway (`policy.pathway_overrides`).

**District options.** A school is closed in district Option k when the workbook's Option k predicted
enrollment is blank (Anishinabe excepted: its program moves to a new building).

## 2. Moving students (`reassignment.py`)

Closed schools are processed paired campuses first, then largest first.

1. A split-grade campus (a K-2 paired with a 3-5, for example) merges into its partner.
2. A high school program moves intact into the comprehensive high school the district names
   (FAIR and Longfellow to North, Heritage to Edison, Wellstone to South).
3. A K-8 moves as two groups: K-5 (6/9 of students) and 6-8 (3/9).
4. Everyone else is offered compatible open schools ranked by: same pathway first; for magnets,
   magnets only, same theme first; then distance. If one school has room for the whole group (and
   choosing it does not break the pathway when the nearest school would not), everyone goes there.
   Otherwise students fill the ranked schools in turn and the student body is marked **split**.

**Room** at a receiving school is

    room = min(capacity - enrollment x max(0, community growth),   # policy.receiver_growth_reserve
               90% x 2024 design enrollment)                         # policy.receiver_max_share_of_mps_design
           - students already there

District Options 2 and 3 specify an address split for Anwatin (48% to Anthony, 52% to Franklin,
`policy.district_option_splits`); it is applied only when evaluating exactly those options.

## 3. Staffing and building savings (`costs.py`)

Every affected school (closed or receiving) is costed before and after.

    FTE for each role   = max(floor, students / students_per_FTE)
                          (for roles with floor 0: whole FTEs only, floor(students / students_per_FTE))
    classroom teachers  = grades x ceil((students / grades) / class-size cap)
    staffing cost       = sum over roles of FTE x loaded salary + classroom teachers x teacher salary

The floors encode the district's "MPS student experience" minimums (deck slides 84-90): for an
elementary, at least 3 specialists, 2 interventionists, 1 social worker, 1 behavior specialist,
2 office staff and a principal. Because a building pays its floor however small it is, merging two
small schools saves one floor. A K-8 adds a counselor. A merged K-2 + 3-5 pair is costed as one K-5.

    staffing savings = staffing before (closed + receiving schools) - staffing after (receiving schools)
    building savings = sq ft x (utilities + maintenance - mothballing cost per sq ft)
                     + sq ft / sq ft per custodian x custodian salary x 50%
                     + one building engineer

## 4. Busing (`transport.py`)

Cost per rider per year is `cost_per_rider_fixed + cost_per_rider_mile x road miles`, calibrated to
the MPS average of about $3,850 per rider. Road miles are straight-line miles times `circuity` (1.35).

For students of a community school that closes, moving `d` miles:

    trip before  = attendance_radius x circuity
    trip after   = sqrt(attendance_radius^2 + d^2) x circuity
    riding after = 1 - (1 - share_riding_now) x exp(-max(0, d - 0.1) / walk zone)
    extra cost   = students x [riding after x (fixed + per_mile x trip after + long-ride premium)
                               - share_riding_now x (fixed + per_mile x trip before)]

Trips longer than `max_ride_mi_before_premium` add `long_ride_premium_per_mi` per extra mile. Magnet
students already ride citywide, so only their added distance counts. High school program students
use Metro Transit, so only a small cost is added. When new riders exceed `spare_rider_capacity`,
each rider beyond it costs `congestion_multiplier` (1.6) times the average.

## 5. Families who leave (`attrition.py`)

For each group of moved students:

    leave rate = direct_base + direct_growth_per_closure x (N - 1)^direct_growth_exponent
               + direct_per_extra_mile x miles moved
               + split_body_penalty      (if the student body is split)
               + pathway_break_penalty   (if the students change high school pathway)
    capped at direct_cap; halved for high school programs, which move intact

and across every school that stays open, a loss of confidence:

    spillover = students in open schools x spillover_scale x N^spillover_exponent

Each student who leaves costs the district its net revenue:

    net revenue per student = revenue_per_pupil x (1 - variable_cost_share) = $11,500 x 0.5 = $5,750

## 6. Specialist sharing (`sharing.py`)

Among open elementary and K-8 schools under 450 students, two schools can share one specialist team
if their combined enrollment is at most `max_combined_enrollment` and the midday drive is at most
`max_travel_minutes`:

    drive minutes     = road miles / avg_speed_mph x 60 + fixed_transfer_minutes
    FTE recovered     = min(fte_saved_per_pair, 2 x floor - max(floor, combined students / 150))
    saving            = FTE recovered x teacher salary
                      - fte_saved_per_pair x drive minutes / workday_minutes x teacher salary
                      - fte_saved_per_pair x road miles x mileage_rate x school_days
                      - coordination_cost_per_pair

The pairs are chosen by a maximum-weight matching (networkx), so each school is in at most one pair
and the total saving is as large as possible.

## 7. Net savings and the search (`closure_model.py`, `search.py`)

    net savings = staffing savings + building savings + sharing savings
                - busing - families lost x $5,750 - N x one_time_closure_cost / amortization_years

For each N from 1 to `policy.extended_curve_max` (30), the search adds the single best candidate to
the best (N-1)-set, then tries every one-for-one swap and keeps any that improves net savings, until
none does. Net savings are nearly flat around the peak, so the **Middle Ground** plan is the fewest
closures whose net savings are within `policy.optimum_tolerance_share` (5%) of the peak, or
`policy.optimum_tolerance` ($0.1M) if that is larger, up to `policy.max_closures` (16). **Family Trust** is
the best 2-closure set.

## 8. Recruitment (`recruitment.py`, `levers.py`)

The gap left after closures and sharing, `structural_gap - net savings`, has to come from recruits.

**Value of a recruit** depends on how full the open buildings are on average
(utilization = students / total design capacity of open buildings):

| Utilization | Annual value of one more student |
|---|---|
| up to 80% | $5,750 |
| 80% to 90% | falls linearly by the busing cost per rider ($3,850), to $1,900 |
| above 90% | $5,750 - $3,850 - $3,800 (new seats) = -$1,900 |

Recruits are valued in steps of 10 as utilization rises.

**Cost of recruiting** (one-time, spread over `amortization_years`):

    trust multiplier = 1 + trust_sensitivity x (spillover students / enrollment) x 100
    cost per recruit = base_cost_per_recruit x trust multiplier x (1 + recruits / volume_half_point)

**Recruits needed** is the smallest number whose value, less the amortized campaign, closes the gap.
If utilization passes 90% first, the plan cannot balance through recruitment.

**Pace and bridge funding.** At the evidence pace (`evidence_pace_pct`, 2% of enrollment a year,
divided by the trust multiplier) recruits accumulate each October. Each year's shortfall, the value
of the full target less the value of recruits so far, must be bridged. The stretch pace is 3%.

The Footprint-First plans are scored with the district's own enrollment strategy
(`district_baseline_recruits` = 0, roughly flat), so their gap stays open; the table also reports the
recruits they would need to balance.

## 9. Reports and figures

`reports/capacity.py` lists, for each plan, every affected building's enrollment, utilization,
classroom sections and average class size before and after. `reports/profiles.py` profiles each
school proposed for closure. The figures in `figures/` read only these tables, so they can be
redrawn without re-running the model. See [outputs.md](outputs.md).
