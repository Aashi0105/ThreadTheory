"""Wardrobe tool module for ThreadTheory Multi-Agent Stylist.

Queries the SQLite database ('wardrobe.db') to fetch available clothing items,
filtering by category, formality, temperature range, and user ownership.
"""

import sqlite3
import os
import json
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "wardrobe.db")
WARDROBE_JSON_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "wardrobe.json")


def _ensure_schema(conn: sqlite3.Connection):
    """Ensures wardrobe table exists with all required metadata and image columns."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wardrobe (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            color TEXT NOT NULL,
            season TEXT NOT NULL,
            formality TEXT NOT NULL,
            temp_min_c REAL NOT NULL,
            temp_max_c REAL NOT NULL,
            owner TEXT,
            img TEXT,
            original_image_path TEXT,
            processed_image_path TEXT,
            subcategory TEXT,
            occasion TEXT
        );
    """)

    # Check and add missing columns if upgrading legacy table
    cursor.execute("PRAGMA table_info(wardrobe)")
    existing_cols = {row[1] for row in cursor.fetchall()}
    needed_cols = {
        "owner": "TEXT",
        "img": "TEXT",
        "original_image_path": "TEXT",
        "processed_image_path": "TEXT",
        "subcategory": "TEXT",
        "occasion": "TEXT"
    }
    for col, col_type in needed_cols.items():
        if col not in existing_cols:
            cursor.execute(f"ALTER TABLE wardrobe ADD COLUMN {col} {col_type}")
    conn.commit()


