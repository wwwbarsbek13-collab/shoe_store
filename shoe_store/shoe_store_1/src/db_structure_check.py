import sqlite3
from pathlib import Path

DB = Path(__file__).parent.parent / "db" / "shoe_store.sqlite"

def get_connection():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def get_tables(conn):
    return [r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")]

def get_columns(conn, table):
    return [dict(r) for r in conn.execute(f"PRAGMA table_info({table})")]

def get_foreign_keys(conn, table):
    return [dict(r) for r in conn.execute(f"PRAGMA foreign_key_list({table})")]

def get_indexes(conn, table):
    return [dict(r) for r in conn.execute(f"PRAGMA index_list({table})")]

def check_database():
    conn = get_connection()
    expected = {"roles","sizes","users","products","stock_items","orders","order_items"}
    actual = set(get_tables(conn))
    print(f"Таблиц найдено: {len(actual)}")
    print(f"Отсутствуют: {expected - actual}")
    print(f"Лишние: {actual - expected}")
    for t in sorted(actual):
        cols = get_columns(conn, t)
        fks = get_foreign_keys(conn, t)
        idxs = get_indexes(conn, t)
        print(f"\n{t}: полей {len(cols)}, FK {len(fks)}, индексов {len(idxs)}")
        for c in cols:
            print(f"  - {c['name']} ({c['type']}) PK={c['pk']} NN={c['notnull']}")
    conn.close()

if __name__ == "__main__":
    check_database()