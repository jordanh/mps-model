# Assumptions

Generated from `config/assumptions.json` by `python -m mps_model assumptions`. Do not edit by hand:
change the JSON file and regenerate.

**ESTIMATE** marks a value with no public figure behind it; it is a reasoned estimate and a good
candidate for sensitivity testing. **PLACEHOLDER** marks a value that has not been researched yet.


## Budget

| Key | Value | Source |
|---|---|---|
| `structural_gap` | 35000000 | ESTIMATE (central of $25-45M): FY28 structural gap. FY27 GF adopted $734.7M (budget.mpschools.org, June 9 2026) closed a $39.7M gap with recurring cuts; drivers (3-4% comp growth on ~$580M staff vs 2-3% formula growth) continue. No published FY28 figure as of Oct 2026. |
| `revenue_per_pupil` | 11500 | ESTIMATE from FY27 MPS budget: marginal revenue lost/gained per student = basic formula $7,683/APU (FY27) + referendum ~$2,140 + compensatory if eligible; range $10-13.5k. City Auditor rule of thumb ~$10k. |
| `variable_cost_share` | 0.5 | ESTIMATE (revised Oct. 9, 2026 after review): blended marginal cost of an added or lost student. About 30% of revenue follows a student who fills a seat in an existing class (supplies, services, some aide time). A student who forces a new class also needs about 1/25 of a teacher plus 0.2 FTE specialist (about $6,000, another 52% of revenue). Recruits cluster at K entry and popular schools; assuming about 40% need new classes gives 30% + 0.4 x 52% = about 51%, used as 50%. Previous value 0.30. |

## Staff cost

| Key | Value | Source |
|---|---|---|
| `teacher_loaded` | 123762 | MPS FY27 average teacher incl. ~37.7% fringe (budget book); used for specialists, interventionists, counselors and social workers (counselor $136k, SW $127k) |
| `esp_loaded` | 62000 | ESTIMATE: education support professional, loaded |
| `office_loaded` | 75410 | MPS FY27 average school secretary, loaded |
| `principal_loaded` | 220000 | ESTIMATE ($210-230k loaded) |
| `ap_loaded` | 190000 | ESTIMATE ($180-200k loaded) |
| `custodian_loaded` | 82000 | PLACEHOLDER |
| `engineer_loaded` | 98000 | PLACEHOLDER |

## Building

| Key | Value | Source |
|---|---|---|
| `utilities_per_sqft` | 0.635 | MPS deck slide 111: Option 1 removes ~1.0M operating sq ft (8.2M -> 7.2M) for $635,000/yr utility savings |
| `maintenance_per_sqft` | 1.25 | ESTIMATE: routine maintenance/repairs avoided on a mothballed building; mothballing still costs ~$0.40/sqft (security, minimal heat), netted below |
| `mothball_cost_per_sqft` | 0.4 | ESTIMATE: cost of keeping an unprogrammed building secure and heated |
| `sqft_per_custodian` | 36600 | MPS deck slide 111: current sq ft per custodial FTE |
| `custodial_savings_share` | 0.5 | ESTIMATE: deck assumes custodial staffing is redeployed to raise cleaning level; we count half as savings |
| `one_time_closure_cost` | 600000 | ESTIMATE: moving, IT, signage, receiving-school prep per closed building (one-time, amortized over 5 years in net figures) |
| `amortization_years` | 5 | ESTIMATE |

## Class size

| Key | Value | Source |
|---|---|---|
| `elementary` | 26 | ESTIMATE: blended K-5 section cap under MFT contract class-size targets |
| `middle` | 30 | ESTIMATE |
| `k8` | 27 | ESTIMATE |

## Staff floors

FTE required per building = max(floor, enrollment / students_per_fte). Encodes the 'MPS student experience' floors from deck slides 84-90.


**Elementary**