def get_wardrobe_items(
    category: Optional[str] = None,
    formality: Optional[str] = None,
    max_temp_c: Optional[float] = None,
    owner: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Queries the SQLite wardrobe database for available clothing items with optional filters.

    Args:
        category: Optional category filter (e.g., "top", "bottom", "outerwear", "shoes", "accessory").
        formality: Optional formality filter (e.g., "casual", "smart casual", "formal").
        max_temp_c: Optional temperature in °C to filter items comfortable for current weather.
        owner: Optional user email to filter items belonging strictly to this user.

    Returns:
        List of dictionaries containing clothing item attributes.
    """
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database file '{DB_PATH}' not found. Please run 'python setup_db.py'.")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    _ensure_schema(conn)
    cursor = conn.cursor()

    query = """
        SELECT id, name, category, color, season, formality, temp_min_c, temp_max_c,
               owner, img, original_image_path, processed_image_path, subcategory, occasion
        FROM wardrobe WHERE 1=1
    """
    params: List[Any] = []

    if owner and owner.strip():
        # Match user's own items strictly to preserve user isolation
        query += " AND LOWER(owner) = LOWER(?)"
        params.append(owner.strip())

    if category and category.strip():
        # Normalize category matching (e.g. "top" matches "top", "tops", "tops & blouses")
        cat = category.strip().lower()
        if cat in ("top", "tops"):
            query += " AND (LOWER(category) LIKE '%top%' OR LOWER(category) LIKE '%knitwear%' OR LOWER(category) LIKE '%shirt%')"
        elif cat in ("bottom", "bottoms", "pants"):
            query += " AND (LOWER(category) LIKE '%bottom%' OR LOWER(category) LIKE '%pant%' OR LOWER(category) LIKE '%jean%' OR LOWER(category) LIKE '%short%' OR LOWER(category) LIKE '%skirt%')"
        elif cat in ("dress", "dresses", "one-piece", "one_piece", "jumpsuit", "romper"):
            query += " AND (LOWER(category) LIKE '%dress%' OR LOWER(category) LIKE '%jumpsuit%' OR LOWER(category) LIKE '%romper%' OR LOWER(category) LIKE '%one-piece%')"
        elif cat in ("shoes", "footwear"):
            query += " AND (LOWER(category) LIKE '%shoe%' OR LOWER(category) LIKE '%footwear%' OR LOWER(category) LIKE '%boot%' OR LOWER(category) LIKE '%sneaker%' OR LOWER(category) LIKE '%heel%')"
        elif cat in ("outerwear", "jacket", "coat"):
            query += " AND (LOWER(category) LIKE '%outerwear%' OR LOWER(category) LIKE '%jacket%' OR LOWER(category) LIKE '%coat%')"
        elif cat in ("accessory", "accessories"):
            query += " AND (LOWER(category) LIKE '%accessor%' OR LOWER(category) LIKE '%scarf%' OR LOWER(category) LIKE '%sunglass%')"
        else:
            query += " AND LOWER(category) = LOWER(?)"
            params.append(cat)

    if formality and formality.strip():
        query += " AND LOWER(formality) = LOWER(?)"
        params.append(formality.strip())

    if max_temp_c is not None:
        query += " AND (temp_min_c <= ? AND temp_max_c >= ? OR (? >= 28 AND temp_max_c >= 25))"
        params.extend([max_temp_c, max_temp_c, max_temp_c])

    query += " ORDER BY category, name"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    items = [dict(row) for row in rows]
    return items


def get_wardrobe_item_by_id(item_id: Any, owner: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Fetches a single verified wardrobe item by its unique ID with optional user ownership enforcement."""
    if not os.path.exists(DB_PATH):
        return None

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    _ensure_schema(conn)
    cursor = conn.cursor()

    if owner and str(owner).strip():
        cursor.execute("""
            SELECT id, name, category, color, season, formality, temp_min_c, temp_max_c,
                   owner, img, original_image_path, processed_image_path, subcategory, occasion
            FROM wardrobe WHERE (id = ? OR CAST(id AS TEXT) = ?) AND LOWER(owner) = LOWER(?)
        """, (str(item_id), str(item_id), str(owner).strip()))
    else:
        cursor.execute("""
            SELECT id, name, category, color, season, formality, temp_min_c, temp_max_c,
                   owner, img, original_image_path, processed_image_path, subcategory, occasion
            FROM wardrobe WHERE id = ? OR CAST(id AS TEXT) = ?
        """, (str(item_id), str(item_id)))
    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else None


def add_wardrobe_item(
    name: str,
    category: str,
    color: str = "custom",
    season: str = "all-season",
    formality: str = "casual",
    temp_min_c: float = 10.0,
    temp_max_c: float = 30.0,
    item_id: Optional[str] = None,
    owner: Optional[str] = None,
    img: Optional[str] = None,
    original_image_path: Optional[str] = None,
    processed_image_path: Optional[str] = None,
    subcategory: str = "",
    occasion: str = ""
) -> str:
    """Inserts or replaces a clothing item in SQLite wardrobe.db."""
    conn = sqlite3.connect(DB_PATH)
    _ensure_schema(conn)
    cursor = conn.cursor()

    final_id = str(item_id) if item_id else f"item_{int(cursor.execute('SELECT COUNT(*) FROM wardrobe').fetchone()[0]) + 1}"

    cursor.execute("""
        INSERT OR REPLACE INTO wardrobe (
            id, name, category, color, season, formality, temp_min_c, temp_max_c,
            owner, img, original_image_path, processed_image_path, subcategory, occasion
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        final_id, name, category, color, season, formality, temp_min_c, temp_max_c,
        owner, img, original_image_path, processed_image_path, subcategory, occasion
    ))
    conn.commit()
    conn.close()
    print(f"[WardrobeDB] Saved item '{name}' (id={final_id}, category={category}, owner={owner})")
    return final_id


def delete_wardrobe_item(item_id: str, owner: Optional[str] = None) -> bool:
    """Deletes an item from SQLite wardrobe.db."""
    if not os.path.exists(DB_PATH):
        return False
    conn = sqlite3.connect(DB_PATH)
    _ensure_schema(conn)
    cursor = conn.cursor()
    if owner:
        cursor.execute("DELETE FROM wardrobe WHERE (id = ? OR CAST(id AS TEXT) = ?) AND LOWER(owner) = LOWER(?)", (str(item_id), str(item_id), owner))
    else:
        cursor.execute("DELETE FROM wardrobe WHERE id = ? OR CAST(id AS TEXT) = ?", (str(item_id), str(item_id)))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted


def sync_from_json(json_path: Optional[str] = None):
    """Synchronizes all wardrobe items from data/wardrobe.json into wardrobe.db."""
    target_path = json_path or WARDROBE_JSON_PATH
    if not os.path.exists(target_path):
        return
    try:
        with open(target_path, "r", encoding="utf-8") as f:
            items = json.load(f)
        if not isinstance(items, list):
            return

        for item in items:
            raw_cat = item.get("category", "Tops")
            # Map categories to standard roles
            role_cat = raw_cat
            rc_lower = raw_cat.lower()
            if "top" in rc_lower or "knitwear" in rc_lower:
                role_cat = "top"
            elif "bottom" in rc_lower or "pant" in rc_lower:
                role_cat = "bottom"
            elif "shoe" in rc_lower or "footwear" in rc_lower:
                role_cat = "shoes"
            elif "outerwear" in rc_lower:
                role_cat = "outerwear"
            elif "dress" in rc_lower:
                role_cat = "dress"
            elif "accessor" in rc_lower:
                role_cat = "accessory"

            color = item.get("dominantColor") or item.get("color") or "custom"
            add_wardrobe_item(
                item_id=str(item.get("id")),
                name=item.get("name", "Clothing Item"),
                category=role_cat,
                color=color,
                season=item.get("season", "all-season"),
                formality=item.get("formality", ""),
                temp_min_c=float(item.get("temp_min_c", 10.0)),
                temp_max_c=float(item.get("temp_max_c", 30.0)),
                owner=item.get("owner", ""),
                img=item.get("img") or item.get("processedImagePath") or item.get("originalImagePath"),
                original_image_path=item.get("originalImagePath"),
                processed_image_path=item.get("processedImagePath"),
                subcategory=item.get("subcategory", ""),
                occasion=item.get("occasion", "")
            )
        print(f"[WardrobeDB] Synchronized {len(items)} items from '{target_path}' into SQLite wardrobe.db.")
    except Exception as e:
        print(f"[WardrobeDB Sync Warning] Could not sync wardrobe.json: {e}")

