import sqlite3
import os

DB_PATH = "children.db"

# ✅ Create database and table
def initialize_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Create table if not exists
    c.execute('''
    CREATE TABLE IF NOT EXISTS missing_children (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        image_path TEXT UNIQUE
    )
    ''')

    conn.commit()
    conn.close()

# ✅ Insert data only if not already present
def insert_sample_data():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Check if data exists
    c.execute("SELECT COUNT(*) FROM missing_children")
    count = c.fetchone()[0]

    if count == 0:  # Only insert if the table is empty
        children_data = [
            ("bala, age 8", 8, "database-records/missing child1.jpg"),
            ("mani, age 9", 10, "database-records/missing child2.jpg"),
            ("neha, age 10", 9, "database-records/missing child3.jpg"),
        ]
        c.executemany("INSERT INTO missing_children (name, age, image_path) VALUES (?, ?, ?)", children_data)
        conn.commit()

    conn.close()

# ✅ Initialize database on first run
initialize_db()
insert_sample_data()
