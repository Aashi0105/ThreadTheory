"""Automated Verification Suite for Phase 2:
Covers all 12 test cases outlined in Phase 9, plus live integration and ownership validation.
"""

import sys
import os
import requests
import pytest
from dotenv import load_dotenv

ENV_PATH = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=ENV_PATH)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api import parse_outfit_from_text
from tools.wardrobe import get_wardrobe_items, get_wardrobe_item_by_id
from agents.stylist_agent import run_stylist_agent
from graph import app_graph


def test_1_dress_plus_shorts_compatibility():
    """TEST 1: If top is a dress/one-piece, bottom must be rejected / None."""
    mock_wardrobe = [
        {"id": "d1", "name": "Floral Summer Dress", "category": "dress", "color": "yellow"},
        {"id": "s1", "name": "Yellow Denim Shorts", "category": "bottom", "color": "yellow"},
        {"id": "sh1", "name": "White Canvas Sneakers", "category": "shoes", "color": "white"}
    ]
    raw_ai_text = (
        "### 👔 Recommended Outfit\n"
        "- **Top:** Floral Summer Dress\n"
        "- **Bottom:** Yellow Denim Shorts\n"
        "- **Shoes:** White Canvas Sneakers\n"
    )
    parsed = parse_outfit_from_text(raw_ai_text, mock_wardrobe)
    assert parsed["top"] is not None
    assert parsed["top"]["id"] == "d1"
    # One-piece rule: bottom MUST be None
    assert parsed["bottom"] is None, "Dress + Shorts combination was not rejected!"
    assert parsed["shoes"]["id"] == "sh1"


def test_2_top_plus_one_bottom_shoes():
    """TEST 2: Top + Jeans + Skirt + Shoes -> Exactly one bottom."""
    mock_wardrobe = [
        {"id": "t1", "name": "Classic White Tee", "category": "top"},
        {"id": "b1", "name": "Blue Jeans", "category": "bottom"},
        {"id": "b2", "name": "Pleated Skirt", "category": "bottom"},
        {"id": "sh1", "name": "Sneakers", "category": "shoes"}
    ]
    raw_ai_text = (
        "### 👔 Recommended Outfit\n"
        "- **Top:** Classic White Tee\n"
        "- **Bottom:** Blue Jeans\n"
        "- **Shoes:** Sneakers\n"
    )
    parsed = parse_outfit_from_text(raw_ai_text, mock_wardrobe)
    assert parsed["top"]["id"] == "t1"
    assert parsed["bottom"]["id"] == "b1"
    assert parsed["shoes"]["id"] == "sh1"


def test_3_jumpsuit_compatibility():
    """TEST 3: Jumpsuit + Top + Jeans + Shoes -> Jumpsuit + Shoes (no bottom)."""
    mock_wardrobe = [
        {"id": "j1", "name": "Navy Linen Jumpsuit", "category": "jumpsuit"},
        {"id": "b1", "name": "Blue Jeans", "category": "bottom"},
        {"id": "sh1", "name": "Loafers", "category": "shoes"}
    ]
    raw_ai_text = (
        "### 👔 Recommended Outfit\n"
        "- **Top:** Navy Linen Jumpsuit\n"
        "- **Bottom:** Blue Jeans\n"
        "- **Shoes:** Loafers\n"
    )
    parsed = parse_outfit_from_text(raw_ai_text, mock_wardrobe)
    assert parsed["top"]["id"] == "j1"
    assert parsed["bottom"] is None, "Jumpsuit should not be paired with bottoms!"
    assert parsed["shoes"]["id"] == "sh1"


def test_4_dress_plus_jacket_plus_shoes():
    """TEST 4: Dress + Jacket + Shoes is a valid coordinate."""
    mock_wardrobe = [
        {"id": "d1", "name": "Satin Slip Dress", "category": "dress"},
        {"id": "o1", "name": "Oversized Leather Jacket", "category": "outerwear"},
        {"id": "sh1", "name": "Ankle Boots", "category": "shoes"}
    ]
    raw_ai_text = (
        "### 👔 Recommended Outfit\n"
        "- **Top:** Satin Slip Dress\n"
        "- **Bottom:** None\n"
        "- **Outerwear:** Oversized Leather Jacket\n"
        "- **Shoes:** Ankle Boots\n"
    )
    parsed = parse_outfit_from_text(raw_ai_text, mock_wardrobe)
    assert parsed["top"]["id"] == "d1"
    assert parsed["bottom"] is None
    assert parsed["outerwear"]["id"] == "o1"
    assert parsed["shoes"]["id"] == "sh1"


