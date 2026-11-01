import sqlite3

conn = sqlite3.connect("db/cinema.sqlite")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
tables = cursor.fetchall()

for table in tables:
    table_name = table[0]
    print(f"\n--- Таблица: {table_name} ---")
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    for col in columns:
        # col: (cid, name, type, notnull, dflt_value, pk)
        print(f"  {col[1]} ({col[2]}) — PK: {'Да' if col[5] else 'Нет'}, NOT NULL: {'Да' if col[3] else 'Нет'}")

conn.close()