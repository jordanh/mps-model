# Reproducibility

`reference_outputs/` holds the tables from a clean run of this repository (`python -m mps_model run`)
with the pinned versions in `requirements.txt` on Python 3.13. `python -m mps_model verify` compares a
results folder with it, table by table, allowing differences of one part in a billion (the last digit
of a float can differ across machines). `python -m pytest` runs the same comparison after
re-evaluating the saved closure sets; `python -m pytest -m slow` repeats the full search.

## Relation to the original model (version 7, Oct. 10, 2026)

This repository is a restructured copy of the model behind the plan in `docs/plan/`. Before the
reference outputs were saved, a clean run of the restructured code (full search, no saved inputs)
was compared with the original model's outputs, both for version 6 (Oct. 9: Middle Ground of 7 closures)
and for version 7 (Oct. 10: the 5% tolerance rule, Middle Ground of 5 closures). Both gave the same
result:

- **Identical**: `plans.json`, `plan_comparison.csv`, `three_plans_levers.csv`,
  `net_savings_by_closures.csv` (all 31 closure sets), `sensitivity.csv`,
  `lever_tradeoff_by_closures.csv`, `plan_reassignments.csv`, `plan_specialist_pairs.csv`,
  `glide_path.csv`, `capacity_summary.csv`, `closure_school_profiles.csv`.
- **One cell differs** in `capacity_class_size_impacts.csv`: Waite Park's average class size after
  District Option 1 is 24.1 here and 24.0 in the original. The exact value is 432.9 students / 18
  sections = 24.05; the original rounded with NumPy (round half to even on the binary value), this
  version rounds with Python. No plan total depends on it.
- **Figures** are pixel-identical except the glide path (fig10), whose step heights are now drawn
  from the unrounded pace instead of one backed out of the rounded bridge total (labels unchanged),
  and sub-pixel differences in the two maps with sharing pairs (pairs are drawn in a fixed order).

## What changed in the restructuring

- The code was split into one module per step, with the formulas documented in each module and in
  [model.md](model.md). Results are unchanged (above).
- The closure search runs in about a minute instead of about twelve, by reading school attributes
  from plain records instead of a pandas table inside the inner loop.
- Outputs no longer depend on Python's hash ordering: affected schools are summed in workbook order
  and sharing pairs are listed in workbook order.
- The pipeline writes each table once, instead of one script editing another script's outputs.
- The "growth areas unprotected" curve (dashed line in figure 1) is recomputed on every run with the
  current assumptions.
