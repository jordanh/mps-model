# Three Levers, Three Plans: Balancing the MPS Budget While Keeping Families' Trust

*An alternative to the district's September 15, 2026 Options 1 to 3. Prepared October 8, 2026; revised October 9, 2026 with a higher cost per added student and a receiving-school capacity limit (Loring stays open; Jenny Lind merges into Lucy Laney), and again with capacity from the 2024 Physical Space Study for every building and a recruit value that falls as buildings pass 80% and 90% full, and on Oct. 10, 2026 with a Middle Ground of 5 closures, the fewest within 5% of the best net savings (Jenny Lind and Wenonah stay open). Revised again on Oct. 10, 2026 with distances and driving times routed on real streets instead of estimated from straight lines (Section 8.1). Many numbers moved slightly; the closures chosen did not change.*

> **How to read the numbers.** Every dollar figure is an annual, steady-state estimate from the model in `model/`:
> - `closure_model.py` handles closures, bussing, families leaving and specialist sharing.
> - `levers.py` handles recruitment cost, pace and bridge funding.
> - Inputs are in `model/assumptions.json`.
>
> District facts come from the Sept. 15, 2026 deck and the Oct. 6, 2026 Building Utilization workbook. Budget, staffing and transport costs come from the MPS FY27 adopted budget and news coverage (see `data/research_finance_sources.md`). Case studies are in `data/case_studies_other.md` and `data/case_hillsborough.md`. Any figure the public record does not give is marked **ESTIMATE**, with its reasoning recorded.

---

## 1. Summary

MPS has **three levers** to close an estimated **$35M** structural gap in FY28:

1. **Close schools.** This saves building and staffing costs, but costs families and bus miles.
2. **Share specialists.** Small nearby schools split art, music and PE specialists half-days. This saves money and costs no families.
3. **Recruit students.** Each added student brings about $11,500 a year. About half of it pays for that student, because some recruits fit into existing classes and others need new teachers, so MPS keeps about $5,750 a year. That holds while the buildings left open are under 80% full on average. Past 80%, extra busing eats into it, and past 90% each added student costs money, because MPS has to add classrooms or reopen buildings (Section 6).

The levers trade off against each other. **Closures can never close more than about $11M of the gap on their own** (plus $2.7-3.1M from sharing). **Net savings are nearly flat from 5 to 9 closures**, within $0.6M a year of each other, and **past 7 closures every additional closure makes the recruiting job bigger, not smaller**, because more families leave than the closure saves. So the Middle Ground stops at 5. Recruitment therefore carries most of the load in every plan. The real choice is how much of the system to disrupt in exchange for a smaller recruiting target.

| | **Family Trust plan** | **Middle Ground plan** | **Footprint-First plan** (district Options 1-3) |
|---|---|---|---|
| Buildings closed | 2 small HS programs merge; **no neighborhood or magnet school closes** | 5 (4 small HS programs + Cityview into HIA) | 14-16 |
| Students who change buildings | 105 | 776 | 3,032-3,538 |
| Families who leave MPS | about 20 | about 135 | about 1,250-1,640 |
| Net savings from closures + sharing | $8.1M | $11.9M | $1.7-6.7M |
| Recruitment effort | Full campaign | Full campaign | District's own strategy (enrollment held about flat) |
| New students needed to balance | 4,955 | 4,255 | 5,516-7,208 if it recruited (cost per recruit 50-80% higher) |
| Gap left with the plan's own recruitment | $0 | $0 | **$28.3-33.3M a year** |
| Years to balance at the evidence-based pace (2%/yr) | 8.6 | 7.6 | 13.6-18.6 if it recruited |
| Years to balance at the stretch pace (3%/yr) | 5.7 | 5.1 | 9.1-12.4 if it recruited |
| Bridge funding needed (evidence / stretch pace) | $108M / $67M | $81M / $50M | Never closes as planned |

**What this means**
- **Footprint-First is the weakest on every lever.** It closes the most schools and loses the most families, yet it saves less than the Middle Ground. It still leaves a $28-33M gap a year. If it tried to recruit its way out, it would need *more* students than the Family Trust plan, and each one would cost more to win. Its buildings are also fuller, so its last recruits are worth less: Option 3 would end at 88% of design enrollment.
- **Family Trust keeps the system intact.** It loses almost no families and has the cheapest cost per recruit. In exchange it needs about 700 more recruits than the Middle Ground, about a year longer to balance, and about $17-27M more bridge funding.
- **Both of our plans return Kenwood to the Southwest pathway** through its neighborhood middle school, Anwatin, which stays open. Southwest has 790-1,000 open seats (Section 3.4).
- **Middle Ground reaches balance soonest.** It has the smallest recruiting target, the fastest path to balance and the least bridge funding. In exchange it moves 776 students and loses about 135 families. Only one elementary building closes: Cityview, 29% full, into HIA.
- **Why 5 and not 7.** Closures 6 and 7 (Jenny Lind and Wenonah) would add only $0.6M a year, about 100 fewer recruits, and would move another 348 students and lose about 120 more families. The 5-closure plan balances slightly sooner (7.6 years against 7.8), because fewer families leave and each recruit is cheaper to win.

**Your intuition, with two corrections.**
- "7 closures if you invest little in recruitment" is not quite right. **No plan balances without about 4,000 or more recruits.** Even the Middle Ground leaves $23M to recruitment. A plan that does the minimum on recruitment (Footprint-First) does not balance the budget at all.
- **The precedents set the timeline.** No urban district we could find grew about 10% in three years through recruitment alone. **Tampa (Hillsborough) did not**: its district-run enrollment fell about 9% since 2018, including a 7,177-student drop in 2025-26. The best similar case is **Saint Paul**, next door. Its targeted Enrollment Project grew target schools 7-48% for about $425K, but the district as a whole gained only about 2% (about 600 students) in its best year. At that 2% pace, our plans balance in **about 7.6-8.6 years with bridge funding**. Balancing in 5-6 years needs the 3% stretch pace, with pre-K, identity programs and retention all working together.

**Recommendation.** Lead with the **Family Trust plan** if the Board's first goal is rebuilding confidence, and with the **Middle Ground** if its first goal is reaching balance soonest. Either is better than Footprint-First on savings, families kept and recruits needed. The deck presents all three side by side.

---

## 2. The three levers

| Lever | What it does | Best case | Limit |
|---|---|---|---|
| **School closures** | Removes duplicated staffing floors and building costs | About +$9.2M net at 5 closures, rising to $10.4M at 7 | Net savings barely change from 5 to 9 closures. Past 7, each closure costs more in departures and bussing than it saves. At 15 closures, net turns negative. |
| **Specialist sharing** | Two small schools split a 3-person specialist team half-days | $3.1M with no or few closures (13 pairs) | Pairs must be within about 15 minutes. Closures absorb small schools, so sharing falls to $0.5-1.0M at 14+ closures. |
| **Recruitment** | Fills empty seats with Minneapolis children now in charters (13,389), other districts (6,685), nonpublic schools (4,814), or never enrolled at K (K entry is 44%) | 2-3% growth a year, about 580-870 students | No precedent above about 3% a year without population growth. Cost per recruit rises with volume and with lost trust. |

**How closures change the recruiting job** (Figure 7, `outputs/lever_tradeoff_by_closures.csv`)

| Schools closed | 0 | 2 | 3 | **5** | 6 | 7 | 8 | 9 | 11 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|
| Families who leave | 0 | 22 | 54 | **135** | 202 | 257 | 359 | 475 | 785 | 1,724 |
| New students needed to balance | 5,898 | 4,955 | 4,683 | **4,255** | 4,183 | 4,150 | 4,192 | 4,273 | 4,692 | can't balance |
| Cost per recruit | $1,737 | $1,629 | $1,608 | **$1,599** | $1,621 | $1,656 | $1,706 | $1,769 | $1,953 | n/a |