| Role | Minimum FTE | Students per FTE | Salary used |
|---|---|---|---|
| specialist | 3 | 150 | teacher_loaded |
| interventionist | 2 | 250 | teacher_loaded |
| social worker | 1 | 400 | teacher_loaded |
| behavior esp | 1 | 300 | esp_loaded |
| nurse health | 0.5 | 700 | esp_loaded |
| media | 0.5 | 700 | teacher_loaded |
| office | 2 | 300 | office_loaded |
| principal | 1 | 100,000 | principal_loaded |
| assistant principal | 0 | 550 | ap_loaded |

**Middle**

| Role | Minimum FTE | Students per FTE | Salary used |
|---|---|---|---|
| exploratory specialist | 4 | 150 | teacher_loaded |
| interventionist | 2 | 300 | teacher_loaded |
| counselor | 1 | 350 | teacher_loaded |
| social worker | 1 | 400 | teacher_loaded |
| tosa | 1 | 100,000 | teacher_loaded |
| security | 1 | 400 | esp_loaded |
| behavior esp | 1 | 300 | esp_loaded |
| office | 2 | 300 | office_loaded |
| principal | 1 | 100,000 | principal_loaded |
| assistant principal | 1 | 450 | ap_loaded |

## Transport

| Key | Value | Source |
|---|---|---|
| `distance_source` | routed | Oct. 10, 2026: road miles and driving minutes along the fastest route on the street network (OpenStreetMap roads via Overture Maps, release 2026-09-23.1; school addresses geocoded to Overture address points). Built by tools/routing/ and stored in data/compiled/school_drive_matrix.csv. 'straight_line' restores the earlier map-distance method. |
| `cost_per_rider_fixed` | 1600 | Calibrated so an average rider (~2.5 road mi) costs ~$3,850/yr: MPS $73M (2024-25) / ~19,000 daily riders |
| `cost_per_rider_mile` | 900 | Calibrated with the fixed term to MPS average $3,850/rider/yr |
| `circuity` | 1.35 | Routed trips between schools average 1.40 x the straight line (median; Overture/OpenStreetMap roads, Oct. 2026). Still used for the home-to-school legs the routing does not cover (attendance radius, magnet home distance) and to put routed trips on the straight-line scale of the per-mile attrition and walking coefficients. Earlier ESTIMATE: 1.35. |
| `walk_zone_elem_mi` | 0.5 | MPS deck slide 114 |
| `walk_zone_middle_mi` | 1.0 | MPS deck slide 114 |
| `attendance_radius_mi` | 0.9 | ESTIMATE: mean home-to-school distance in a K-5 attendance area (~2.5 sq mi per area) |
| `share_riding_now` | 0.55 | ESTIMATE: share of community-school students currently bused (outside 0.5 mi walk zone) |
| `spare_rider_capacity` | 600 | ESTIMATE: new riders that fit on existing routes before new buses/routes are needed |
| `congestion_multiplier` | 1.6 | ESTIMATE: marginal cost multiplier for riders beyond spare capacity (new routes, driver-shortage premiums, longer tiers) |
| `max_ride_mi_before_premium` | 3.0 | ESTIMATE: beyond this one-way road distance a dedicated route is needed |
| `long_ride_premium_per_mi` | 900 | ESTIMATE: extra annual cost per rider per mile beyond the threshold |

## Attrition

Students lost = direct (displaced students) + spillover (whole-district confidence). Both grow non-linearly with the number of closures N.

| Key | Value | Source |
|---|---|---|
| `direct_base` | 0.08 | Chicago 2013 closures: ~6% of displaced students left the district (UChicago Consortium); +2 pts for Minneapolis's dense charter/open-enrollment market (42% of residents already outside MPS, 2022-23) |
| `direct_growth_per_closure` | 0.003 | ESTIMATE: displaced families more likely to leave as more schools close (N=15 -> ~20% direct) |
| `direct_growth_exponent` | 1.4 | ESTIMATE: convex growth |
| `direct_per_extra_mile` | 0.04 | ESTIMATE: +4 pts leave rate per extra mile to the new school |
| `split_body_penalty` | 0.04 | ESTIMATE: +4 pts when a school community is split across receivers |
| `pathway_break_penalty` | 0.06 | ESTIMATE: +6 pts when students must leave their current high school pathway |
| `direct_cap` | 0.6 | ESTIMATE |
| `spillover_scale` | 5.2e-05 | ESTIMATE: share of ALL remaining students who leave = scale * N^2.2 (N=15 -> ~2%, ~500 students). Local evidence: MPS 2021 redesign (no closures) coincided with >4,200 students (>10%) leaving in two years |
| `spillover_exponent` | 2.2 | ESTIMATE: confidence collapse is strongly convex |

