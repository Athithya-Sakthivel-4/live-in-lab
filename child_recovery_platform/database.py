import sqlite3

# Connect to the database
conn = sqlite3.connect('children.db')
c = conn.cursor()

# Create the missing_children table if it doesn't exist
c.execute('''
CREATE TABLE IF NOT EXISTS missing_children (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    image_path TEXT
)
''')

# Insert sample missing children (Update file paths accordingly)
children_data = [
    ("bala", 8, "/workspaces/live-in-lab/child_recovery_platform/database-records/missing child1.jpg"),
    ("mani", 10, "/workspaces/live-in-lab/child_recovery_platform/database-records/missing child2.jpg"),
    ("neha", 9, "/workspaces/live-in-lab/child_recovery_platform/database-records/missing child3.jpg"),
]

for child in children_data:
    c.execute("INSERT INTO missing_children (name, age, image_path) VALUES (?, ?, ?)", child)

conn.commit()
conn.close()

print("✅ Missing children added to the database!")
