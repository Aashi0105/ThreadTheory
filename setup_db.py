import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "wardrobe.db")

def init_wardrobe_db():
    """Initializes the SQLite database with wardrobe table and sample clothing items."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wardrobe (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            color TEXT NOT NULL,
            season TEXT NOT NULL,
            formality TEXT NOT NULL,
            temp_min_c REAL NOT NULL,
            temp_max_c REAL NOT NULL
        );
    """)

    # Check if table already has data
    cursor.execute("SELECT COUNT(*) FROM wardrobe")
    count = cursor.fetchone()[0]

    if count == 0:
        sample_items = [
            ("Navy Blue Wool Trench Coat", "outerwear", "navy", "winter", "formal", -5.0, 15.0),
            ("Black Heavy Puffer Jacket", "outerwear", "black", "winter", "casual", -10.0, 10.0),
            ("Beige Lightweight Windbreaker", "outerwear", "beige", "spring", "casual", 10.0, 22.0),
            ("Dark Grey Tailored Suit Jacket", "outerwear", "grey", "all-season", "formal", 12.0, 24.0),
            ("White Oxford Cotton Shirt", "top", "white", "all-season", "smart casual", 10.0, 30.0),
            ("Charcoal Cashmere Sweater", "top", "charcoal", "winter", "smart casual", 0.0, 16.0),
            ("Graphic Vintage Tee", "top", "black", "summer", "casual", 18.0, 35.0),
            ("Linen Short Sleeve Shirt", "top", "sky blue", "summer", "casual", 22.0, 38.0),
            ("Dark Wash Slim Jeans", "bottom", "dark denim", "all-season", "casual", 5.0, 28.0),
            ("Beige Chino Pants", "bottom", "beige", "all-season", "smart casual", 10.0, 30.0),
            ("Black Tailored Dress Trousers", "bottom", "black", "all-season", "formal", 10.0, 26.0),
            ("Linen Blend Shorts", "bottom", "khaki", "summer", "casual", 20.0, 38.0),
            ("Brown Leather Chelsea Boots", "shoes", "brown", "winter", "smart casual", -5.0, 20.0),
            ("Minimalist White Leather Sneakers", "shoes", "white", "all-season", "casual", 5.0, 30.0),
            ("Black Oxfords Leather Shoes", "shoes", "black", "all-season", "formal", 10.0, 30.0),
            ("Wool Ribbed Scarf", "accessory", "grey", "winter", "casual", -10.0, 12.0),
            ("UV Protection Sunglasses", "accessory", "black", "summer", "casual", 15.0, 40.0)
        ]

        cursor.executemany("""
            INSERT INTO wardrobe (name, category, color, season, formality, temp_min_c, temp_max_c)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, sample_items)
        conn.commit()
        print(f"Database initialized successfully with {len(sample_items)} clothing items at '{DB_PATH}'.")
    else:
        print(f"Database already contains {count} items at '{DB_PATH}'. Skipping seed.")

    conn.close()

if __name__ == "__main__":
    init_wardrobe_db()
