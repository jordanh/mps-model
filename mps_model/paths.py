"""Where the model finds its inputs and writes its results.

Everything is relative to the repository root, so the model runs the same way on any machine.
"""
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

ASSUMPTIONS_FILE = REPO_ROOT / "config" / "assumptions.json"

DATA_DIR = REPO_ROOT / "data"
DISTRICT_DATA_DIR = DATA_DIR / "district"      # files published by Minneapolis Public Schools
COMPILED_DATA_DIR = DATA_DIR / "compiled"      # tables we compiled from public sources

UTILIZATION_WORKBOOK = DISTRICT_DATA_DIR / "Transformation Building Utilization Data - Oct. 6, 2026.xlsx"
CURRENT_PATHWAY_MAP = DISTRICT_DATA_DIR / "current_hs_pathways_map.png"
GROWTH_MAP = DISTRICT_DATA_DIR / "projected_10yr_enrollment_change_map.webp"
DISTRICT_OPTION_MAPS_DIR = DISTRICT_DATA_DIR / "option_maps"

SCHOOL_CONTEXT = COMPILED_DATA_DIR / "map_positions_and_context.csv"
COMMUNITY_GROWTH = COMPILED_DATA_DIR / "community_growth.csv"
SCHOOL_PROFILES = COMPILED_DATA_DIR / "school_profiles_public.csv"

REFERENCE_OUTPUTS_DIR = REPO_ROOT / "reference_outputs"
DEFAULT_RESULTS_DIR = REPO_ROOT / "results"


class ResultsDir:
    """Layout of one run's results folder: tables at the top level, figures underneath."""

    def __init__(self, root):
        self.root = Path(root)
        self.figures = self.root / "figures"
        self.basemaps = self.figures / "basemaps"
        self.deck = self.figures / "deck"

    def create(self):
        for d in (self.root, self.figures, self.basemaps):
            d.mkdir(parents=True, exist_ok=True)
        return self

    def table(self, name):
        return self.root / name

    def figure(self, name):
        return self.figures / name
