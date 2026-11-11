"""Replay the completed fuzz tests against the assigned buggy starter."""

import test_processor as tests
import original_processor as original
from test_processor import *  # noqa: F401,F403

tests.parse_zone = original.parse_zone
tests.moisture_average = original.moisture_average
tests.water_needed = original.water_needed