**How the recruitment lever is modeled** (all values are **ESTIMATES** in `assumptions.json > recruitment`)
- **Base cost:** $1,000 per recruited student. Benchmarks are Florida pay-per-recruit contracts at $935 per student (Orange and Osceola, 2025-26) and Newark at $890.
- **Volume:** the average cost rises as easier families are reached first, doubling at 8,000 recruits.
- **Trust:** each 1% of enrollment lost to the system-wide loss of confidence raises the cost per recruit by 25%, and slows the pace by the same factor. Footprint-First's multiplier is 1.38-1.50. Family Trust's is 1.01.
- The campaign cost is amortized over 5 years and netted out of recruitment revenue.
- **Pace:** the evidence-based pace is 2% of enrollment a year (Saint Paul 2024-25); the stretch pace is 3%.
- **Bridge funding** is the sum of each year's shortfall until recruitment catches up. It would come from reserves (general fund balance $112M at the start of FY26) or temporary cuts.

---

## 3. The three plans

### 3.1 The Family Trust plan: close as little as possible, recruit with everything

- **Closures:** none of MPS's neighborhood or magnet schools. Two tiny specialty high school programs merge intact into comprehensive high schools, as every district option already proposes:
  - Heritage Academy (68 students) into Edison's Somali Heritage pathway
  - Longfellow Alternative (37) into North's Teen Parent Services
- **Specialist sharing:** 13 pairs, $3.1M a year.
- **Net savings:** $8.1M a year. Families who leave: about 20.
- **Recruitment:** 4,955 net new students, the full campaign in Section 14. Campaign cost is about $8.1M over the campaign years, at $1,629 per recruit.
- **Timeline:** balanced in about 8.6 years at the evidence-based pace, 5.7 at the stretch pace.
- **Bridge funding:** $108M (evidence-based pace) or $67M (stretch).
- **Promise to families:** a **five-year footprint pledge**. No neighborhood school closes through 2032.
- **Strongest when** the Board believes the trust lost after the 2021 redesign is the main reason families leave. In the two years after that redesign, more than 4,200 students left.
- **Main risk:** recruitment under-delivers. At 60% of target, an $11.4M gap remains.
- **Variant with zero closures**, keeping Heritage and Longfellow in place: $3.1M net, 5,898 recruits, 10.1 years at the evidence-based pace.

### 3.2 The Middle Ground plan: 5 closures, the fewest that capture nearly all the savings, plus full recruitment

- **Closures:**
  - The same 2 HS program merges, plus Wellstone into South and FAIR into North (also in every district option).
  - One elementary building, the emptiest in the district that can move whole into a school in the same pathway: Cityview (186 students, 29% of its MPS design enrollment) into HIA, 1.1 mi.
- No student changes high school pathway, and no growth-area school closes.
- **No receiving school goes above 75% of its MPS design enrollment** (Section 10.1). The fullest is North at 75%.
- **Why 5 (Oct. 10 revision):** net savings are nearly flat from 5 to 9 closures, between $11.9M and $12.5M a year. We now pick the fewest closures within 5% of the best result. The next two closures the model would add are Jenny Lind into Lucy Laney (+$0.4M a year) and Wenonah into its paired Keewaydin campus (+$0.2M). Together they would move another 348 students and lose about 120 more families for $0.6M a year and about 100 fewer recruits. Without them the plan balances slightly sooner.
- **Kept open: Jenny Lind, Wenonah and Loring.** Jenny Lind's scores are rising and no district option closes it. Wenonah stays as the K-1 campus of the Lake Nokomis Community School. An earlier version merged Loring into Jenny Lind and called both buildings nearly empty. That was wrong: Loring is 80-85% full, which MPS rates "efficient". Every district option still closes Loring and Wenonah.
- **Specialist sharing:** 12 pairs, $2.7M a year.
- **Kept open: Anwatin Middle,** the neighborhood middle school for Kenwood and Bryn Mawr (Section 3.4). Closing it would add only about $0.7M a year and would send Kenwood's 11-to-14-year-olds to Franklin in North Minneapolis.
- **Net savings:** $11.9M a year. Families who leave: about 135.
- **Recruitment:** 4,255 net new students. Campaign cost is about $6.8M at $1,599 per recruit.
- **Timeline:** balanced in about 7.6 years at the evidence-based pace, 5.1 at the stretch pace.
- **Bridge funding:** $81M or $50M.
- **Strongest when** the Board wants the fastest path to balance while closing only one neighborhood building.
- **Main risk:** recruitment under-delivers. At 60% of target, a $9.8M gap remains. Even at 1.5 times our attrition and bussing assumptions, net savings are still $11.5M.

### 3.3 The Footprint-First plan: the district's Options 1-3

- **Closures:** 14-16 buildings (Option 1: 15; Option 2: 14; Option 3: 16), moving 3,032-3,538 students. It includes schools in growth areas: HIA, Pratt, Webster, Bethune, Hiawatha and Howe.
- **Specialist sharing:** mostly lost ($0.5-1.0M), because the small schools that could share are the ones closed.
- **Net savings:** $1.7-6.7M a year in our model. The district's own figure is $0.2-2.4M after reinvestment.
- **Families who leave:** about 1,250-1,640. This matches research: closing districts in California lost about 288 students on average per district and saw no financial gain (Pearman, Stanford, Sept. 2026).
- **Recruitment:** the district's enrollment strategy holds K-12 at about 28,000 through 2035-36 (deck slide 95). The gap left is therefore **$28.3-33.3M a year**.
- To recruit its way to balance it would need 5,516-7,208 students at $2,407-2,860 each. At the trust-reduced pace that takes 13.6-18.6 years, with over $190M of bridge funding.
- **Kenwood:** Option 1 sends Kenwood to Franklin and North. Options 2 and 3 return Kenwood to Southwest, but through Anthony Middle, about 8.2 road miles away, because Anwatin closes. In the model that route alone adds about $2M a year in bussing.
- **Strongest when** the only goal is a smaller building footprint.
- **Main risk:** it locks in the largest departures and the largest structural gap.

### 3.4 Neighborhood pathways: Kenwood returns to Southwest (Family Trust and Middle Ground)

- **The change:** Kenwood Elementary feeds Anwatin Middle (3.1 road miles, about 10 minutes by car, as today; I-394, the bluff and Cedar Lake leave no direct street) and then **Southwest High instead of North**. This restores the high school Kenwood fed before the 2021 redesign. Bryn Mawr stays on its North pathway.
- **Why:** few Kenwood-area families followed the 2021 move.
  - North's principal estimates that about 15 white students came from the new south-side zones in five years (Star Tribune, Oct. 18, 2025).
  - Kenwood parents described a handful of former classmates at Anwatin, and families moving to St. Louis Park or choosing Southwest anyway.
  - The often-quoted "13" comes from the NYT (Nov. 2021): 13 white ninth-graders at North in the first year. We found no source for the claim that they were all gone by year's end. Details are in `data/kenwood_pathway_research.md`.
- **It is feasible.**
  - Southwest has 1,170 students in a building designed for 1,959-2,177, so it has 790-1,000 open seats.
  - Kenwood has about 62 students per grade, so even full continuation adds at most about 250 high schoolers.
  - Southwest is about 4.1 road miles from Kenwood, against 3.8 to North. High schoolers ride Metro Transit with a student pass, so no yellow-bus routes are added.
  - Default phase-in: incoming 9th graders from fall 2027. Current North students may stay through graduation.
- **The middle school is what makes it work.** Both of our plans keep Anwatin open.
  - The district's Options 2 and 3 also return Kenwood to Southwest, but they close Anwatin and route Kenwood's middle schoolers to Anthony, about 8.2 road miles away (about 16 minutes by car), where only about 100-200 seats are open.
  - In the model that route adds about $2M a year in bussing.
- **What it costs:**
  - Family Trust: nothing, since Anwatin was already open.
  - Middle Ground: about $0.7M a year against closing Anwatin, and about 120 more recruits than if Anwatin closed.
- **The selling point:** a **neighborhood pathway guarantee**. Every family can name its K-5, 6-8 and 9-12 schools from its address, and each is the nearby school its neighbors attend. Kenwood-area families who left MPS after 2021 are a natural "Come Home" audience (Section 14). That upside is not counted in the totals.

**Figures for this section:**
- **Figure 6** (`figures/fig6_three_plans_lever_mix.png`): how each plan closes the $35M, split into sharing, closures, recruitment and gap left.
- **Figure 7** (`figures/fig7_lever_tradeoff.png`): families who leave, and recruits needed, by number of closures.
- Maps: `figures/fig3_map_optimum_plan.png` (Middle Ground) and `figA1`-`figA3` (Footprint-First). Family Trust uses `figures/fig8_map_family_trust_plan.png`.