def test_5_top_bottom_outerwear_shoes():
    """TEST 5: Standard four-piece coordinate."""
    mock_wardrobe = [
        {"id": "t1", "name": "Oxford Shirt", "category": "top"},
        {"id": "b1", "name": "Chino Trousers", "category": "bottom"},
        {"id": "o1", "name": "Wool Trench Coat", "category": "outerwear"},
        {"id": "sh1", "name": "Chelsea Boots", "category": "shoes"}
    ]
    raw_ai_text = (
        "### 👔 Recommended Outfit\n"
        "- **Top:** Oxford Shirt\n"
        "- **Bottom:** Chino Trousers\n"
        "- **Outerwear:** Wool Trench Coat\n"
        "- **Shoes:** Chelsea Boots\n"
    )
    parsed = parse_outfit_from_text(raw_ai_text, mock_wardrobe)
    assert parsed["top"]["id"] == "t1"
    assert parsed["bottom"]["id"] == "b1"
    assert parsed["outerwear"]["id"] == "o1"
    assert parsed["shoes"]["id"] == "sh1"


def test_6_empty_wardrobe_graceful():
    """TEST 6: Empty wardrobe must not infinite loop and returns graceful message."""
    output = run_stylist_agent("cocktail party", {"city": "Vadodara", "temperature": 25.0}, [])
    resp = (output.get("agent_response") or output.get("stylist_response") or "").lower()
    assert "no suitable outfit" in resp or "wardrobe" in resp or "none available" in resp

    # Verify graph does not loop infinitely with empty wardrobe
    state = {
        "user_prompt": "cocktail party",
        "weather_data": {"city": "Vadodara", "temperature": 25.0},
        "wardrobe_items": [],
        "stylist_response": None,
        "recommended_outfit": None,
        "execution_trace": []
    }
    result = app_graph.invoke(state)
    assert result["wardrobe_items"] == []
    assert "none available" in result["final_response"].lower() or "no clothing items" in result["final_response"].lower()


def test_7_user_a_isolation():
    """TEST 7: User A queries return only User A items."""
    # dhwani@gmail.com has 4 specific items in data/wardrobe.json
    items_dhwani = get_wardrobe_items(owner="dhwani@gmail.com")
    for item in items_dhwani:
        assert item["owner"].lower() == "dhwani@gmail.com"


def test_8_user_b_isolation():
    """TEST 8: User B queries return only User B items."""
    items_demo = get_wardrobe_items(owner="demo@threadtheory.io")
    for item in items_demo:
        assert item["owner"].lower() == "demo@threadtheory.io"


def test_9_ai_returns_invalid_id():
    """TEST 9: AI returns an ID not existing in user's wardrobe -> Rejected."""
    mock_wardrobe = [
        {"id": "item_123", "name": "Real Top", "category": "top"}
    ]
    raw_ai_text = (
        "### 👔 Recommended Outfit\n"
        "- **Top:** item_99999\n"
        "- **Bottom:** None\n"
    )
    parsed = parse_outfit_from_text(raw_ai_text, mock_wardrobe)
    assert parsed["top"] is None, "Nonexistent item ID was not rejected!"


def test_10_ai_returns_other_users_valid_id():
    """TEST 10: AI attempts to use User B's item ID for User A -> Rejected."""
    user_a_wardrobe = [
        {"id": "a_1", "name": "User A Tee", "category": "top", "owner": "user_a@test.com"}
    ]
    raw_ai_text = (
        "### 👔 Recommended Outfit\n"
        "- **Top:** b_1\n"
        "- **Bottom:** None\n"
    )
    parsed = parse_outfit_from_text(raw_ai_text, user_a_wardrobe, user_email="user_a@test.com")
    assert parsed["top"] is None, "Cross-user item was not rejected!"


def test_11_image_integrity_preserved():
    """TEST 11: Exact item image is preserved without replacement."""
    mock_wardrobe = [
        {
            "id": "t1",
            "name": "Silk Blouse",
            "category": "top",
            "img": "/uploads/exact_silk_blouse.png",
            "processedImagePath": "/uploads/exact_silk_blouse_clean.png"
        }
    ]
    raw_ai_text = (
        "### 👔 Recommended Outfit\n"
        "- **Top:** Silk Blouse\n"
        "- **Bottom:** None\n"
    )
    parsed = parse_outfit_from_text(raw_ai_text, mock_wardrobe)
    assert parsed["top"]["img"] == "/uploads/exact_silk_blouse_clean.png"
    assert parsed["top"]["processedImagePath"] == "/uploads/exact_silk_blouse_clean.png"