## Sharing

| Key | Value | Source |
|---|---|---|
| `levels` | ["elementary", "k8"] |  |
| `max_combined_enrollment` | 700 | ESTIMATE: 3 specialists rotating half-days can cover ~28 sections (~700 students) across two buildings |
| `fte_saved_per_pair` | 3 | User ask: specialists split half days at two schools; two 3-FTE floors become one shared 3-FTE team |
| `max_travel_minutes` | 15 | ESTIMATE: a midday transfer longer than ~15 min, including parking and setup, costs a teaching period and is impractical |
| `avg_speed_mph` | 18 | Used only when transport.distance_source is 'straight_line'. With routing, minutes come from the drive-time matrix (median about 18 mph between schools under 3 road miles apart, about 28 mph across all pairs). |
| `fixed_transfer_minutes` | 8 | ESTIMATE: parking, sign-in, setup (added to the routed driving time) |
| `workday_minutes` | 435 | ESTIMATE: 7.25 hr teacher duty day |
| `school_days` | 174 | MPS calendar (approx.) |
| `mileage_rate` | 0.725 | IRS 2026 standard mileage rate |
| `coordination_cost_per_pair` | 15000 | ESTIMATE: scheduling/stipends, duplicate materials |

## Policy

| Key | Value | Source |
|---|---|---|
| `growth_protect_threshold` | 0.15 | User ask: preserve schools in areas with large projected growth (10-yr change map). Communities >= +15% protected: Central, Phillips, University, Longfellow, Near North, Northeast |
| `protect_comprehensive_hs` | True | User ask: preserve current high school pathways |
| `protect_new_builds` | ["Anishinabe"] |  |
| `receiver_capacity_basis` | design_hi | Workbook 'Modeled Future Design Enrollment' upper bound |
| `receiver_growth_reserve` | True | Receivers keep room for their community's projected 10-yr growth |
| `max_closures` | 16 | User ask |
| `extended_curve_max` | 30 | Extension to show where costs explode |
| `pathway_overrides` | {"Kenwood": "Southwest"} | Reviewer and Jordan (Oct 8, 2026): return Kenwood to the Southwest High pathway it fed before the 2021 redesign. Southwest has 1,170 students in a building designed for 1,959-2,177 (workbook), so it has room. |
| `protect_neighborhood_middle` | ["Anwatin"] | Anwatin is the walkable neighborhood middle school for Kenwood and Bryn Mawr (1.1 and 0.2 road mi). Closing it sends Kenwood 6-8 students to Franklin in North Minneapolis (3.0 mi) or to Anthony (5.7 mi). Kept open so Kenwood's path is Kenwood - Anwatin - Southwest. |
| `district_option_splits` | {"2": {"Anwatin": {"Anthony": 0.48, "Franklin": 0.52}}, "3": {"Anwatin": {"Anthony": 0.48, "Franklin": 0.52}}} | District Options 2 and 3 send Kenwood-area students through Anthony Middle to Southwest; North Bryn Mawr goes to Franklin and North (Ward 7 News, Sept. 18, 2026; North News, Sept. 27, 2026). Kenwood share of Anwatin = Kenwood K-5 / (Kenwood + Bryn Mawr K-5) = 370 / 767 = 0.48. ESTIMATE |
| `middle_ground_closures` | 5 | Policy (Jordan, Oct. 10, 2026): Middle Ground is locked at 5 closures. The within-5%-of-peak rule below is now a check, not the selector (it picks 5 under routed central assumptions, by about $8,500). Set to null to let the rule choose. |
| `optimum_tolerance` | 100000 | Floor on the tolerance below, in $ a year (the earlier rule, Oct 8, 2026). |
| `optimum_tolerance_share` | 0.05 | Policy (Jordan, Oct. 10, 2026): pick the fewest closures whose net savings are within 5% of the peak. Net savings are flat from 5 to 9 closures (within $0.6M a year, under 2% of the $35M gap), and the plan aims for as few closures as possible. |
| `receiver_max_share_of_mps_design` | 0.9 | Policy (added Oct. 9, 2026 after Minneapolis Families for Public Schools' review): a receiving school may be filled to at most 90% of its design enrollment in MPS's 2024 Physical Space Study (the figure on MPS's public building reports), leaving room for growth and for programs. MPS rates 70-90% 'efficient'. |

## Recruitment

Used by levers.py. Turns the recruitment lever into a cost and a risk so the three plans can be compared on all three levers.

| Key | Value | Source |
|---|---|---|
| `base_cost_per_recruit` | 1000 | Florida pay-per-recruit enrollment contracts 2025-26: $935-985 per student enrolled (research_finance_sources.md section 8); rounded up |
| `volume_half_point` | 8000 | ESTIMATE: average cost per recruit rises linearly with volume as easier families are reached first; cost doubles at 8,000 recruits |
| `trust_sensitivity` | 0.25 | ESTIMATE: each 1% of district enrollment lost to spillover (loss of confidence) raises recruiting cost 25%; families who watched neighboring schools close are harder to win back |
| `campaign_years` | 3 | Plan: three enrollment cycles 2027-28 to 2029-30 |
| `amortization_years` | 5 | ESTIMATE: recruited students stay several years; one-time campaign cost spread over 5 years |
| `district_baseline_recruits` | 0 | District deck slide 95: enrollment strategies project ~28,000 K-12 students in 2030-31 and 2035-36, i.e. roughly flat; no net growth beyond today |
| `underdelivery_test` | 0.6 | Stress test: recruitment delivers only 60% of target |
| `resident_pool` | 25348 | MPS deck slide 96: residents in charters 13,389 + open enrollment out 6,685 + nonpublic 4,814 + homeschool 460 |
| `evidence_pace_pct` | 0.02 | Saint Paul Public Schools 2024-25: +2% (~600 students) in its best recent year (state Oct 1 count), aided by immigration; Detroit 2025 +1.1%. No urban precedent found for >3%/yr from recruitment alone (case_studies_other.md) |
| `stretch_pace_pct` | 0.03 | Stretch: stacks pre-K3/4 pipeline (DC lottery study: +16.8 pts K enrollment for Pre-K3 winners), identity/dual-language programs (SPPS +16-58% at those schools), re-enrollment metrics, and no further closures |
| `base_enrollment` | 29149 | MPS FY27 projected enrollment |
| `capacity_response.full_benefit_until_util` | 0.8 | Policy choice (Jordan): below 80% average utilization each recruit is worth the full net revenue ($5,750). |
| `capacity_response.taper_end_util` | 0.9 | Policy choice (Jordan): from 80% to 90% the value falls as more recruits must be bussed to buildings with room; at 90% new classrooms or buildings are needed. |
| `capacity_response.bus_cost_per_added_rider` | 3850 | MPS transportation about $73M (2024-25) / about 19,000 daily riders = $3,850 a rider a year. Phased in linearly from 80% to 90% utilization. |
| `capacity_response.new_capacity_cost_per_seat` | 3800 | ESTIMATE: reopening a closed elementary of about 450 seats: staffing floors (principal, office, specialists, interventionists, social worker) about $1.27M + building operations about $0.30M + reopening cost $0.6M over 5 years ($0.12M) = about $1.7M a year, or about $3,800 a seat. Applies to every recruit above 90% utilization, on top of busing. |
