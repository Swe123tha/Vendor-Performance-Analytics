import sqlite3
from pathlib import Path

DB_PATH = Path("../data/inventory.db")
SQL_PATH = Path("../sql/01_vendor_analysis.sql")

conn = sqlite3.connect(DB_PATH)

with open(SQL_PATH, "r", encoding="utf-8") as file:
    sql_script = file.read()

try:
    conn.executescript(sql_script)
    print("SQL analysis executed successfully!")
except Exception as e:
    print("SQL Error:")
    print(e)

conn.close()