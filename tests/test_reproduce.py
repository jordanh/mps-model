"""End-to-end check: re-running the model reproduces reference_outputs/.

The fast test re-evaluates the saved closure sets (a few seconds). The full test repeats the search
(about a minute); run it with: python -m pytest -m slow
"""
import pytest

from mps_model.paths import REFERENCE_OUTPUTS_DIR
from mps_model.pipeline import run
from mps_model.verify import TABLES, compare_table


def _check(results):
    problems = [p for name in TABLES for p in compare_table(name, results)]
    assert not problems, "\n".join(problems)


def test_tables_reproduce_from_saved_closure_sets(tmp_path):
    run(tmp_path, reuse_curve=REFERENCE_OUTPUTS_DIR / "net_savings_by_closures.csv", unconstrained=False,
        figures=False, log=lambda *_: None)
    _check(tmp_path)


@pytest.mark.slow
def test_full_search_reproduces_reference(tmp_path):
    run(tmp_path, unconstrained=False, figures=False, log=lambda *_: None)
    _check(tmp_path)
