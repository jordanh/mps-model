"""The school table: one record per school building, built from the district's utilization workbook
plus our compiled context table (map position, community, program type, grades, paired campus).

Key fields and where they come from:
  enrollment          workbook column L, "SY26 Enrolled Students"
  mps_design_2024     workbook column N, "2024 Physical Space Study Estimated Design Enrollment"
                      (the capacity figure on MPS's public building reports)
  design_capacity     the capacity the model fills receiving schools up to: column N where present,
                      otherwise the top of column O ("Modeled Future Design Enrollment"),
                      otherwise 1.3 x current enrollment
  open_in_option[k]   False when the district's Option k leaves the building unprogrammed
                      (a blank in that option's "Predicted Enrollment" column)
"""
import math
from dataclasses import dataclass

import pandas as pd

from . import paths

# Workbook header -> our field name. Column D has no header and is ignored.
WORKBOOK_COLUMNS = {
    "School Level": "level_raw",
    "Current High School Pathway": "hs_pathway",
    "School Name": "school",
    "Building Square Footage": "sqft",
    "Original Year Constructed": "year_built",
    "FRL>70%": "frl_over_70",
    "Core Grade Classrooms": "core_rooms",
    "Setting III Special Education Classrooms": "sped_rooms",
    "Specialist Spaces": "specialist_rooms",
    "Pre-K Classrooms": "prek_rooms",
    "SY26 Enrolled Students": "enrollment",
    "Highest Historic Enrollment (2019-2026)": "historic_max",
    "2024 Physical Space Study Estimated Design Enrollment": "mps_design_2024",
    "Modeled Future Design Enrollment": "modeled_design_range",
    "Option 1 Predicted Enrollment": "option1_enrollment",
    "Option 1 Predicted Building Utilization": "option1_utilization",
    "Option 2 Predicted Enrollment": "option2_enrollment",
    "Option 2 Predicted Building Utilization": "option2_utilization",
    "Option 3 Predicted Enrollment": "option3_enrollment",
    "Option 3 Predicted Building Utilization": "option3_utilization",
}

DEFAULT_SQFT = 80000             # Wellstone has no square footage in the workbook (ESTIMATE)
FALLBACK_CAPACITY_FACTOR = 1.3   # capacity when the workbook gives none: 1.3 x current enrollment

# School levels used throughout the model
ELEMENTARY, MIDDLE, K8, HIGH_SCHOOL, HS_PROGRAM = "elementary", "middle", "k8", "high_school", "hs_program"


@dataclass(frozen=True)
class School:
    name: str
    level: str                  # one of the level constants above
    program_type: str           # community, magnet, community_magnet, comprehensive_hs, hs_program
    is_magnet: bool             # citywide magnet (students come from across the city)
    magnet_theme: str | None
    grades: str                 # e.g. "K-5", "PK-8", "3-5"
    n_grades: int
    paired_with: str | None     # partner campus for split-grade pairs (e.g. a K-2 and a 3-5)
    community: str
    growth: float               # projected 10-year change in students attending MPS in this community
    hs_pathway: str             # high school pathway, after policy overrides
    pathway: str                # pathway label used to match receiving schools ("Magnet" for districtwide)
    enrollment: int             # SY26
    mps_design_2024: float      # NaN when the workbook gives none
    design_capacity: float      # upper capacity used for receiving students
    design_capacity_low: float
    sqft: float
    map_x: float                # position on the district's pathway map, in pixels
    map_y: float
    open_in_option: dict        # {1: bool, 2: bool, 3: bool}

    @property
    def has_partner(self):
        return self.paired_with is not None


class Schools:
    """Ordered collection of School records (workbook order), looked up by name."""

    def __init__(self, records, frame):
        self._by_name = {s.name: s for s in records}
        self.names = [s.name for s in records]
        self.frame = frame  # the merged table, for reports that want the raw columns
        self.total_enrollment = sum(s.enrollment for s in records)

    def __getitem__(self, name):
        return self._by_name[name]

    def __iter__(self):
        return iter(self._by_name.values())

    def __len__(self):
        return len(self.names)


def read_workbook(path=paths.UTILIZATION_WORKBOOK):
    """The district workbook with readable column names (as published, no adjustments)."""
    wb = pd.read_excel(path)
    wb = wb[[c for c in wb.columns if not str(c).startswith("Unnamed")]]
    missing = set(WORKBOOK_COLUMNS) - set(wb.columns)
    if missing:
        raise ValueError(f"Workbook is missing expected columns: {sorted(missing)}")
    return wb.rename(columns=WORKBOOK_COLUMNS)


def _parse_range(text):
    """'689 - 766' -> (689.0, 766.0); anything else -> (nan, nan)."""
    if isinstance(text, str) and "-" in text:
        lo, hi = [float(x) for x in text.split("-")]
        return lo, hi
    return math.nan, math.nan


def _level(program_type, grades):
    if program_type == "comprehensive_hs":
        return HIGH_SCHOOL
    if program_type == "hs_program":
        return HS_PROGRAM
    if grades == "6-8":
        return MIDDLE
    if grades in ("K-8", "PK-8"):
        return K8
    return ELEMENTARY


def _count_grades(grades):
    """'K-5' -> 6, 'PK-8' -> 9 (pre-K counted with K), '3-5' -> 3."""
    first, last = grades.replace("PK", "0").replace("K", "0").split("-")
    return int(last) - int(first) + 1


def _text_or_none(value):
    return value if isinstance(value, str) else None


def load_schools(assumptions):
    wb = read_workbook()
    context = pd.read_csv(paths.SCHOOL_CONTEXT)
    growth = pd.read_csv(paths.COMMUNITY_GROWTH).set_index("community").projected_10yr_change.to_dict()
    df = wb.merge(context, on="school", how="left")
    pathway_overrides = assumptions.get("policy", "pathway_overrides", {})

    records = []
    for r in df.itertuples(index=False):
        modeled_lo, modeled_hi = _parse_range(r.modeled_design_range)
        has_mps_design = not math.isnan(r.mps_design_2024)
        capacity_hi = r.mps_design_2024 if has_mps_design else modeled_hi
        if math.isnan(capacity_hi):
            capacity_hi = r.enrollment * FALLBACK_CAPACITY_FACTOR
        capacity_lo = r.mps_design_2024 if has_mps_design else modeled_lo
        if math.isnan(capacity_lo):
            capacity_lo = capacity_hi

        hs_pathway = r.hs_pathway
        pathway = "Magnet" if hs_pathway == "Districtwide Program" else hs_pathway.replace(" & Districtwide", "")
        if r.school in pathway_overrides:
            hs_pathway = pathway = pathway_overrides[r.school]

        records.append(School(
            name=r.school,
            level=_level(r.program_type, r.grades),
            program_type=r.program_type,
            is_magnet=r.program_type == "magnet",
            magnet_theme=_text_or_none(r.magnet_theme),
            grades=r.grades,
            n_grades=_count_grades(r.grades),
            paired_with=_text_or_none(r.paired_with),
            community=r.community,
            growth=growth.get(r.community, math.nan),
            hs_pathway=hs_pathway,
            pathway=pathway,
            enrollment=int(r.enrollment),
            mps_design_2024=float(r.mps_design_2024),
            design_capacity=float(capacity_hi),
            design_capacity_low=float(capacity_lo),
            sqft=DEFAULT_SQFT if math.isnan(r.sqft) else float(r.sqft),
            map_x=float(r.map_x),
            map_y=float(r.map_y),
            open_in_option={k: bool(pd.notna(getattr(r, f"option{k}_enrollment"))) for k in (1, 2, 3)},
        ))
    return Schools(records, df)
