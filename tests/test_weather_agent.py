"""Standalone test script for the Weather Agent (Phase 4).

Tests the Weather Agent and its LLM tool-calling logic independently.
"""

import sys
import os
from dotenv import load_dotenv

# Ensure root project directory is in python path & load .env explicitly
ENV_PATH = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=ENV_PATH)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.weather_agent import run_weather_agent


def test_weather_agent():
    """Test running Weather Agent with natural language city prompt."""
    query = "Check the current weather in Vadodara for today."
    print(f"[TEST] Executing Weather Agent query: '{query}'...")

    try:
        output = run_weather_agent(query)
        print("  ✓ Agent Output Received:")
        print("    Weather Data:", output.get("weather_data"))
        print("    Agent Summary:", output.get("agent_response"))

        assert "weather_data" in output
        assert "city" in output["weather_data"]
        assert output["weather_data"]["city"] == "Vadodara"
        assert "temperature" in output["weather_data"]
        assert "agent_response" in output

        print("  -> WEATHER AGENT TEST PASSED PERFECTLY!\n")
    except Exception as e:
        print(f"  ✗ Weather Agent Test Failed: {e}\n")
        raise e


if __name__ == "__main__":
    print("==================================================")
    print("       ThreadTheory Phase 4 - Weather Agent Test   ")
    print("==================================================\n")

    test_weather_agent()

    print("🎉 WEATHER AGENT TEST COMPLETED SUCCESSFULLY!")
