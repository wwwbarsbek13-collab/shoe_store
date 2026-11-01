import sqlite3
from pathlib import Path

DB = Path(__file__).parent.parent / "db" / "shoe_store.sqlite"

def get_connection():
    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def run(sql, params=()):
    conn = get_connection()
    try:
        conn.execute(sql, params)
        conn.commit()
        return "ОШИБКА: вставка прошла"
    except sqlite3.IntegrityError as e:
        return f"OK: {e}"
    finally:
        conn.close()

if __name__ == "__main__":
    # Подготовка
    conn = get_connection()
    conn.execute("INSERT OR IGNORE INTO roles (role_name) VALUES ('администратор')")
    conn.execute("INSERT OR IGNORE INTO roles (role_name) VALUES ('менеджер')")
    conn.execute("INSERT OR IGNORE INTO users (last_name, first_name, login, role_id) VALUES ('Иванов','Иван','admin',1)")
    conn.commit()
    conn.close()

    print("UNIQUE login:", run("INSERT INTO users (last_name,first_name,login,role_id) VALUES ('A','B','admin',1)"))
    print("NOT NULL last_name:", run("INSERT INTO users (first_name,login,role_id) VALUES ('Иван','user2',1)"))
    print("CHECK price:", run("INSERT INTO products (category,manufacturer,product_name,price) VALUES ('X','Y','Z',-100)"))
    print("CHECK quantity:", run("INSERT INTO stock_items (product_id,size_id,quantity_available) VALUES (1,1,-5)"))
    print("FK role_id:", run("INSERT INTO users (last_name,first_name,login,role_id) VALUES ('A','B','sid',999)"))
    print("RESTRICT:", run("DELETE FROM roles WHERE role_id=1"))