---

## 4. Can recruitment really work? Case studies

The case studies matter because recruitment is the lever every plan depends on. What the evidence supports, and what it does not:

### 4.1 Saint Paul Public Schools: the closest comparison (similarity very high; evidence medium at the school level, low district-wide)
- **Same state, same funding formula, similar charter share, next door.**
- **What they did:** the *Enrollment Project* (from Aug 2023, with vendor SchoolMint) worked with 6 under-enrolled schools. Tactics:
  - secret-shopper audits of the front-office experience;
  - tour training and fast follow-up;
  - multilingual social ads.
- Alongside it, identity-based programs (Hmong, East African, Spanish immersion) and pre-K expansion.
- **Cost:** about $425K over three years ($350K in the first two, $75K in the third; Star Tribune, Mar 2025).
- **Results:**
  - Targeted schools grew 7-48%. The East African Magnet grew 58%, outside the project.
  - District enrollment was 31,496 on Oct 1, 2024, up about 2% (about 600 students), its first increase in a decade.
- **Caveats:**
  - Immigration helped. Minneapolis also rose slightly that year.
  - Saint Paul then lost about 900 students by Mar 2026 after the immigration enforcement surge.
  - SchoolMint's "+527 students" is a vendor claim.
- **Lesson for MPS:** front-door basics are cheap and work at the school level, and identity programs draw families. Expect about 2% a year district-wide in a good year, not 10%.

### 4.2 DC Public Schools: the strongest evidence for the pre-K pipeline (evidence high, similarity medium)
- Enrollment grew from 44,718 (2009-10) to 52,036 (2024-25), **+16%**, while charters grew to about 48% of public enrollment.
- **The best causal evidence we found** comes from DC's randomized pre-K lottery (Braga et al., 2024). Children who won a Pre-K3 seat were:
  - up to **16.8 percentage points more likely to enroll in a DCPS kindergarten**;
  - 17.8 points less likely to switch schools.
- Effects were largest in low-income neighborhoods and dual-language programs.
- **Caveat:** DC's population grew. DCPS grew with the city and its share fell, so it did not win families back from charters.
- **Lesson for MPS:** universal pre-K placed inside the elementary building is the single most proven enrollment lever. It underpins the "Start Here, Stay Here" strategy.

### 4.3 Cleveland Metropolitan: stabilizing after decline (evidence medium, similarity high)
- After enrollment roughly halved from 2002 to 2011, the 2012 *Cleveland Plan* held it at about 38,000-39,000 for most of the next decade, and its share of district-plus-charter enrollment at about 72%. The plan combined:
  - a voter-approved levy;
  - autonomous schools;
  - partnerships with high-quality charters, sharing revenue;
  - new magnet high schools;
  - pre-K expansion.
- Its earlier door-to-door recruiting reportedly failed.
- **Lesson for MPS:** a credible whole-system quality plan, with a stable footprint, stopped the bleeding where marketing alone had not.

### 4.4 What did not work, or is not proven
- **Tampa (Hillsborough County):** the claim is **not supported**.
  - District-run enrollment fell from 195,016 (2018) to 177,336 (2025-26), about -9%.
  - Charter share rose to about 16%, and voucher requests rose 72% after Florida's 2023 universal voucher law.
  - An August 2026 headline projected a "small enrollment increase". The actual count came in about 2,650 lower.
  - Hillsborough closed schools in 2023-24 and again for 2026-27, and enrollment kept falling.
- **Florida pay-per-recruit contracts** (Caissa K12, $935 per student):
  - Orange County "recovered" 1,932 students in year 1 for about $1.8M, yet net enrollment still fell 5,539.
  - In Osceola, about 60 of 294 identified students enrolled.
  - Useful as a price benchmark, not as proof of net growth.
- **Miami-Dade** grew choice programs, from 35% to 61% of students and from 41K to 72K magnet seats. Total district enrollment still fell from 321K to 282K.
- **Detroit** spent about $3.5M a year on marketing and canvassing for +495 students (+1.1%) in 2025, about $7K per net student.
- **Research:**
  - A 2023 systematic review in the *Review of Educational Research* finds no causal evidence that district marketing alone raises net enrollment.
  - No rigorous evaluation of 8th-to-9th retention programs was found, so MPS should pilot one with a comparison group.

**Bottom line for the deck.** Recruitment can work when it changes what families get, through pre-K, identity programs, a guaranteed experience and stability, and not when it is only advertising. Plan on about 2% a year and design for 3%.

---

## 5. What the plans prioritize

1. **Balance the budget.** Close the FY28 structural gap (estimated at $35M) with recurring savings and recurring revenue, not reserves. The general fund balance is $112M and below the 8% policy.
2. **Deliver the "Minneapolis experience" everywhere.** Every school keeps the staffing floors the district promised: 3 specialists, reading and math interventionists, a social worker, and behavior support (Section 7).
3. **Protect growth.** Do not close schools in communities projected to grow 15% or more in the next 10 years. Those buildings will be needed.
4. **Keep pathways whole.** Keep today's elementary to middle to high school pathways (attached map). Receiving schools are always in the closed school's own pathway.
5. **Keep school communities together.** Each closing school moves as one student body to one receiving school, with no splitting.
6. **Share before closing.** Pair nearby small schools to share specialists half-days. This is cheaper and less disruptive than closing either one.
7. **Grow enrollment.** Make up the rest of the gap with students: smooth pre-K to K, bring families "home", recruit from charters and private schools, strengthen 8th to 9th grade, and guarantee stability.

---

## 6. The budget gap and how it is closed

| Item | Annual $ | Source |
|---|---|---|
| FY27 general fund (adopted June 9, 2026) | $734.7M spending / $737.3M revenue | MPS FY27 budget |
| FY27 gap closed with recurring cuts | $39.7M | MPS budget updates, Feb to June 2026 |
| **FY28 structural gap (planning figure)** | **$35M** (range $25-45M) | **ESTIMATE**: compensation grows 3-4% on a ~$580M staff base vs. 2-3% formula growth. MPS has re-forecast each year's gap upward by ~$20M mid-cycle. |
| Net savings from closures + specialist sharing | **-$8.1M** (Family Trust) / **-$11.9M** (Middle Ground) | Model |
| **Remaining gap closed by recruitment** | **-$26.9M** / **-$23.1M** | 4,955 / 4,255 students x $5,750, less the amortized campaign cost ($1.6M / $1.4M a year) |
| Net revenue per added student | $5,750 while open buildings are under 80% full; falls to $1,900 at 90%; -$1,900 above 90% | $11,500 marginal revenue (FY27 basic formula $7,683 + referendum ~$2,140 + compensatory) x 50% kept after the cost of serving the student, less busing and new-capacity costs as buildings fill (below). **ESTIMATE**, revised Oct. 9, 2026 |

**Why students and not more closures.** Each added student brings about $11,500 in revenue. MPS buildings are only about 60% full, so space is not the constraint, but teachers are. A student who fills a seat in a class that already exists costs about 30% of that revenue (supplies, services, some aide time). A student who forces a new class also needs about a 25th of a teacher plus a fifth of a specialist, about $6,000 more. Recruits cluster at kindergarten entry and at popular schools, so we assume about 40% need new classes, a blended cost of about 50%. Closing schools beyond 7 still costs more in departing families and bussing than it saves (Section 9).

