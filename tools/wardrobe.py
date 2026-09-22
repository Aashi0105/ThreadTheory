"""Wardrobe tool module for ThreadTheory Multi-Agent Stylist.

Queries the SQLite database ('wardrobe.db') to fetch available clothing items,
filtering by category, formality, and temperature range.
"""

import sqlite3
import os
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "wardrobe.db")


def get_wardrobe_items(
    category: Optional[str] = None,
    formality: Optional[str] = None,
    max_temp_c: Optional[float] = None
) -> List[Dict[str, Any]]:
    """Queries the SQLite wardrobe database for available clothing items with optional filters.

    Args:
        category: Optional category filter (e.g., "top", "bottom", "outerwear", "shoes", "accessory").
        formality: Optional formality filter (e.g., "casual", "smart casual", "formal").
        max_temp_c: Optional temperature in °C to filter items comfortable for current weather.

    Returns:
        List of dictionaries containing clothing item attributes.

    Raises:
        FileNotFoundError: If wardrobe.db does not exist.
        sqlite3.Error: On database query errors.
    """
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database file '{DB_PATH}' not found. Please run 'python setup_db.py'.")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enables column access by name
    cursor = conn.cursor()

    query = "SELECT id, name, category, color, season, formality, temp_min_c, temp_max_c FROM wardrobe WHERE 1=1"
    params: List[Any] = []

    if category and category.strip():
        query += " AND LOWER(category) = LOWER(?)"
        params.append(category.strip())

    if formality and formality.strip():
        query += " AND LOWER(formality) = LOWER(?)"
        params.append(formality.strip())

    if max_temp_c is not None:
        query += " AND temp_min_c <= ? AND temp_max_c >= ?"
        params.extend([max_temp_c, max_temp_c])

    query += " ORDER BY category, name"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    items = [dict(row) for row in rows]
    return items


def add_wardrobe_item(
    name: str,
    category: str,
    color: str = "custom",
    season: str = "all-season",
    formality: str = "casual",
    temp_min_c: float = 10.0,
    temp_max_c: float = 30.0
) -> int:
    """Inserts a new clothing item into SQLite wardrobe.db."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO wardrobe (name, category, color, season, formality, temp_min_c, temp_max_c)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, category, color, season, formality, temp_min_c, temp_max_c))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    print(f"[WardrobeDB] Inserted item '{name}' (id={new_id}, category={category}, temp={temp_min_c}°C to {temp_max_c}°C)")
    return new_id

