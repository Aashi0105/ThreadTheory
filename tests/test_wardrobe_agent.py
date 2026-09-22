"""Standalone test script for the Wardrobe Agent (Phase 5).

Tests the Wardrobe Agent and its LLM tool-calling logic independently without LangGraph.
"""

import sys
import os
from dotenv import load_dotenv

# Ensure root project directory is in python path & load .env explicitly
ENV_PATH = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=ENV_PATH)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.wardrobe_agent import run_wardrobe_agent


def test_wardrobe_agent_general():
    """Test general wardrobe query."""
    query = "What clothes do I have in my closet?"
    print(f"[TEST 1] Query: '{query}'...")
    res = run_wardrobe_agent(query)
    print("  ✓ Wardrobe Items Count:", len(res["wardrobe_items"]))
    print("  ✓ Summary:\n", res["agent_response"])
    assert len(res["wardrobe_items"]) > 0
    assert "agent_response" in res
    print("  -> TEST 1 PASSED PERFECTLY!\n")


def test_wardrobe_agent_category_filter():
    """Test category specific query."""
    query = "Show my tops."
    print(f"[TEST 2] Query: '{query}'...")
    res = run_wardrobe_agent(query)
    print("  ✓ Tops Found:", len(res["wardrobe_items"]))
    assert len(res["wardrobe_items"]) > 0
    for item in res["wardrobe_items"]:
        assert item["category"].lower() == "top"
    print("  -> TEST 2 PASSED PERFECTLY!\n")


def test_wardrobe_agent_formality_filter():
    """Test formality specific query."""
    query = "Show my formal clothing options."
    print(f"[TEST 3] Query: '{query}'...")
    res = run_wardrobe_agent(query)
    print("  ✓ Formal Items Found:", len(res["wardrobe_items"]))
    assert len(res["wardrobe_items"]) > 0
    for item in res["wardrobe_items"]:
        assert item["formality"].lower() == "formal"
    print("  -> TEST 3 PASSED PERFECTLY!\n")


def test_wardrobe_agent_empty_result():
    """Test handling query with no matching items."""
    query = "Do I have any space suits or astronaut helmets?"
    print(f"[TEST 4] Query: '{query}'...")
    res = run_wardrobe_agent(query)
    print("  ✓ Items Found:", len(res["wardrobe_items"]))
    print("  ✓ Agent Honest Response:", res["agent_response"])
    assert len(res["wardrobe_items"]) == 0
    assert len(res["agent_response"]) > 0
    print("  -> TEST 4 PASSED PERFECTLY!\n")


if __name__ == "__main__":
    print("==================================================")
    print("      ThreadTheory Phase 5 - Wardrobe Agent Test  ")
    print("==================================================\n")

    test_wardrobe_agent_general()
    test_wardrobe_agent_category_filter()
    test_wardrobe_agent_formality_filter()
    test_wardrobe_agent_empty_result()

    print("🎉 ALL WARDROBE AGENT TESTS COMPLETED SUCCESSFULLY!")
