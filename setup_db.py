import sqlite3
import os
import json

DB_PATH = os.path.join(os.path.dirname(__file__), "wardrobe.db")
WARDROBE_JSON_PATH = os.path.join(os.path.dirname(__file__), "data", "wardrobe.json")

# Mapping realistic fallback images for the 17 core wardrobe items
DEFAULT_ITEM_IMAGES = {
    1: "/uploads/image-1781761852201-370707935_processed.png",
    2: "/uploads/image-1781761852201-370707935_processed.png",
    3: "/uploads/image-1781760502836-295940226_processed.png",
    4: "/uploads/image-1781760502836-295940226_processed.png",
    5: "/uploads/image-1781761417975-998202756_processed.png",
    6: "/uploads/image-1781760502836-295940226_processed.png",
    7: "/uploads/image-1784919260477-715049820_processed.png",
    8: "/uploads/image-1782494474069-846865506_processed.png",
    9: "/uploads/image-1783318778779-958279157_processed.png",
    10: "/uploads/image-1784919403308-597048030_processed.png",
    11: "/uploads/image-1784919403308-597048030_processed.png",
    12: "/uploads/image-1791046494660-396972332_processed.png",
    13: "/uploads/image-1781847240303-824307617_processed.png",
    14: "/uploads/image-1783318479020-124496457_processed.png",
    15: "/uploads/image-1783182762512-113271116_processed.png",
    16: "/uploads/image-1783318434976-184123174_processed.png",
    17: "/uploads/image-1783318434976-184123174_processed.png"
}

