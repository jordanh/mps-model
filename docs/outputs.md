# Outputs

A run writes these files to `results/` (or the folder given with `--results`). Copies of the tables
from a clean run are in `reference_outputs/`. Dollar amounts are annual unless noted.

## Tables

| File | One row per | What it shows |
|---|---|---|
| `net_savings_by_closures.csv` | number of closures N (0-30) | The best closure set found for N, with every savings and cost component |
| `plans.json` | | The Middle Ground size, each named plan's closed schools, the closure candidates and why every other school is protected |
| `plan_comparison.csv` | plan | Closures-only comparison: savings, costs, net, families lost, and recruits needed if net revenue alone closed the gap |
| `sensitivity.csv` | scenario | Net savings with attrition and busing assumptions at 0.5x, 1x and 1.5x |
| `three_plans_levers.csv` | plan | The main result: closures, sharing and recruitment together, recruits needed, campaign cost, years and bridge funding at the evidence and stretch paces |
| `lever_tradeoff_by_closures.csv` | N (0-16) | Families lost and recruits needed to balance at each number of closures |
| `glide_path.csv` | plan and school year | Shortfall bridge funding must cover each year (Family Trust and Middle Ground) |
| `plan_reassignments.csv` | plan, closed school, receiver | Students moved, miles, whether they keep their pathway, whether the student body is split |
| `plan_specialist_pairs.csv` | plan and pair | Schools sharing specialists, drive time and saving |
| `capacity_class_size_impacts.csv` | plan and affected school | Enrollment, utilization, sections and class size before and after |
| `capacity_summary.csv` | plan | District-wide buildings, seats, utilization and average class size |
| `closure_school_profiles.csv`, `.md` | school proposed for closure | Demographics, test-score trends, where students go |
| `unconstrained/net_savings_by_closures.csv` | N | The same curve with growth areas unprotected |

Plan names: "Optimum plan (5 closures)" in the closure tables is the **Middle Ground** plan.

## Figures (`results/figures/`)

| File | Shows |
|---|---|
| `fig1_net_savings_vs_closures.png` | Gross savings, costs and net savings by number of closures, with the district options |
| `fig1b_extended_stress_test.png` | The same curve to 30 closures |
| `fig2_plan_comparison.png` | Savings, costs and net by plan |
| `fig3`, `fig4`, `fig5`, `fig8` | Closure maps: Middle Ground, 3-closure variant, Middle Ground with sharing pairs, Family Trust |
| `figA1`-`figA3` | District Options 1-3 on the district's own option maps |
| `fig6_three_plans_lever_mix.png` | How each plan closes the gap, lever by lever |
| `fig7_lever_tradeoff.png` | Families lost and recruits needed by number of closures |
| `fig9_kenwood_pathway.png` | Kenwood's middle and high school path under each plan |
| `fig10_glide_path.png` | Bridge funding by school year |
| `fig11_capacity_class_size.png` | Middle Ground receiving schools: fullness and class size |
| `fig12_recruit_value_capacity.png` | Value of a recruit as buildings fill, with each plan's start and end |
| `basemaps/` | The district maps registered to one frame, used by the closure maps |
| `deck/` | With `--deck-images`: the figures cropped and padded for our slide deck |
