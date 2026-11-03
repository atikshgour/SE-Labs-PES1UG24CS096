"""Decision and loop branch coverage tests for the Lab 6 scheduler."""

import pytest

from irrigation_scheduler import schedule, should_irrigate, water_volume


@pytest.mark.parametrize(
    ("moisture", "rain", "stage", "expected"),
    [
        (60, 0, "seedling", False),       # moisture guard: true
        (59, 10, "seedling", False),      # rain guard: true
        (44, 0, "seedling", True),        # seedling threshold: true
        (45, 0, "seedling", False),       # seedling threshold: false
        (54, 0, "flowering", True),       # flowering threshold: true
        (55, 0, "flowering", False),      # flowering threshold: false
        (39, 5, "mature", False),         # mature rain guard: true
        (39, 4, "mature", True),          # mature threshold: true
        (40, 4, "mature", False),         # mature threshold: false
    ],
)
def test_irrigation_decision_branches(moisture, rain, stage, expected):
    assert should_irrigate(moisture, rain, stage) is expected


@pytest.mark.parametrize(
    ("area", "stage", "temp", "expected"),
    [
        (2, "seedling", 20, 4),
        (2, "flowering", 36, 15),
        (2, "mature", 9, 4),
        (2, "mature", 20, 8),
    ],
)
def test_volume_branches(area, stage, temp, expected):
    assert water_volume(area, stage, temp) == expected


@pytest.mark.parametrize("area", [0, -1])
def test_invalid_area_branch(area):
    with pytest.raises(ValueError, match="invalid area"):
        water_volume(area, "seedling", 20)


def test_empty_schedule_exits_loop():
    assert schedule([], 10) == []


def test_schedule_continue_and_budget_break():
    zones = [
        ("wet", 1, 60, 0, "seedling", 20),
        ("affordable", 2, 30, 0, "seedling", 20),
        ("over-budget", 2, 30, 0, "flowering", 20),
        ("never-reached", 1, 30, 0, "seedling", 20),
    ]
    assert schedule(zones, 5) == ["affordable"]


def test_schedule_uses_exact_budget_and_finishes_loop():
    assert schedule([("exact", 2, 30, 0, "seedling", 20)], 4) == ["exact"]