def init_wardrobe_db():
    """Initializes and migrates the SQLite database with TEXT primary keys, metadata, images, and user sync."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='wardrobe'")
    exists = cursor.fetchone()

    need_migration = False
    if exists:
        # Check id column type
        cursor.execute("PRAGMA table_info(wardrobe)")
        cols = cursor.fetchall()
        id_col = next((c for c in cols if c[1] == 'id'), None)
        if id_col and 'INT' in id_col[2].upper():
            need_migration = True

    if not exists or need_migration:
        print("[SetupDB] Migrating wardrobe table schema to TEXT id and full metadata columns...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS wardrobe_v2 (
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

        if exists:
            # Copy existing legacy rows into v2
            cursor.execute("PRAGMA table_info(wardrobe)")
            legacy_cols = [c[1] for c in cursor.fetchall()]
            common_cols = [c for c in ['name', 'category', 'color', 'season', 'formality', 'temp_min_c', 'temp_max_c'] if c in legacy_cols]
            col_list = ", ".join(common_cols)
            cursor.execute(f"SELECT id, {col_list} FROM wardrobe")
            rows = cursor.fetchall()
            for r in rows:
                row_id = str(r[0])
                num_id = int(r[0]) if row_id.isdigit() else 0
                img_url = DEFAULT_ITEM_IMAGES.get(num_id, "")
                cursor.execute(f"""
                    INSERT OR REPLACE INTO wardrobe_v2 (id, {col_list}, img, original_image_path, processed_image_path)
                    VALUES (?, {', '.join(['?']*len(common_cols))}, ?, ?, ?)
                """, (row_id, *r[1:], img_url, img_url, img_url))

            cursor.execute("DROP TABLE wardrobe")

        cursor.execute("ALTER TABLE wardrobe_v2 RENAME TO wardrobe")
        conn.commit()

    # Check if table has seed data
    cursor.execute("SELECT COUNT(*) FROM wardrobe")
    count = cursor.fetchone()[0]

    if count == 0:
        sample_items = [
            ("1", "Navy Blue Wool Trench Coat", "outerwear", "navy", "winter", "formal", -5.0, 15.0, "demo@threadtheory.io", DEFAULT_ITEM_IMAGES[1]),
            ("2", "Black Heavy Puffer Jacket", "outerwear", "black", "winter", "casual", -10.0, 10.0, "demo@threadtheory.io", DEFAULT_ITEM_IMAGES[2]),
            ("3", "Beige Lightweight Windbreaker", "outerwear", "beige", "spring", "casual", 10.0, 22.0, "demo@threadtheory.io", DEFAULT_ITEM_IMAGES[3]),
            ("4", "Dark Grey Tailored Suit Jacket", "outerwear", "grey", "all-season", "formal", 12.0, 24.0, "demo@threadtheory.io", DEFAULT_ITEM_IMAGES[4]),
            ("5", "White Oxford Cotton Shirt", "top", "white", "all-season", "smart casual", 10.0, 30.0, "demo@threadtheory.io", DEFAULT_ITEM_IMAGES[5]),
            ("6", "Charcoal Cashmere Sweater", "top", "charcoal", "winter", "smart casual", 0.0, 16.0, "demo@threadtheory.io", DEFAULT_ITEM_IMAGES[6]),
            ("7", "Graphic Vintage Tee", "top", "black", "summer", "casual", 18.0, 35.0, "demo@threadtheory.io", DEFAULT_ITEM_IMAGES[7]),
            ("8", "Linen Short Sleeve Shirt", "top", "sky blue", "summer", "casual", 22.0, 38.0, "demo@threadtheory.io", DEFAULT_ITEM_IMAGES[8]),
            ("9", "Dark Wash Slim Jeans", "bottom", "dark denim", "all-season", "casual", 5.0, 28.0, "demo@threadtheory.io", DEFAULT_ITEM_IMAGES[9]),
            ("10", "Beige Chino Pants", "bottom", "beige", "all-season", "smart casual", 10.0, 30.0, "demo@threadtheory.io", DEFAULT_ITEM_IMAGES[10]),
            ("11", "Black Tailored Dress Trousers", "bottom", "black", "all-season", "formal", 10.0, 26.0, "demo@threadtheory.io", DEFAULT_ITEM_IMAGES[11]),
            ("12", "Linen Blend Shorts", "bottom", "khaki", "summer", "casual", 20.0, 38.0, "demo@threadtheory.io", DEFAULT_ITEM_IMAGES[12]),
            ("13", "Brown Leather Chelsea Boots", "shoes", "brown", "winter", "smart casual", -5.0, 20.0, "demo@threadtheory.io", DEFAULT_ITEM_IMAGES[13]),
            ("14", "Minimalist White Leather Sneakers", "shoes", "white", "all-season", "casual", 5.0, 30.0, "demo@threadtheory.io", DEFAULT_ITEM_IMAGES[14]),
            ("15", "Black Oxfords Leather Shoes", "shoes", "black", "all-season", "formal", 10.0, 30.0, "demo@threadtheory.io", DEFAULT_ITEM_IMAGES[15]),
            ("16", "Wool Ribbed Scarf", "accessory", "grey", "winter", "casual", -10.0, 12.0, "demo@threadtheory.io", DEFAULT_ITEM_IMAGES[16]),
            ("17", "UV Protection Sunglasses", "accessory", "black", "summer", "casual", 15.0, 40.0, "demo@threadtheory.io", DEFAULT_ITEM_IMAGES[17])
        ]

        cursor.executemany("""
            INSERT INTO wardrobe (id, name, category, color, season, formality, temp_min_c, temp_max_c, owner, img, original_image_path, processed_image_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9], item[9], item[9]) for item in sample_items])
        conn.commit()
        print(f"Database initialized successfully with {len(sample_items)} clothing items at '{DB_PATH}'.")

    # Ensure all core items have images
    for nid, img_url in DEFAULT_ITEM_IMAGES.items():
        cursor.execute("UPDATE wardrobe SET img = ?, original_image_path = ?, processed_image_path = ? WHERE id = ? AND (img IS NULL OR img = '')", (img_url, img_url, img_url, str(nid)))
    conn.commit()
    conn.close()

    # Synchronize items from data/wardrobe.json
    try:
        from tools.wardrobe import sync_from_json
        sync_from_json()
    except Exception as e:
        print("[SetupDB] Sync from JSON skipped:", e)

if __name__ == "__main__":
    init_wardrobe_db()
