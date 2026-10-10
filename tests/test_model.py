"""Unit tests for the model's building blocks. Run with: python -m pytest"""
import math

import pandas as pd
import pytest

from mps_model.assumptions import Assumptions
from mps_model.closure_model import ClosureModel
from mps_model.costs import classroom_sections, school_staffing_cost
from mps_model.paths import SCHOOL_LOCATIONS
from mps_model.recruitment import Recruitment
from mps_model.schools import ELEMENTARY


@pytest.fixture(scope="module")
def model():
    return ClosureModel()


def test_workbook_loads_every_school(model):
    assert len(model.schools) == 60
    assert model.schools.total_enrollment == 27425


def test_capacity_comes_from_column_n(model):
    # Loring: 2024 Physical Space Study design enrollment 396 (MPS building report)
    assert model.schools["Loring"].design_capacity == 396


def test_routed_distances_cover_every_pair(model):
    assert model.distances.source == "routed"
    names = model.schools.names
    for a in names:
        assert model.distances.road_miles(a, a) == 0
        for b in names:
            if a != b:
                assert model.distances.road_miles(a, b) > 0 and model.distances.drive_minutes(a, b) > 0


def test_routes_are_never_shorter_than_the_straight_line(model):
    locations = pd.read_csv(SCHOOL_LOCATIONS).set_index("school")
    for a, b in [("Cityview", "HIA"), ("FAIR", "North"), ("Wellstone", "South"), ("Kenwood", "Anwatin")]:
        dy = (locations.lat[a] - locations.lat[b]) * 69.0
        dx = (locations.lon[a] - locations.lon[b]) * 69.0 * math.cos(math.radians(locations.lat[a]))
        assert model.distances.road_miles(a, b) >= math.hypot(dx, dy)


def test_routed_times_are_plausible(model):
    # Cityview to HIA is about 1.1 road miles; North to South High about 6 road miles across downtown
    assert 0.9 < model.distances.road_miles("Cityview", "HIA") < 1.5
    assert 4 < model.distances.drive_minutes("North", "South") < 20


def test_round_trips_average_both_directions(model):
    miles, minutes = model.distances.both_ways("Ella Baker", "Whittier")
    assert minutes == pytest.approx((model.distances.drive_minutes("Ella Baker", "Whittier")
                                     + model.distances.drive_minutes("Whittier", "Ella Baker")) / 2)


def test_straight_line_source_still_works():
    a = Assumptions.load()
    straight = ClosureModel(a.with_values({("transport", "distance_source"): "straight_line"}))
    assert straight.distances.road_miles("Kenwood", "Anwatin") == pytest.approx(
        straight.distances.map_miles("Kenwood", "Anwatin") * a.get("transport", "circuity"))
    assert straight.distances.road_miles("Kenwood", "Anwatin") == straight.distances.road_miles("Anwatin", "Kenwood")


def test_protection_rules(model):
    assert "comprehensive high school" in model.protected["Southwest"]
    assert "Kenwood" in model.protected["Anwatin"]
    assert "Near North" in model.protected["Bethune"]
    assert "Loring" in model.candidates


def test_staffing_floor_makes_small_schools_expensive_per_student():
    a = Assumptions.load()
    small = school_staffing_cost(150, ELEMENTARY, 6, a) / 150
    large = school_staffing_cost(600, ELEMENTARY, 6, a) / 600
    assert small > large


def test_sections_respect_class_size_cap():
    a = Assumptions.load()
    assert classroom_sections(156, ELEMENTARY, 6, a) == 6   # 26 per grade fits one class each
    assert classroom_sections(162, ELEMENTARY, 6, a) == 12  # 27 per grade needs two


def test_closing_nothing_moves_no_one(model):
    r = model.evaluate([])
    assert r.students_moved == 0 and r.bus_cost == 0 and r.students_lost == 0
    assert r.net_savings == r.sharing_savings


def test_every_student_of_a_closed_school_is_placed(model):
    closed = ["Cityview", "Jenny Lind"]
    r = model.evaluate(closed, detail=True)
    for school in closed:
        placed = sum(m.students for m in r.moves if m.from_school == school)
        assert placed == pytest.approx(model.schools[school].enrollment)


def test_paired_campus_merges_with_its_partner(model):
    r = model.evaluate(["Wenonah"], detail=True)
    assert {m.to_school for m in r.moves} == {"Keewaydin"}


def test_recruit_value_tapers_with_utilization():
    rec = Recruitment(Assumptions.load())
    assert rec.value_of_recruit(0.70) == rec.net_revenue
    assert rec.value_of_recruit(0.85) == pytest.approx(rec.net_revenue - 3850 / 2)
    assert rec.value_of_recruit(0.95) < 0


def test_recruits_needed_closes_the_gap():
    rec = Recruitment(Assumptions.load())
    n, balances = rec.recruits_needed(10e6, 0.0, 25000, 40000)
    assert balances
    assert rec.annual_net_value(n, 0.0, 25000, 40000) >= 10e6 > rec.annual_net_value(n - 1, 0.0, 25000, 40000)


def test_recruiting_cannot_balance_when_buildings_are_full():
    rec = Recruitment(Assumptions.load())
    n, balances = rec.recruits_needed(30e6, 0.0, 39000, 40000)
    assert not balances and not math.isnan(n)
