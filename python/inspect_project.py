import sqlite3
import pandas as pd
from pathlib import Path

DATA_DIR = Path("../data")
DB_PATH = DATA_DIR / "inventory.db"

# ============================================================
# 1. INSPECT SQLITE DATABASE
# ============================================================

print("\n" + "=" * 60)
print("DATABASE INSPECTION")
print("=" * 60)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    ORDER BY name;
""")

tables = [row[0] for row in cursor.fetchall()]

print(f"\nTables found: {len(tables)}")

for table in tables:
    print(f"\n--- Table: {table} ---")

    cursor.execute(f'PRAGMA table_info("{table}")')
    columns = cursor.fetchall()

    for column in columns:
        print(f"  {column[1]} | {column[2]}")

    cursor.execute(f'SELECT COUNT(*) FROM "{table}"')
    count = cursor.fetchone()[0]

    print(f"Rows: {count:,}")

conn.close()


# ============================================================
# 2. INSPECT CSV FILES
# ============================================================

print("\n" + "=" * 60)
print("CSV FILE INSPECTION")
print("=" * 60)

csv_files = sorted(DATA_DIR.glob("*.csv"))

for file in csv_files:

    print(f"\n--- {file.name} ---")

    try:
        df = pd.read_csv(file)

        print(f"Rows: {len(df):,}")
        print(f"Columns: {len(df.columns)}")

        print("Columns:")
        for column in df.columns:
            print(f"  - {column}")

        print("\nFirst 2 rows:")
        print(df.head(2).to_string(index=False))

    except Exception as e:
        print(f"Could not read file: {e}")


print("\n" + "=" * 60)
print("INSPECTION COMPLETED")
print("=" * 60)