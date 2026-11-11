import math

import pytest
from hypothesis import given, strategies as st

from processor import moisture_average, parse_zone, water_needed


@given(st.text() | st.none())
def test_parse_zone_fuzz(value):
    try:
        name, area = parse_zone(value)
    except ValueError:
        return
    assert isinstance(name, str) and name and name == name.title()
    assert math.isfinite(area) and area > 0


@given(st.text(min_size=1).filter(lambda s: ":" not in s and s.strip()),
       st.floats(min_value=0.001, max_value=1e8, allow_nan=False))
def test_parse_zone_valid(name, area):
    assert parse_zone(f"{name}:{area}") == (name.strip().title(), area)


@given(st.text() | st.none())
def test_moisture_average_fuzz(value):
    try:
        result = moisture_average(value)
    except ValueError:
        return
    assert isinstance(result, int) and 0 <= result <= 100


@given(st.lists(st.integers(min_value=0, max_value=100), min_size=1))
def test_moisture_average_valid(readings):
    assert moisture_average(",".join(map(str, readings))) == sum(readings) // len(readings)


@given(st.text() | st.none())
def test_water_needed_fuzz(value):
    try:
        result = water_needed(value)
    except ValueError:
        return
    assert math.isfinite(result) and result >= 0


@given(st.floats(min_value=0, max_value=1e6, allow_nan=False),
       st.floats(min_value=0, max_value=1e6, allow_nan=False))
def test_water_needed_valid(area, rain):
    assert water_needed(f"{area}|{rain}") == max(area * 5 - rain, 0)


@pytest.mark.parametrize("value", ["", "north", "north:0", "north:-2", "north:nan", None])
def test_parse_zone_rejects_invalid(value):
    with pytest.raises(ValueError):
        parse_zone(value)


@pytest.mark.parametrize("value", ["", "1,,2", "-1,20", "101", None])
def test_moisture_average_rejects_invalid(value):
    with pytest.raises(ValueError):
        moisture_average(value)


@pytest.mark.parametrize("value", ["", "1", "-1|2", "1|-2", "nan|2", None])
def test_water_needed_rejects_invalid(value):
    with pytest.raises(ValueError):
        water_needed(value)
