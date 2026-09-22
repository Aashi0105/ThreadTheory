"""Standalone test script for LangGraph Multi-Agent Routing (Phase 7).

Tests the Supervisor routing and full state machine flow:
Supervisor -> Weather Agent -> Supervisor -> Wardrobe Agent -> Supervisor -> Stylist Agent -> FINISH
"""

import sys
import os
from dotenv import load_dotenv

# Ensure root project directory is in python path & load .env explicitly
ENV_PATH = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=ENV_PATH)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from graph import app_graph, AgentState


def test_full_langgraph_routing():
    """Test full multi-agent orchestration via LangGraph."""
    user_prompt = "What should I wear for a smart casual meeting in Vadodara today?"
    
    initial_state: AgentState = {
        "user_prompt": user_prompt,
        "next_agent": "",
        "weather_data": {},
        "wardrobe_items": [],
        "execution_trace": [],
        "final_response": ""
    }

    print("==================================================")
    print("   ThreadTheory Phase 7 - LangGraph Graph Test    ")
    print("==================================================\n")
    print(f"Starting Graph Execution for Query: '{user_prompt}'\n")

    final_state = app_graph.invoke(initial_state)

    print("\n==================================================")
    print("            GRAPH EXECUTION COMPLETE              ")
    print("==================================================\n")

    print("📍 Execution Trace:")
    for idx, step in enumerate(final_state.get("execution_trace", []), 1):
        print(f"  {idx}. {step}")

    print("\n🌤️ Weather Data Captured:", final_state.get("weather_data"))
    print("👔 Wardrobe Items Captured Count:", len(final_state.get("wardrobe_items", [])))

    print("\n👗 Final Stylist Response:\n")
    print(final_state.get("final_response"))

    # Assertions
    assert len(final_state.get("weather_data", {})) > 0, "Weather data must be captured"
    assert len(final_state.get("wardrobe_items", [])) > 0, "Wardrobe items must be captured"
    assert len(final_state.get("final_response", "")) > 0, "Final response must be generated"
    assert "FINISH" in "".join(final_state.get("execution_trace", [])), "Graph must reach FINISH"

    print("\n🎉 LANGGRAPH ROUTING TEST PASSED PERFECTLY!")


if __name__ == "__main__":
    test_full_langgraph_routing()
