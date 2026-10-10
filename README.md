# MPS school transformation model

A transparent, reproducible model of how Minneapolis Public Schools (MPS) could close an estimated
$35M structural budget gap with three levers:

1. **Closing or merging schools**, which saves staffing and building costs but adds busing and
   causes some families to leave the district.
2. **Sharing specialists** between small schools close to each other (art, music and PE teachers
   split half-days), which saves money without closing anything.
3. **Recruiting students** back from charters, other districts and private schools, which brings
   revenue but costs money to win and is limited by building space.

It compares three plans: **Family Trust** (two small high school program merges, recruitment does
most of the work), **Middle Ground** (the fewest closures that come within 5% of the best net savings, five
buildings, plus recruitment) and **Footprint-First** (the district's own Options 1-3 from its Sept. 15, 2026
proposal, 14-16 closures).

This is an independent analysis built from public documents. It is not an MPS product. Every value
that is not in the public record is labeled **ESTIMATE** in `config/assumptions.json`, with its
reasoning.

## Quick start

Requires Python 3.11 or newer (the reference outputs were produced with Python 3.13).

```bash
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python -m mps_model run              # about 1.5 minutes: every table and figure, written to results/
python -m mps_model verify           # compare results/ with reference_outputs/
python -m pytest                     # unit tests and a fast reproduction check
```

Other commands:

| Command | What it does |
|---|---|
| `python -m mps_model run --skip-figures` | Tables only (about 1 minute) |
| `python -m mps_model run --reuse-search reference_outputs/net_savings_by_closures.csv` | Skip the closure search and re-evaluate the saved closure sets (seconds). Useful after changing an assumption that should not change which schools are chosen. |
| `python -m mps_model run --assumptions my_assumptions.json --results results/my_case` | Run a scenario with your own assumptions file |
| `python -m mps_model figures` | Redraw figures from tables already in `results/` |
| `python -m mps_model run --deck-images` | Also write images sized for our slide deck |
| `python -m mps_model assumptions` | Regenerate `docs/assumptions.md` after editing the assumptions |
| `python -m pytest -m slow` | Repeat the full search and check it against the reference |

## How the model works

The short version is below. [`docs/model.md`](docs/model.md) walks through every step with its
formulas, and each module in `mps_model/` opens with a plain-language description of what it does.

```
config/assumptions.json ─┐
data/district/  ─────────┼─> schools.py ──> closure_model.py ──> search.py ──> plans.py ──> levers.py ──> reports/ ──> figures/
data/compiled/  ─────────┘   (one record     (net savings of     (best set     (Middle      (adds          (capacity,  (charts
                              per building)   any closure set)    for each N)   Ground,      recruitment)   profiles)   and maps)
                                                                                district
                                                                                options)
```

1. **Schools** (`schools.py`, `policy.py`). One record per building from the district's Oct. 6, 2026
   utilization workbook: enrollment, design capacity, square footage, pathway. Protected schools
   (comprehensive high schools, Anwatin, the new Anishinabe building, and schools in communities
   projected to grow 15% or more) are never closed.
2. **Closure model** (`closure_model.py`). For any set of closed schools it
   - moves each closed school's students to the nearest compatible school with room (by driving time
     on the street network; `geography.py`), keeping them in
     their high school pathway and together where possible (`reassignment.py`);
   - recomputes staffing at every affected school using the district's own minimum staffing floors,
     which is where most savings come from (`costs.py`);
   - adds busing for longer trips (`transport.py`) and prices the families who leave the district
     (`attrition.py`);
   - finds the best set of specialist-sharing pairs among the small schools left open (`sharing.py`).
3. **Search** (`search.py`). For each number of closures N from 1 to 30, a greedy search with
   one-for-one swaps finds the closure set with the highest net savings.
4. **Plans** (`plans.py`). Net savings are nearly flat from 5 to 9 closures. The Middle Ground plan
   is the fewest closures within 5% of the best. Family Trust is the best two-closure set. The
   district's options are scored with the same model.
5. **Levers** (`levers.py`, `recruitment.py`). The gap left after closures and sharing must come from
   recruitment. Each recruit is worth about $5,750 a year until the open buildings pass 80% full,
   less up to 90%, and costs money beyond that. Recruiting gets more expensive with volume and with
   the trust lost to closures. The model solves for the recruits each plan needs, the years it takes
   at a realistic pace, and the bridge funding until then.

## Repository layout

```
config/assumptions.json   every number the model assumes, each with its source
data/district/            files published by MPS (workbook, pathway maps, growth map)
data/compiled/            tables we compiled from public sources (map positions, school profiles,
                          geocoded school locations, the school-to-school drive-time table)
data/README.md            what each data file is, where it came from, and redistribution notes
mps_model/                the model (start with closure_model.py)
  reports/                school-by-school capacity and closure profiles
  figures/                charts and maps
tools/routing/            rebuilds the drive-time table from OpenStreetMap roads (optional; see its README)
reference_outputs/        the tables a clean run should reproduce (model version 8, Oct. 10, 2026)
tests/                    unit tests and the reproduction check
docs/model.md             the model, step by step, with formulas
docs/assumptions.md       every assumption as a table (generated)
docs/outputs.md           what each output table and figure contains
docs/reproducibility.md   how the reference outputs were checked
docs/plan/                the written plan these numbers support
docs/research/            research notes behind the assumptions and case studies
```

`results/` is created by a run and is not checked in.

## Changing an assumption

1. Edit the value in `config/assumptions.json` (keep the `src` note up to date).
2. Run `python -m mps_model run --results results/my_change` and compare its tables with
   `reference_outputs/`.
3. If the change is meant to become the new baseline, copy the new tables into `reference_outputs/`
   and regenerate `docs/assumptions.md`.

## Caveats

- **The budget gap is an estimate.** MPS has not published an FY28 figure. $35M is the middle of a
  $25-45M range reasoned from the FY27 budget.
- **Demographics and test scores are from secondary sources** (SchoolDigger, allk12, exploremps.org)
  that republish Minnesota Department of Education data. Check them against the Minnesota Report Card
  (rc.education.mn.gov) before quoting them. They feed only the closure profiles, not the dollar
  figures.
- **Driving times are modeled, not observed.** Distances are routed on OpenStreetMap streets
  (Overture Maps, Sept. 2026), but travel speeds are posted limits slowed by an estimated traffic
  factor, not live traffic data. See "Distances and driving times" in `docs/model.md`; rebuild the
  table with `tools/routing/` (for example `--traffic-scale 0.8` for slower traffic).
- **Behavioral parameters are estimates**, especially how many families leave after closures and how
  fast recruiting can grow enrollment. `sensitivity.csv` scales the attrition and busing assumptions
  by 0.5 and 1.5. The Middle Ground plan saves more than every district option in the central and
  high cases; in the low case, district Option 1 saves about $0.5M a year more.
- The Footprint-First rows model the district's options with this model's rules; they are not the
  district's own estimates.

## Sources

The district's Sept. 15, 2026 Transformation Proposal (Board work session deck) and the Oct. 6, 2026
Transformation Building Utilization workbook are the main inputs. The deck PDF is not included
(26 MB, and it is the district's document); download it from the district's school transformation
page, https://www.mpschools.org/about-mps/school-transformation. Budget, staffing and transportation
sources are listed in `docs/research/research_finance_sources.md` and next to each value in
`config/assumptions.json`.

## License

No license has been chosen yet. Until one is added, others may read the code but have no explicit
permission to reuse it. See `data/README.md` for the terms that apply to the data files.
