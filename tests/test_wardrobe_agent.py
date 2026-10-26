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
    from unittest.mock import patch, MagicMock

    query = "Do I have any space suits or astronaut helmets?"
    print(f"[TEST 4] Query: '{query}'...")

    # Mock LLM tool call and empty DB return to deterministically verify empty result branch
    mock_msg = MagicMock()
    mock_msg.tool_calls = [{
        "name": "fetch_wardrobe_inventory",
        "args": {"category": "accessory"}
    }]
    mock_llm_instance = MagicMock()
    mock_llm_instance.invoke.return_value = mock_msg

    with patch("agents.wardrobe_agent.create_wardrobe_llm", return_value=mock_llm_instance), \
         patch("agents.wardrobe_agent.get_wardrobe_items", return_value=[]):
        res = run_wardrobe_agent(query)
        print("  ✓ Items Found:", len(res["wardrobe_items"]))
        print("  ✓ Agent Honest Response:", res["agent_response"])
        assert len(res["wardrobe_items"]) == 0
        assert len(res["agent_response"]) > 0
        assert "no items matching" in res["agent_response"].lower()
        print("  -> TEST 4 PASSED PERFECTLY!\n")


def test_wardrobe_agent_explicit_empty_preloaded():
    """Regression test: preloaded_items=[] must return empty inventory without querying DB or LLM."""
    from unittest.mock import patch

    with patch("agents.wardrobe_agent.create_wardrobe_llm") as mock_llm, \
         patch("agents.wardrobe_agent.get_wardrobe_items") as mock_db:
        res = run_wardrobe_agent("cocktail party in Vadodara", weather_data={"temperature": 25.0}, preloaded_items=[])
        assert res["wardrobe_items"] == [], "Explicitly empty preloaded items must return empty wardrobe_items"
        assert "no clothing items" in res["agent_response"].lower()
        mock_llm.assert_not_called()
        mock_db.assert_not_called()

    # Also verify non-empty preloaded items are returned without querying DB or LLM
    mock_item = {"id": "custom_1", "name": "Custom Linen Shirt", "category": "top", "temp_min_c": 10.0, "temp_max_c": 35.0}
    with patch("agents.wardrobe_agent.create_wardrobe_llm") as mock_llm, \
         patch("agents.wardrobe_agent.get_wardrobe_items") as mock_db:
        res = run_wardrobe_agent("what tops do I have?", weather_data={"temperature": 25.0}, preloaded_items=[mock_item])
        assert len(res["wardrobe_items"]) == 1
        assert res["wardrobe_items"][0]["id"] == "custom_1"
        mock_llm.assert_not_called()
        mock_db.assert_not_called()


if __name__ == "__main__":
    print("==================================================")
    print("      ThreadTheory Phase 5 - Wardrobe Agent Test  ")
    print("==================================================\n")

    test_wardrobe_agent_general()
    test_wardrobe_agent_category_filter()
    test_wardrobe_agent_formality_filter()
    test_wardrobe_agent_empty_result()
    test_wardrobe_agent_explicit_empty_preloaded()

    print("🎉 ALL WARDROBE AGENT TESTS COMPLETED SUCCESSFULLY!")