def test_12_no_silent_unrelated_substitution():
    """TEST 12: Missing image does not invent a random demo photo URL."""
    mock_wardrobe = [
        {
            "id": "t1",
            "name": "Grey Heather Hoodie",
            "category": "top",
            "img": "",
            "processedImagePath": ""
        }
    ]
    raw_ai_text = (
        "### 👔 Recommended Outfit\n"
        "- **Top:** Grey Heather Hoodie\n"
        "- **Bottom:** None\n"
    )
    parsed = parse_outfit_from_text(raw_ai_text, mock_wardrobe)
    assert parsed["top"]["img"] == ""


def test_13_formality_mapping_data_integrity():
    """TEST 13: Stored SQLite formality must reflect actual formality, not occasion."""
    import sqlite3
    from tools.wardrobe import add_wardrobe_item, delete_wardrobe_item, DB_PATH

    test_id = "test_formality_item_999"
    try:
        # Add item with occasion="Party" but formality="formal"
        add_wardrobe_item(
            item_id=test_id,
            name="Formal Dinner Blazer",
            category="outerwear",
            color="black",
            season="all-season",
            formality="formal",
            temp_min_c=10.0,
            temp_max_c=25.0,
            owner="test@test.com",
            occasion="Party"
        )

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT formality, occasion FROM wardrobe WHERE id = ?", (test_id,))
        row = cursor.fetchone()
        conn.close()

        assert row is not None, "Item was not inserted into wardrobe.db"
        stored_formality, stored_occasion = row
        assert stored_formality == "formal", "Expected formality 'formal', got " + str(stored_formality)
        assert stored_occasion == "Party", "Expected occasion 'Party', got " + str(stored_occasion)
        assert stored_formality != stored_occasion, "Formality was improperly overwritten with occasion!"
    finally:
        delete_wardrobe_item(test_id)


def test_14_formality_recommendation_and_persistence_integrity():
    """TEST 14: Verifies occasion does NOT overwrite formality in persistence or recommendation metadata.

    Input:
        occasion = 'Party'
        formality = 'Casual'
    Expected persisted data:
        occasion = 'Party'
        formality = 'Casual'
    Expected recommendation metadata:
        occasion = 'Party'
        formality = 'Casual'
    Fails if formality becomes 'Party'.
    """
    # 1. Recommendation metadata verification via parse_outfit_from_text
    mock_wardrobe = [
        {
            "id": "item_party_casual_1",
            "name": "Party Silk Shirt",
            "category": "top",
            "color": "black",
            "season": "all-season",
            "formality": "Casual",
            "occasion": "Party",
            "img": "/uploads/party_shirt.png"
        }
    ]
    raw_ai_text = (
        "### 👔 Recommended Outfit\n"
        "- **Top:** Party Silk Shirt\n"
        "- **Bottom:** None\n"
        "- **Outerwear:** None\n"
        "- **Shoes:** None\n"
    )
    parsed = parse_outfit_from_text(raw_ai_text, mock_wardrobe)
    assert parsed["top"] is not None
    assert parsed["top"]["formality"] == "Casual", f"Expected formality 'Casual', got {parsed['top']['formality']}"
    assert parsed["top"]["occasion"] == "Party", f"Expected occasion 'Party', got {parsed['top']['occasion']}"
    assert parsed["top"]["formality"] != "Party", "Formality was improperly overwritten with occasion 'Party'!"

    # 2. Wardrobe persistence data integrity
    import sqlite3
    from tools.wardrobe import add_wardrobe_item, delete_wardrobe_item, DB_PATH

    test_id = "test_persistence_formality_001"
    try:
        add_wardrobe_item(
            item_id=test_id,
            name="Party Silk Shirt",
            category="top",
            color="black",
            season="all-season",
            formality="Casual",
            temp_min_c=15.0,
            temp_max_c=30.0,
            owner="audit@threadtheory.io",
            occasion="Party"
        )

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT formality, occasion FROM wardrobe WHERE id = ?", (test_id,))
        row = cursor.fetchone()
        conn.close()

        assert row is not None, "Item was not inserted into wardrobe.db"
        persisted_formality, persisted_occasion = row
        assert persisted_formality == "Casual", f"Expected persisted formality 'Casual', got {persisted_formality}"
        assert persisted_occasion == "Party", f"Expected persisted occasion 'Party', got {persisted_occasion}"
        assert persisted_formality != "Party", "Persisted formality was improperly set to occasion 'Party'!"
    finally:
        delete_wardrobe_item(test_id)

