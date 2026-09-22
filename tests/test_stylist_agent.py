"""Standalone test script for the Stylist Agent (Phase 6).

Tests the Stylist Agent and its reasoning capabilities over combined weather and wardrobe data.
"""

import sys
import os
from dotenv import load_dotenv

# Ensure root project directory is in python path & load .env explicitly
ENV_PATH = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=ENV_PATH)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.stylist_agent import run_stylist_agent


def test_stylist_agent_reasoning():
    """Test Stylist Agent reasoning over weather and wardrobe context."""
    user_prompt = "I have a smart casual client meeting in Vadodara today."
    
    mock_weather = {
        "city": "Vadodara",
        "temperature": 26.2,
        "weather": "Light Drizzle",
        "rain_probability": 100,
        "wind_speed": 16.1
    }

    mock_wardrobe = [
        {"id": 5, "name": "White Oxford Cotton Shirt", "category": "top", "color": "white", "formality": "smart casual", "temp_min_c": 10.0, "temp_max_c": 30.0},
        {"id": 10, "name": "Beige Chino Pants", "category": "bottom", "color": "beige", "formality": "smart casual", "temp_min_c": 10.0, "temp_max_c": 30.0},
        {"id": 3, "name": "Beige Lightweight Windbreaker", "category": "outerwear", "color": "beige", "formality": "casual", "temp_min_c": 10.0, "temp_max_c": 22.0},
        {"id": 13, "name": "Brown Leather Chelsea Boots", "category": "shoes", "color": "brown", "formality": "smart casual", "temp_min_c": -5.0, "temp_max_c": 20.0},
        {"id": 14, "name": "Minimalist White Leather Sneakers", "category": "shoes", "color": "white", "formality": "casual", "temp_min_c": 5.0, "temp_max_c": 30.0}
    ]

    print(f"[TEST] Running Stylist Agent for query: '{user_prompt}'...")
    output = run_stylist_agent(user_prompt, mock_weather, mock_wardrobe)
    
    print("  ✓ Stylist Recommendation Output:\n")
    print(output.get("agent_response"))

    assert "agent_response" in output
    assert len(output["agent_response"]) > 0
    assert "Recommended Outfit" in output["agent_response"] or "Top:" in output["agent_response"]

    print("\n  -> STYLIST AGENT TEST PASSED PERFECTLY!\n")


if __name__ == "__main__":
    print("==================================================")
    print("       ThreadTheory Phase 6 - Stylist Agent Test   ")
    print("==================================================\n")

    test_stylist_agent_reasoning()

    print("🎉 STYLIST AGENT TEST COMPLETED SUCCESSFULLY!")
