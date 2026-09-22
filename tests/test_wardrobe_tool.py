"""Standalone test script for the Wardrobe Tool (Phase 3).

Tests querying the SQLite database directly without any agent or LangGraph overhead.
"""

import sys
import os

# Ensure root project directory is in python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools.wardrobe import get_wardrobe_items


def test_get_all_wardrobe_items():
    """Test fetching all wardrobe items without filters."""
    print("[TEST 1] Fetching all wardrobe items...")
    items = get_wardrobe_items()
    print(f"  ✓ Received {len(items)} items from database.")
    assert len(items) > 0, "Wardrobe should not be empty."
    
    first_item = items[0]
    print("  ✓ Sample item:", first_item)
    assert "id" in first_item
    assert "name" in first_item
    assert "category" in first_item
    assert "temp_min_c" in first_item
    print("  -> TEST 1 PASSED PERFECTLY!\n")


def test_filter_by_category_and_temp():
    """Test filtering items by category ('top') and temperature (26°C)."""
    print("[TEST 2] Fetching 'top' items suitable for 26°C weather...")
    tops = get_wardrobe_items(category="top", max_temp_c=26.0)
    print(f"  ✓ Found {len(tops)} matching tops:")
    for top in tops:
        print(f"    - {top['name']} ({top['color']}, {top['formality']}) [{top['temp_min_c']}°C to {top['temp_max_c']}°C]")
    
    assert len(tops) > 0, "Should find at least one top for 26°C"
    for top in tops:
        assert top["category"].lower() == "top"
        assert top["temp_min_c"] <= 26.0 <= top["temp_max_c"]
    
    print("  -> TEST 2 PASSED PERFECTLY!\n")


def test_filter_by_formality():
    """Test filtering items by formality ('formal')."""
    print("[TEST 3] Fetching 'formal' attire...")
    formal_items = get_wardrobe_items(formality="formal")
    print(f"  ✓ Found {len(formal_items)} formal items:")
    for item in formal_items:
        print(f"    - {item['name']} ({item['category']}, {item['color']})")
    
    assert len(formal_items) > 0, "Should find formal items"
    for item in formal_items:
        assert item["formality"].lower() == "formal"
    
    print("  -> TEST 3 PASSED PERFECTLY!\n")


if __name__ == "__main__":
    print("==================================================")
    print("       ThreadTheory Phase 3 - Wardrobe Tool Test   ")
    print("==================================================\n")

    test_get_all_wardrobe_items()
    test_filter_by_category_and_temp()
    test_filter_by_formality()

    print("🎉 ALL WARDROBE TOOL TESTS COMPLETED SUCCESSFULLY!")