**When buildings fill up (Oct. 9 revision).** The value of an added student depends on how full the district's open buildings are on average, after the closures and after the families each plan expects to lose:
- **Below 80% full:** MPS keeps the full $5,750. Recruits fit into buildings with room.
- **80% to 90% full:** the benefit shrinks in a straight line, from $5,750 to $1,900. More recruits have to be placed outside their neighborhood school, so each one adds busing, up to $3,850 a year at 90%. That is MPS's average cost per rider ($73M for about 19,000 riders, FY27 budget).
- **Above 90% full:** each added student costs MPS about $1,900 a year. Besides busing, MPS has to add classrooms or reopen a closed building, about $3,800 a seat a year. That is our **ESTIMATE** for reopening a 450-seat elementary: a new set of staffing floors (about $1.27M at MPS FY27 salary averages), running the building (about $0.30M, with utilities at the district deck's $0.635/sq ft), and about $0.6M of one-time reopening cost spread over 5 years.
- The 80% and 90% lines are a policy choice. They match the top of the 70-90% range MPS's building reports call "efficient".

| | Family Trust | Middle Ground | Option 1 | Option 2 | Option 3 |
|---|---|---|---|---|---|
| Students in buildings left open, after families leave | 27,403 | 27,290 | 25,991 | 26,173 | 25,790 |
| Design enrollment of buildings left open (MPS 2024 study) | 44,282 | 42,696 | 37,918 | 38,821 | 37,723 |
| Full before recruiting | 62% | 64% | 69% | 67% | 68% |
| Recruits that fit before 80% / 90% | 8,022 / 12,450 | 6,866 / 11,136 | 4,343 / 8,134 | 4,883 / 8,766 | 4,388 / 8,161 |
| Recruits needed to balance | 4,955 | 4,255 | 5,516 | 5,912 | 7,208 |
| Full after recruiting | 73% | 74% | 83% | 83% | 88% |
| Average value per recruit | $5,750 | $5,750 | $5,623 | $5,661 | $5,187 |

**What this changes.** Nothing for our two plans: both stay well below 80% full, with 2,600-3,100 recruits of room to spare before the busing costs start. The district options start fuller, so their last 1,000-2,800 recruits are worth less and they need more of them: 5,516-7,208, up from 5,378-6,387, and 13.6-18.6 years to balance at the evidence-based pace instead of 13.3-16.5. Past 14 closures the gap can no longer be closed by recruiting at all, because the open buildings would pass 90% first.

Figure 12 (`figures/fig12_recruit_value_capacity.png`) draws this curve with each plan's recruiting on it.

**This is a district average.** Individual schools fill sooner. Popular schools near 90% today would have to turn recruits away or add portables, while half-empty schools have room. The campaign therefore has to steer families to schools with room (Section 14), and a school-by-school limit would raise the targets somewhat.

**One-time costs.** Moving costs are about $0.6M per closed building (amortized at $0.60M a year for the Middle Ground's 5, over 5 years, and already netted in the figures above). Recruitment costs about $1,600-1,630 per student once volume and trust are priced in (Section 2). The base of $1,000 is benchmarked on Florida pay-per-recruit contracts (2025-26) at $935-985 per student. The campaign totals $8.1M for Family Trust and $6.8M for Middle Ground, amortized over 5 years and already netted in the targets.

---

## 7. What is the "Minneapolis experience"

This is the district's own promise (deck slides 84 to 90, "MPS student experience"). This plan keeps it in full, and the model funds every floor at every remaining school.

**Elementary school**
- At least **3 full-time specialists** at every site, including two arts areas plus physical education.
- A consistent **WIN ("What I Need")** block.
- A **reading and a math interventionist** at every site.
- **Behavior intervention staff** at every site.
- A **social worker** and education support professional (ESP) support.
- Inclusive services for students with an IEP and multilingual learners.
- Magnet theme experiences.

**Middle school**
- Rigorous core instruction aligned to state standards.
- Exploratory courses aligned to International Baccalaureate (IB).
- Advisory.
- Athletics and activities.
- Two intervention FTE (one reading), an instructional teacher on special assignment (TOSA), a counselor and a social worker.
- Dedicated security staff.
- Centrally run 5th-6th and 8th-9th transition programs.

**High school**
- All graduation requirements at every site.
- Career and technical education (CTE) and early college credit for all.
- Robust electives, athletics and activities.
- Post-secondary planning.
- Security staff.

**Pre-K in all 7 pathways.**

**The change in this plan.** At small schools, specialists may be **shared half-days** between two nearby buildings, so each school keeps the same specialist time per class. The 3-specialist team is shared rather than duplicated. This is how the plan pays for the experience at small schools without closing them.

---

## 8. How the model works

The model is `model/closure_model.py` (run `python3 closure_model.py`). It treats **every building as a candidate**, except:
- the 7 comprehensive high schools, which anchor the pathways;
- Anishinabe Academy, a new build under Board Resolution 2026-0047;
- the 20 schools in communities projected to grow by 15% or more.

That leaves 32 candidates.

**Building data.** All school names, enrollments and capacities come from the district's "Transformation Building Utilization Data - Oct 6, 2026" workbook. Current enrollment is its SY26 Enrolled Students (column L). Capacity is its 2024 Physical Space Study Estimated Design Enrollment (column N), the figure on MPS's public building reports. Four buildings have no value in column N: Longfellow and Anishinabe use the workbook's modeled future design enrollment (column O), and Heritage and Wellstone are assumed to hold 1.3 times their current enrollment. Locations come from the district's pathway map.

For each closure set it computes:

**1. Gross closure savings**
- Every building has staffing floors (the Minneapolis experience) plus classroom sections.
- When a school's students move to a receiver, the closed school's floors disappear. The receiver adds staff only where its larger enrollment needs more.
- Classroom sections are re-counted: partial classes combine.
- Building costs avoided:
  - utilities at $0.635/sq ft (district deck, slide 111);
  - maintenance net of mothballing at $0.85/sq ft (**ESTIMATE**);
  - half of custodial staff (the district redeploys the rest);
  - one engineer.
- Staff costs are MPS FY27 averages: teacher $123,762 loaded, secretary $75,410. Principal ($220k) and assistant principal ($190k) are **ESTIMATES**.

**2. Receiving schools**
- Students go to the nearest open school in the same high school pathway with room, after reserving room for that community's projected 10-year growth.
- Each school moves whole if any one receiver can take it. Otherwise it is split, with a family-loss penalty.
- Paired campuses (K-2 and 3-5 buildings) merge with their partner first.
- Magnets go to magnets, preferring the same theme.
- Specialty high school programs go where the district already plans: FAIR and Longfellow to North, Heritage to Edison, Wellstone to South.

**3. Extra bussing**
- Recomputed from the road distance between the closed school and its receiver, routed on the street network (Section 8.1).
- Walk zones are 0.5 mi (elementary) and 1.0 mi (middle).
- A rider costs $1,600 plus $900 per road mile per year. This is calibrated to MPS's $73M for about 19,000 riders, about $3,850 each.
- Once more than 600 new riders are added district-wide, new routes are needed and the marginal cost rises 60%.
- Rides longer than 3 road miles add $900 per extra mile.
- **So bussing cost climbs steeply as closures push students to more distant schools** (Figure 1b).

**4. Families leaving (non-linear)**
- **Direct loss** among displaced families is 8% for a single closure. That is Chicago's 2013 rate of 6%, plus 2 points for Minneapolis's dense charter market.
- It rises with every additional closure (+0.3 pt x (N-1)^1.4).
- It rises 4 points per extra mile of travel, 4 points if a school community is split, and 6 points if students must leave their pathway.
- **Spillover loss** from the whole district = 0.0052% x N^2.2 of all remaining students. That is about 0.4% at 7 closures and about 1.7% at 15.
- This captures the loss of confidence in the system. Locally, about 4,200 students (over 10%) left MPS in the two years after the 2021 redesign, which had no closures.
- Each departing student costs $5,750 a year in net revenue (the same blended 50% cost share, in reverse).

**5. Specialist sharing**
- Eligible: small elementary schools under 450 students, in pairs with no more than 700 students combined.
- A shared 3-person specialist team replaces two 3-person teams.
- Each pair's saving is net of:
  - lost teaching time for the midday trip (minutes / 435-minute day x salary);
  - mileage at the IRS rate of $0.725/mi x 174 days;
  - $15k in coordination.
- Pairs more than 15 minutes apart are not allowed. That counts the routed driving time plus 8 minutes to park and set up (Section 8.1).
- A maximum-weight matching picks the best set of pairs. As schools close, the remaining small schools are farther apart, so sharing savings shrink: $3.1M at 0-2 closures, $2.1-2.4M at 6-7, $0.5-1.0M at 14 or more.

**6. Search**
- For N = 1 to 16 (and on to 30 as a stress test), the model adds the single best closure, then tries every one-for-one swap until no swap improves net savings.
- District Options 1 to 3 are evaluated with exactly the same engine. Their closure sets come from the workbook: a blank in the Option column means the building is unprogrammed.

**Net savings** = gross closure savings + sharing savings - bussing - lost-family revenue - amortized one-time costs.

### 8.1 Road distances and driving times (Oct. 10, 2026)

Until Oct. 10, 2026 the model estimated road miles as the straight-line distance on the district's pathway map times 1.35, and driving time at an average 18 mph. It now uses real routes.
- **Streets:** every trip is routed on OpenStreetMap streets, from the Overture Maps release of Sept. 2026 (2026-09-23.1). One-way streets are respected.
- **Addresses:** each school is placed at its street address, not its position on the pathway map.
- **Driving time:** each street's posted speed limit, or Minneapolis's defaults where none is posted (20 mph on residential streets, 25 mph on other city streets), slowed by an estimated traffic factor for signals and school-hour traffic: 70% of the limit on arterials, 75% on local streets and 85% on freeways. This is our **ESTIMATE**. We use no live traffic data.
- **Construction:** current closures (the Penn Ave bridge over I-394 and part of Nicollet) are treated as open, because the plan starts in fall 2027.
- **How it compares:** routed road miles are a median 1.08 times the old estimate (half of school pairs fall between 1.01 and 1.21 times). Routed driving times are a median 0.76 times the old estimate. Short trips under 2 miles take about 18% longer than we had estimated, and cross-city trips about 40% less time, because they use freeways.
- **Two data corrections:** Las Estrellas's address was listed as Ella Baker's building. It is at 1201 University Ave NE (its map position was already right). Northrop's position on the pathway map was 1.1 miles off, and is corrected.
- **What changed in the results:** the closures chosen did not change for any plan. Middle Ground's net savings moved from $12.0M to $11.9M, and it now has 12 sharing pairs instead of 13. The district options fall more, to $1.7-6.7M, because their larger moves have longer real routes (Anwatin to Anthony is 9.4 road miles), so their bussing rises $1.5-2.4M a year.
- **How close the rule now is:** the 5-closure Middle Ground still clears the "fewest closures within 5% of the best" rule, but now by only about $8,500 a year (the 5% line is $11.89M, against the plan's $11.90M). If traffic were 20% slower than we assume, fewer specialist pairs would fit inside 15 minutes, and the rule would pick 6 closures, adding Jenny Lind.

---

## 9. Results

### 9.1 Net savings by number of schools closed (Figure 1)

| Schools closed | 0 | 1 | 2 | 3 | 4 | **5** | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Net savings ($M/yr) | 3.1 | 5.7 | 8.1 | 9.6 | 10.9 | **11.9** | 12.3 | 12.5 | 12.3 | 11.9 | 11.4 | 9.9 | 7.8 | 5.3 | 0.8 | -4.1 | -10.1 |

- N = 0 is specialist sharing alone.
- Savings rise steeply through the specialty high school merges and the emptiest elementary building, then flatten: from 5 to 9 closures net savings stay between $11.9M and $12.5M a year (Figure 1 shades this stretch). Beyond 9 closures, net savings fall faster than gross savings rise.
- The peak is $12.51M at 7 closures. **The plan takes the fewest closures within 5% of the peak: 5 closures, $11.90M** (rule changed Oct. 10, 2026; it was within $0.1M of the peak, which picked 7). With routed distances it clears the 5% line ($11.89M) by only about $8,500 (Section 8.1).
- **Receiving-school limit (Oct. 9 revision):** no receiving school is filled past 90% of its design enrollment in MPS's 2024 Physical Space Study, the figure on MPS's public building reports. This leaves room for growth and programs, and it is applied to every plan, including the district options.
- Anwatin is no longer a candidate: it stays open as Kenwood's and Bryn Mawr's neighborhood middle school (Section 3.4).
- Net savings turn negative at 15 closures. At 16 they are about -$10.1M, and about 2,060 students leave.
- Past 16 closures (Figure 1b), net savings drop to -$112M at 30 closures, driven by long bus rides and a collapse in family confidence.

### 9.2 Plan comparison (Figure 2, main results table)

All figures are $ millions a year, in the same model with the same assumptions.

| Plan | Schools closed | Students moved | Gross closure savings | Specialist sharing | **Gross savings** | Bussing | Families leaving | One-time (amortized) | **Total costs** | **Net savings** | Students lost | Remaining gap (of $35M) | **Recruits, before campaign cost** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Middle Ground** | 5 | 776 | 10.88 | 2.74 | **13.62** | 0.35 | 0.78 | 0.60 | **1.72** | **11.90** | 135 | 23.10 | **4,018** |
| 3-closure plan | 3 | 291 | 7.80 | 2.74 | **10.53** | 0.28 | 0.31 | 0.36 | **0.95** | **9.58** | 54 | 25.42 | **4,421** |
| District Option 1 | 15 | 3,338 | 25.78 | 0.57 | **26.35** | 9.63 | 8.24 | 1.80 | **19.68** | **6.67** | 1,434 | 28.33 | **4,927** |
| District Option 2 | 14 | 3,032 | 22.13 | 0.70 | **22.83** | 9.57 | 7.20 | 1.68 | **18.45** | **4.38** | 1,252 | 30.62 | **5,326** |
| District Option 3 | 16 | 3,538 | 24.86 | 0.20 | **25.06** | 12.00 | 9.40 | 1.92 | **23.33** | **1.73** | 1,635 | 33.27 | **5,786** |

Recruits before campaign cost = remaining gap / $5,750 (flat; the targets in Sections 1-3 and 14 also apply the capacity limits in Section 6), and already include replacing the students each plan expects to lose. The plan targets in Sections 1-3 and 14 also pay for the campaign itself, so they are higher (Middle Ground 4,255, 3-closure 4,683); the authoritative figures are in `outputs/three_plans_levers.csv`. The "Optimum plan" here is the Middle Ground plan.

**Why our figures differ from the district's.** The district reported net savings of about $0.2M to $2.4M for its options (Sept. 25, 2026). That is because it reinvests most of the freed staffing into the student experience and assumes only about 200 students leave. Our "gross savings" is the budget capacity a closure frees *before* reinvestment, because this plan uses it to close the gap and pays for the experience at small schools through specialist sharing instead. Our Options 2 and 3 follow the district's address split of Anwatin: Kenwood-area students (48%) to Anthony and Bryn Mawr-area students to Franklin. The long Anthony ride is one reason Option 2 models below Option 1.

### 9.3 The 3-closure plan
- The three most efficient closures are **Heritage to Edison, Longfellow to North, and Cityview to HIA**. Together they move 291 students and save $9.58M a year net, including $2.74M from 12 specialist-sharing pairs.
- It captures about four fifths of the Middle Ground's savings. It needs about 430 more recruits than the Middle Ground (4,683 against 4,255). The Middle Ground adds the two other specialty high school merges, Wellstone and FAIR. The Family Trust plan drops Cityview from this set and keeps it open.

### 9.4 Sensitivity

The same closure sets were re-run with family-loss and bussing assumptions halved and multiplied by 1.5. Values are net savings in $M a year.

| Scenario | Best N | Middle Ground (5) | 3-closure | Option 1 | Option 2 | Option 3 |
|---|---|---|---|---|---|---|
| Low (x0.5) | 9 | 12.30 | 9.78 | 12.84 | 10.00 | 8.98 |
| Central | 7 | 11.90 | 9.58 | 6.67 | 4.38 | 1.73 |
| High (x1.5) | 7 | 11.50 | 9.38 | 0.50 | -1.25 | -5.48 |

- **The 5-closure Middle Ground holds up where it matters.** If families leave at 1.5 times our estimate, it is within $0.1M of the best closure set. It gives up the most, $1.6M a year, only if families are much more loyal than we assume, when more closures would pay.
- In the central and high cases it beats every district option by about $5-17M a year. In the low case Option 1 saves $12.8M against the Middle Ground's $12.3M, but only by closing 15 buildings and losing about 1,430 families in the central case.
- **What protecting growth areas costs.** With protection turned off, the model would also close Hall and HIA in Near North (projected to grow 21%) and Webster in Northeast. Net savings would peak at $13.7M with 9 closures. Protecting growth areas therefore costs about **$1.2M a year**, about 200 recruited students, and avoids closing buildings the district will need again within 10 years.

---

## 10. The Middle Ground closures in detail (5 closures)

| Closed building | Students | Moves to | Road miles | Pathway | Kept together | Also closed in district options? |
|---|---|---|---|---|---|---|
| Heritage Academy (9-12) | 68 | Edison High (Somali Heritage + CTE programming) | 7.4 | kept (Districtwide to Edison program) | yes | 1, 2, 3 |
| Longfellow Alternative High (7-12) | 37 | North High (Teen Parent Services) | 6.4 | kept | yes | 1, 2, 3 |
| Wellstone International High (9-12) | 174 | South High (multilingual 18+ supports) | 4.3 | kept | yes | 1, 2, 3 |
| FAIR School for Arts (9-12) | 311 | North High (Arts magnet) | 2.2 | kept | yes | 1, 2, 3 |
| Cityview (PK-5) | 186 | Hmong International Academy | 1.1 | Camden | yes | 1, 3 |

**What the Middle Ground keeps open that the district would close:**
- **Anwatin Middle:** Kenwood's and Bryn Mawr's neighborhood middle school (Section 3.4).
- **Loring:** 80-85% full (MPS rates it "efficient"). No nearby school could take it without going above 90% full.
- **Wenonah:** the K-1 campus of the Lake Nokomis Community School. Merging it into Keewaydin would add only about $0.2M a year.
- **Growth areas:** HIA, Pratt, Webster, Bethune, Hiawatha and Howe (Near North +21%, University +35%, Northeast +16%, Longfellow +22%).
- **Southwest schools:** Kenny, Lake Harriet Lower and Field. Each adds little or nothing to net savings, and they save money by sharing specialists instead.
- It also keeps **Jenny Lind** open, which no district option closes.

**Specialist-sharing pairs in the Middle Ground plan (12 pairs, $2.74M a year):**

| Pair | Combined enrollment | Road miles | Travel minutes | Net saving |
|---|---|---|---|---|
| Howe + Anishinabe | 426 | 0.8 | 11 | $347k |
| Webster + Las Estrellas | 565 | 0.8 | 11 | $252k |
| Bethune + Hall | 479 | 0.9 | 12 | $322k |
| Keewaydin + Wenonah | 471 | 0.9 | 12 | $328k |
| Armatage + Kenny | 697 | 1.0 | 11 | $142k |
| Northrop + Hale | 700 | 1.3 | 13 | $139k |
| Lake Harriet Upper + Lake Harriet Lower | 586 | 1.5 | 14 | $232k |
| Pillsbury + Waite Park | 691 | 1.7 | 14 | $145k |
| Lucy Laney + Nellie Stone Johnson | 658 | 1.7 | 14 | $172k |
| Jenny Lind + Loring | 517 | 1.9 | 14 | $288k |
| Hiawatha + Folwell | 599 | 2.0 | 14 | $220k |
| Windom + Field | 684 | 2.6 | 13 | $151k |

Travel minutes are the routed driving time plus 8 minutes to park and set up.

*(The exact list is in `outputs/plan_specialist_pairs.csv`. The design agent should use that file, which is authoritative.)*


### 10.1 Capacity and class size after the moves (Figure 11)

Building capacity here is the design enrollment in MPS's 2024 Physical Space Study, the number on MPS's public building reports. Counts include every moved student, before any family leaves, so they are the most crowded case. Class sizes are modeled: each grade gets enough sections to stay at or under 26 students (elementary) or 30 (secondary). Real class sizes vary by grade.

**Middle Ground receiving schools**

| Receiving school | From | Students today | Students after | MPS design enrollment | Full today | Full after | Seats left | Avg. class today | Avg. class after |
|---|---|---|---|---|---|---|---|---|---|
| North | FAIR, Longfellow | 616 | 964 | 1,292 | 48% | 75% | 328 | programs move with their teachers | |
| South | Wellstone | 1,163 | 1,337 | 2,089 | 56% | 64% | 752 | program moves with its teachers | |
| Edison | Heritage | 844 | 912 | 1,421 | 59% | 64% | 509 | program moves with its teachers | |
| HIA | Cityview | 203 | 389 | 797 | 25% | 49% | 408 | 17 | 22 |

Family Trust only merges Heritage into Edison (59% to 64% full) and Longfellow into North (48% to 51%).

**What this means for families**
- No receiving building goes above 75% of its design enrollment, and every elementary class stays under the cap of 26.
- Elementary classes at HIA grow from about 17 to about 22 students. That is where the savings come from: two half-empty schools become one school with full classes and one set of staffing floors.
- The four high school programs move with their own teachers into buildings that stay at or below 75% full.

**Across the district**

| | Today | Family Trust | Middle Ground | Option 1 | Option 2 | Option 3 |
|---|---|---|---|---|---|---|
| School buildings in use | 60 | 58 | 55 | 45 | 46 | 44 |
| Share of design enrollment in use (MPS 2024 study) | 61% | 62% | 64% | 72% | 71% | 73% |
| Average class size (modeled) | 24.0 | 24.2 | 24.4 | 24.8 | 24.6 | 24.6 |
| Receiving schools at 88% or more of MPS design enrollment | | 0 | 0 | 11 | 8 | 12 |

Under the district options, 8 to 12 receiving schools end up at or near the 90% limit our model allows (Anthony at 99%, because the district's address split sends Kenwood-area Anwatin students there). Those buildings have little room left for growth, new programs or pre-K. The district's own workbook forecasts lower enrollments at many receivers, which implies more families leaving or moving outside their new attendance area.

**Data check (Oct. 9, 2026).** The building data come from the district's Oct. 6, 2026 utilization workbook. We checked them against MPS's 2024 building reports for 57 schools (`data/mps_building_reports_2024.csv`). The design enrollments match. Between Oct. 2024 and SY26, enrollment fell about 5% at the median school and 20-30% at Cityview, HIA, Jenny Lind, Pratt, Webster, Lyndale and Las Estrellas. Loring: 335 of 396 in Oct. 2024 (85%, "efficient") and 315 in SY26 (80%). Bethune: 244 of 532 in Oct. 2024 (46%) and 271 in SY26 (51%). Bethune is about half full, not nearly empty, and it stays open in our plans because Near North is projected to grow 21%. It shares specialists with Hall in the Middle Ground.

---

## 11. Reference variant: the 3-closure plan

| Closed building | Students | Moves to | Road miles |
|---|---|---|---|
| Heritage Academy | 68 | Edison High | 7.4 |
| Longfellow High | 37 | North High | 6.4 |
| Cityview | 186 | HIA | 1.1 |

Plus 12 specialist-sharing pairs ($2.74M), including Jenny Lind + Loring, which stay open and share specialists.

---

## 12. Profiles of schools proposed for closure

Full profiles are in `outputs/closure_school_profiles.md` and `.csv`. The Middle Ground closes all five programs below. Only one is a neighborhood elementary school: Cityview. Jenny Lind, Wenonah, Loring and Anwatin stay open in both of our plans and are not profiled here (Section 3.2). The Family Trust plan merges only the last two, Heritage and Longfellow, and keeps every neighborhood and magnet school open. Highlights:

**Cityview (PK-5, Camden pathway)**
- 186 students in a 121,588 sq ft building designed for 632 (MPS 2024 space study): 29% full.
- Students: 89% students of color (52% Black, 23% Hispanic); 90% free/reduced lunch; 26% special education (the site hosts ASD and ECSE programs).
- Reading 14% (2025) to 6% (2026). Math 6% (2024) to 9% to 12%.
- **Moves whole to HIA**, 1.1 mi away. HIA is a growth-area school with room: 203 students, design 797, so it goes from 25% to 49% full. The Turnaround Arts and full-service community school partnerships should move with the students.

**FAIR School for Arts (9-12)**
- 311 students, a downtown arts magnet.
- Reading 56% to 39%, math 17% to 2% (2025 to 2026; high school testing is grade 10 reading and grade 11 math).
- **Moves intact to North High's Arts magnet**, as all district options propose.

**Wellstone International High (9-12)**
- 174 newcomer English learners (99% EL).
- MCA proficiency of 0% reflects students who are new to English, not the program's quality.
- **Moves intact to South High's multilingual 18+ program.**

**Heritage Academy (9-12)**
- 68 students in a 193,441 sq ft building; Somali language and culture, STEM.
- **Moves intact to Edison's Somali Heritage pathway.**

**Longfellow Alternative High (7-12)**
- 37 students, teen parent services with on-site childcare.
- **Moves to North High's Teen Parent Services.** The on-site childcare must move too.

**Equity check.** All five closing programs serve mostly students of color and low-income families. That reflects where MPS has its smallest, least-used buildings, and it must be handled with care.
- Every move keeps the community together.
- Every move is to a school in the same pathway, within 1-3 miles for K-8.
- Programs, staff and partners move with the students.
- The district options close more of these schools: HIA, Bethune, Pratt, Webster, Loring and Anwatin as well.

---

## 13. Maps

- **Figure 8:** Family Trust plan, with its 13 specialist-sharing pairs.
- **Base maps:** our plans are drawn on the district's current pathway map with Kenwood's attendance area moved to the Southwest pathway, our only boundary change. Each district option is drawn on the district's own map for that option (Transformation Proposal, slide 24), so its new attendance boundaries are shown. Earlier versions drew all plans on today's boundaries, which misstated the district's options. `model/basemaps.py` builds the base maps.
- **Figure 3:** Middle Ground plan. Closed buildings are crossed out, with arrows to receiving schools.
- **Figure 4:** 3-closure plan.
- **Figure 5:** Middle Ground plan with the specialist-sharing pairs.
- **Figures A1-A3:** Footprint-First plan, district Options 1-3 as modeled.
- **Figure 6:** how each plan closes the $35M gap, by lever.
- **Figure 11:** Middle Ground receiving schools, share of design enrollment in use and average class size, before and after.
- **Figure 12:** what MPS keeps from each added student as the open buildings fill, with each plan's recruiting drawn from start to finish.
- **Figure 7:** families who leave, and recruits needed, by number of closures.
- **Figure 10:** the glide path, each school year's shortfall that bridge funding covers (`outputs/glide_path.csv`).

---

## 14. Recruitment strategy: the lever every plan depends on

**Targets.** Each plan's target is the number of net new students needed to close the rest of the $35M gap after its closures and sharing, including the cost of the campaign itself (`outputs/three_plans_levers.csv`).

| | Family Trust | Middle Ground | Footprint-First (if it recruited) |
|---|---|---|---|
| Net new students to balance | **4,955** | **4,255** | 5,516-7,208 |
| Growth on today's 29,149 | 17.0% | 14.6% | 18.9-24.7% |
| Cost per recruit | $1,629 | $1,599 | $2,407-2,860 |
| Campaign cost (total) | $8.1M | $6.8M | $13.4-20.6M |
| Recruits a year at the evidence-based pace (2%) | 580 | 559 | 387-421 |
| Years to balance | 8.6 | 7.6 | 13.6-18.6 |
| Open buildings full, before and after recruiting | 62% to 73% | 64% to 74% | 67-69% to 83-88% |
| Average value per recruit | $5,750 | $5,750 | $5,187-5,661 (buildings pass 80% full) |

**Timeline: a 7.6-8.6 year glide path at the evidence-based pace.** The deck presents the evidence-based pace of about 2% growth a year, the best district-wide year Saint Paul has had in a decade (Section 4.1). The yearly shortfall until recruitment catches up is bridged with reserves, temporary cuts and the first closure savings: $108M in total for Family Trust and $81M for Middle Ground. At the 3% stretch pace the plans balance in 5.7 and 5.1 years, with $67M and $50M of bridging.

**Milestones (October official counts, net new students over today):**

| October of year | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| Family Trust | 580 | 1,160 | 1,740 | 2,320 | 2,900 | 3,480 | 4,060 | 4,640 | **4,955** |
| Middle Ground | 559 | 1,118 | 1,677 | 2,236 | 2,795 | 3,354 | 3,913 | **4,255** | |

**Where the students come from** (full-scale targets, with about a 5% buffer above each plan's need; all **ESTIMATES**):

| Lever | Family Trust | Middle Ground | How it is counted | Evidence |
|---|---|---|---|---|
| Pre-K to K: "Start Here, Stay Here" | 1,850 | 1,650 | K entry raised from 44% to about 52% (about +400 kindergartners a year), held for 4-5 cohorts, net of later exits | **Strong:** DC Pre-K3 lottery, up to +16.8 points in district K enrollment (4.2) |
| "Come Home to MPS" (open enrollment out) | 1,000 | 900 | Win back 13-15% of the 6,685 residents who open-enroll out, starting with Kenwood-area families who left after 2021 | **Medium:** Saint Paul front-door work, targeted schools +7-48% (4.1) |
| Targeted charter and private recruiting | 1,150 | 1,000 | 5-6.5% of 13,389 charter and 4,814 nonpublic students, at grades 5-6 and 8-9 | **Medium:** Saint Paul identity programs; Cleveland held share against charters (4.3) |
| 8th to 9th grade transition | 450 | 350 | Cut 8th to 9th exits by about half | **Unproven:** pilot with a comparison group |
| Stability guarantee (retention) | 750 | 550 | +2 to +3 points of year-to-year retention | **Medium:** Cleveland's stable footprint; closure research (4.4) |
| **Total** | **5,200** | **4,450** | | |

Why Family Trust can ask for more: it has the lowest trust penalty (cost multiplier 1.01 against 1.04 for Middle Ground and 1.38-1.50 for Footprint-First), and the stability pledge is credible only when nothing closes.

**What the case studies say to do, and not to do**
- **Change what families get, not just the advertising.** Pre-K inside the elementary building (DC), identity and heritage-language programs (Saint Paul), and a guaranteed Minneapolis experience in every school. Marketing alone has no causal evidence behind it (4.4).
- **Fix the front door first.** It is cheap: Saint Paul's whole Enrollment Project cost about $425K over three years.
- **Do not buy recruits by the head.** Florida's $935-per-student contracts produced "recovered" students while net enrollment fell (4.4). Use the price only as a cost benchmark.

**1. Pre-K to K: "Start Here, Stay Here"**
- Pre-K in all 7 pathways, housed in the elementary school each pre-K family feeds into, so kindergarten is down the hall.
- Families who stay at the same school are much more likely to continue: 78% of public pre-K children stayed at the same school for K in a Miami study, and DC's lottery shows the effect is causal.
- Every MPS pre-K and ECFE family gets a pre-filled kindergarten seat by January, confirmed with one click.
- Spring "K Day" in the real classroom with the real teacher, a summer K bridge week, and shared pre-K to K portfolios.
- Birth-to-5 outreach at ages 3 and 4 through Hennepin County, Head Start, Way to Grow, child care centers and pediatric clinics.

**2. "Come Home to MPS": bringing students home**
- Map where resident children are not enrolled in MPS, by neighborhood and grade, using MDE resident and open-enrollment data.
- Message:
  - the guaranteed Minneapolis experience (3 specialists, interventionists, a social worker and a counselor at every site);
  - a full K-12 pathway;
  - free transportation;
  - heritage-language pathways (Spanish, Somali, Hmong, American Indian).
- Channels:
  - neighborhood digital campaigns in English, Spanish, Somali, Hmong and Oromo;
  - ethnic media;
  - paid parent ambassadors;
  - Saturday open houses;
  - libraries, Park Board centers, clinics and places of worship.
- Front-door basics, as in Saint Paul: secret-shopper audits of every front office, tour training, follow-up within 48 hours.
- Concierge enrollment: one phone and text line, a named navigator for each family, a tour in the same week, and mid-year enrollment welcomed.

**3. Targeted recruiting back from charters and private schools**
- Recruit at the natural exits: charters at 5th to 6th and 8th to 9th grade, privates at 8th to 9th, when tuition jumps.
- Offer what small charters cannot:
  - a comprehensive high school with athletics, CTE, AP/IB/College in the Schools and the arts;
  - full special education and EL services;
  - busing.
- "Soft landing" agreements with closing or shrinking charters, so whole cohorts transfer together.
- A fall "High school is free and comprehensive" campaign to 7th and 8th grade private and parochial families, with shadow days.

**4. 8th to 9th grade: tutoring and connecting with older students**
- Every 8th grader gets a paid 9th-12th grade "pathway buddy" from their future high school.
- High schoolers run paid after-school math and reading tutoring at feeder middle schools, partly funded from specialist-sharing savings.
- A two-week freshman summer academy at the pathway high school.
- High school counselors and coaches visit every feeder 8th grade, plus family nights in each heritage language.
- No rigorous evaluation of programs like this was found, so it runs as a pilot with a comparison group.

**5. Guaranteeing stability**
- **A five-year footprint pledge:** a Board resolution that no neighborhood school closes through 2032 (Family Trust), or no further closures beyond the plan's 5 (Middle Ground).
- **A pathway guarantee:** any student can finish their pathway K-12, and siblings get priority.
- **Staff stability:** teachers and partners move with their students, and class-size and specialist guarantees are published for each school.
- **A transportation guarantee:** a bus stop within 0.25 mi and published ride-time caps.
- **A public dashboard** of enrollment, budget and promises kept, updated every October.

**Cost and measurement**
- Campaign cost is $8.1M (Family Trust) or $6.8M (Middle Ground) in total, amortized over 5 years in the figures above.
- Track each October against MDE official counts, by lever and by pathway, against the milestone table. Two years in a row below 75% of the milestone triggers a Board review of the plan's footprint.

---

## 15. Risks and what to verify

- **FY28 gap.** $35M is an estimate. If the gap is $45M, about 1,740 more recruits are needed. If it is $25M, about 1,740 fewer.
- **Recruitment is now the biggest risk in every plan.** At 60% of target, Family Trust leaves an $11.4M gap and Middle Ground $9.8M. No district we found grew about 10% through recruitment alone (Section 4), so the milestones in Section 14 are the early warning.
- **Bridge funding.** The 7.6-8.6 year glide path needs $81-108M of bridging ($50-67M at the stretch pace). The $112M general fund balance is already below the 8% policy, so reserves cannot carry all of it: plan on a mix of reserves, temporary cuts and, for Middle Ground, front-loaded closure savings.
- **Cost per added student.** We assume half of each recruit's $11,500 goes to serving them. If recruits fit mostly into existing classes (30%), Middle Ground needs about 3,000; if most need new classes (65%), about 6,100. Track new sections opened against students added each October.
- **Capacity is an average.** The busing and new-classroom costs start when the open buildings average 80% and 90% full. Popular schools reach those lines sooner. Track the number of schools above 90% each October, and steer recruits to schools with room.
- **Family-loss behavior** is the biggest uncertainty in the closure lever (Section 9.4). The Middle Ground stays the best closure set under it.
- **Building data.**
  - Wellstone has no square footage in the workbook (we assumed 80,000).
  - Heritage and Wellstone have no design capacity in the workbook (we assumed 1.3 times current enrollment), and Longfellow and Anishinabe have no 2024 study figure (we used the workbook's modeled future design).
  - Las Estrellas's address was listed as Ella Baker's building. We corrected it on Oct. 10, 2026 to 1201 University Ave NE; its map position was already right. Northrop's map position, 1.1 miles off, was corrected at the same time.
- **Score data** comes from secondary sites that republish MDE data. It should be checked against the Minnesota Report Card before publication. 2023-2024 scores were found for only a handful of schools.
- **Ask MPS for:**
  - the option-level cost breakdown;
  - the FY28 pro forma;
  - the referendum authority;
  - principal, custodial and engineering costs by building;
  - per-route bus rates;
  - deferred maintenance by building (for example, $12.6M of cooling at Field and $10.6M at Kenwood are in the capital plan).

---

## 16. Files

| File | What it is |
|---|---|
| `model/closure_model.py`, `model/assumptions.json` | The runnable model and every adjustable assumption |
| `model/levers.py` | The three plans: recruitment targets, cost per recruit, pace and bridge funding (run after the model) |
| `model/basemaps.py` | Base maps: the district's Option 1-3 maps registered to the current map, and the current map with Kenwood moved to Southwest |
| `model/figures.py`, `model/figures_levers.py`, `model/figure_kenwood.py`, `model/figure_glide_path.py`, `model/profiles.py`, `model/deck_images.py` | Re-draw the figures, profiles and deck images after a re-run (run basemaps.py first) |
| `data/district_maps/` | The district's current and Option 1-3 maps, extracted from slide 24 of the Sept. 15 proposal |
| `model/figure_recruit_value.py` | Figure 12, the value of an added student by how full the open buildings are (reads `assumptions.json > recruitment > capacity_response`) |
| `data/Transformation Building Utilization Data - Oct. 6, 2026.xlsx` | District workbook (input) |
| `data/mps_building_reports_2024.csv` | MPS 2024 building reports for 57 schools (second source for capacity) |
| `outputs/capacity_class_size_impacts.csv`, `outputs/capacity_summary.csv` | Capacity and class size before and after, by school and plan (`model/capacity_impacts.py`) |
| `data/map_positions_and_context.csv` | Per-school map position, community, growth, grades, magnet theme, paired campus |
| `data/school_profiles_public.csv` | Demographics and MCA scores for 53 schools |
| `data/school_addresses_approx.csv` | Addresses and approximate coordinates |
| `data/kenwood_pathway_research.md` | Kenwood pathway history, the NYT claim, and Southwest feasibility |
| `data/case_studies_other.md`, `data/case_hillsborough.md` | Case-study research with sources (Saint Paul, DC, Cleveland, Detroit, Tampa and others) |
| `data/research_finance_sources.md` | Budget, transport, staffing and attrition research with URLs |
| `outputs/net_savings_by_closures.csv` | The curve: N = 0-30 with every component |
| `outputs/three_plans_levers.csv` | **The three plans by lever (authoritative headline numbers)** |
| `outputs/lever_tradeoff_by_closures.csv` | Families lost, recruits needed and cost per recruit for N = 0-16 |
| `outputs/plan_comparison.csv` | Closure-model results table (recruits before campaign cost) |
| `outputs/plan_reassignments.csv`, `outputs/plan_specialist_pairs.csv` | Student moves and sharing pairs for every plan |
| `outputs/closure_school_profiles.md/.csv` | School profiles |
| `outputs/sensitivity.csv`, `outputs/unconstrained/` | Sensitivity runs |
| `figures/*.png` | Figures 1-10 and A1-A3; `figures/deck/` holds the deck-ready crops |
| `DESIGN_AGENT_INSTRUCTIONS.md` | Slide-by-slide brief for the presentation designer |

---

## Sources

Public documents only. Savings, families leaving, recruits and bridge funding are this plan's own estimates, calculated from them.

**Minneapolis Public Schools**
- *Transformation Proposal*, Board work session, Sept. 15, 2026 (options, option maps on slide 24, the MPS student experience on slides 84-90).
- *Transformation Building Utilization Data*, Oct. 6, 2026.
- MPS building reports (2024 Physical Space Study), one per school, mpschools.org > School Transformation > Building Reports. Enrollment as of Oct. 1, 2024.
- *10-year projected change in where students attend MPS schools*, and the current high school pathway map.
- FY27 Adopted Budget, budget.mpschools.org (June 9, 2026).

**State data**
- Minnesota Department of Education, FY27 general education formula ($7,683 per pupil unit).
- MCA results and 2024-25 demographics (MDE and NCES data, via SchoolDigger).

**News**
- MPR News, KSTP, CBS Minnesota and Fox 9 coverage of the Sept. 15 and Sept. 25, 2026 presentations.
- Minnesota Reformer (Oct. 17, 2024), MPS financial projections.
- Star Tribune (Mar. 6, 2020; Mar. 2025; Oct. 18, 2025); New York Times (Nov. 2021).
- Sahan Journal (Jan. 2024, Aug. 2026); KSTP (Nov. 2024).

**Roads**
- OpenStreetMap street network, via the Overture Maps Foundation transportation release 2026-09-23.1 (Sept. 2026), for road distances and driving times (Section 8.1).

**Research**
- UChicago Consortium on School Research (2015), on Chicago's 2013 closures.
- Pew Charitable Trusts (2011), *Closing Public Schools in Philadelphia*.
- Research for Action (2024), *Revisiting Research on School Closings*.
- Greaves, Wilson & Nairn (2023), *Review of Educational Research*; Pearman (Stanford, Sept. 2026); Kim (2024).
- Braga et al. (2024), EdWorkingPaper 24-1019, on DC Pre-K3; DC Mayor's office enrollment tables.
- Cleveland Transformation Alliance (2019) and Fordham Institute, on the Cleveland Plan; Chalkbeat on Detroit and Newark.

- Full URL list: `data/research_finance_sources.md`, `data/case_studies_other.md`, `data/case_hillsborough.md` and the `source_urls` column of `data/school_profiles_public.csv`.
