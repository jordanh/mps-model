# Data

## `district/`: published by Minneapolis Public Schools

| File | What it is | Source |
|---|---|---|
| `Transformation Building Utilization Data - Oct. 6, 2026.xlsx` | One row per building: level, high school pathway, square footage, year built, rooms, SY26 enrollment (col. L), historic maximum, 2024 Physical Space Study design enrollment (col. N), modeled future design range (col. O), and predicted enrollment and utilization under Options 1-3 (blank = building unprogrammed) | MPS, released Oct. 6, 2026 |
| `current_hs_pathways_map.png` | Current high school pathway map with attendance areas | MPS |
| `option_maps/option{1,2,3}.png` | Pathway maps for the district's Options 1-3, extracted from slide 24 of the Sept. 15, 2026 Transformation Proposal | MPS |
| `projected_10yr_enrollment_change_map.webp` | 10-year projected change in where students attend MPS schools, by community | MPS |

Not included: the Sept. 15, 2026 Transformation Proposal deck itself (26 MB PDF). Download it from
https://www.mpschools.org/about-mps/school-transformation. The model uses these facts from it:
the "MPS student experience" staffing floors (slides 84-90), utility savings per square foot
(slide 111), where Minneapolis resident students attend (slides 95-96), and walk zones (slide 114).

## `compiled/`: tables we compiled from public sources

| File | What it is | Used by |
|---|---|---|
| `map_positions_and_context.csv` | Each school's pixel position on the current pathway map, community, program type, magnet theme, grades and paired campus | the whole model |
| `community_growth.csv` | Projected 10-year change by community, transcribed from the growth map | protection rule, growth reserve |
| `school_profiles_public.csv` | Demographics (NCES 2024-25), MCA reading and math proficiency, EL and special education shares, programs, with source URLs per school | closure profiles only |
| `mps_building_reports_2024.csv` | MPS building reports (Oct. 1, 2024 enrollment, design enrollment, utilization rating, condition), used to check the workbook's capacity column | reference only |
| `school_addresses_approx.csv` | Street addresses and approximate coordinates | reference only |

Positions were read off the map image and checked against the street grid (122 pixels per mile,
median error about 0.15 mile).

**Check before public use.** Demographics and test scores in `school_profiles_public.csv` come from
SchoolDigger and allk12 (which republish Minnesota Department of Education data) and exploremps.org.
State data sites could not be reached when this was compiled. Verify against the Minnesota Report
Card (rc.education.mn.gov).

## Redistribution notes

These files were not created by us. Review them before publishing the repository:

| File | Note |
|---|---|
| `district/*` (workbook, three maps, growth map) | Public documents released by MPS for community review. Likely fine to share with attribution, but they are the district's work. If in doubt, replace them with download instructions. |
| `compiled/school_profiles_public.csv` | Facts compiled from SchoolDigger, allk12, NCES and exploremps.org. Facts are generally reusable, but SchoolDigger's terms restrict republishing its pages; the underlying MDE and NCES data are public. Consider re-sourcing from the Minnesota Report Card. |
| `compiled/mps_building_reports_2024.csv` | Figures transcribed from MPS's public building report pages (URLs included). |
| `docs/research/*.md` | Our notes, with short quotations from news articles and links to them. |
