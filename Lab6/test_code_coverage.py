"""Statement coverage tests for the Lab 6 irrigation scheduler."""

import pytest

from irrigation_scheduler import schedule, should_irrigate, water_volume


@pytest.mark.parametrize(
    ("moisture", "rain", "stage", "expected"),
    [
        (60, 0, "seedling", False),
        (30, 10, "seedling", False),
        (40, 0, "seedling", True),
        (50, 0, "seedling", False),
        (50, 0, "flowering", True),
        (55, 0, "flowering", False),
        (30, 5, "mature", False),
        (30, 0, "mature", True),
        (40, 0, "mature", False),
    ],
)
def test_irrigation_decision(moisture, rain, stage, expected):
    assert should_irrigate(moisture, rain, stage) is expected


@pytest.mark.parametrize(
    ("area", "stage", "temp", "expected"),
    [
        (10, "seedling", 20, 20),
        (10, "flowering", 20, 50),
        (10, "mature", 20, 40),
    ],
)
def test_water_volume(area, stage, temp, expected):
    assert water_volume(area, stage, temp) == expected


def test_schedule_skips_wet_zone_and_stops_when_budget_is_exceeded():
    zones = [
        ("wet", 10, 60, 0, "seedling", 20),
        ("dry", 10, 30, 0, "seedling", 20),
        ("too-expensive", 10, 30, 0, "flowering", 20),
    ]
    assert schedule(zones, 40) == ["dry"]
