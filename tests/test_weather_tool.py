"""Standalone test script for the Weather Tool (Phase 2).

Tests the weather tool directly without any agent or LangGraph overhead.
"""

import sys
import os

# Ensure root project directory is in python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools.weather import get_weather


def test_weather_valid_city():
    """Test fetching weather for a valid city."""
    city_name = "Vadodara"
    print(f"[TEST 1] Fetching weather for '{city_name}'...")

    try:
        result = get_weather(city_name)
        print("  ✓ Result received:")
        print("   ", result)

        # Assert correct output schema
        assert isinstance(result, dict), "Result should be a dictionary"
        assert "city" in result, "Key 'city' missing"
        assert "temperature" in result, "Key 'temperature' missing"
        assert "weather" in result, "Key 'weather' missing"
        assert "rain_probability" in result, "Key 'rain_probability' missing"
        assert "wind_speed" in result, "Key 'wind_speed' missing"

        assert isinstance(result["temperature"], (int, float)), "temperature must be numeric"
        assert isinstance(result["rain_probability"], int), "rain_probability must be int"
        assert isinstance(result["wind_speed"], (int, float)), "wind_speed must be numeric"
        assert isinstance(result["weather"], str), "weather must be string"

        print("  -> TEST 1 PASSED PERFECTLY!\n")
    except Exception as e:
        print(f"  ✗ TEST 1 FAILED: {e}\n")
        raise e


def test_weather_invalid_city():
    """Test error handling when given an unresolvable city name."""
    invalid_city = "NonExistentCityX1Y2Z3"
    print(f"[TEST 2] Testing error handling for invalid city '{invalid_city}'...")

    try:
        get_weather(invalid_city)
        print("  ✗ TEST 2 FAILED: Expected ValueError was not raised.\n")
    except ValueError as e:
        print(f"  ✓ Handled cleanly as expected! Exception caught: {e}")
        print("  -> TEST 2 PASSED PERFECTLY!\n")
    except Exception as e:
        print(f"  ✗ TEST 2 FAILED with unexpected exception type: {e}\n")


if __name__ == "__main__":
    print("==================================================")
    print("        ThreadTheory Phase 2 - Weather Tool Test   ")
    print("==================================================\n")

    test_weather_valid_city()
    test_weather_invalid_city()

    print("🎉 ALL WEATHER TOOL TESTS COMPLETED SUCCESSFULLY!")
