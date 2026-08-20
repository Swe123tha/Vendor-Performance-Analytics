import sqlite3
from pathlib import Path

DB_PATH = Path("../data/inventory.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Get all tables
cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    ORDER BY name;
""")

tables = cursor.fetchall()

print("\n=== TABLES IN DATABASE ===")

for table in tables:
    table_name = table[0]
    print(f"\nTable: {table_name}")

    cursor.execute(f"PRAGMA table_info('{table_name}')")
    columns = cursor.fetchall()

    print("Columns:")
    for column in columns:
        print(f"  - {column[1]} ({column[2]})")

conn.close()

print("\nDatabase inspection completed.")