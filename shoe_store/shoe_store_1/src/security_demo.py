import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "shoe_store.sqlite"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# Уязвимая функция (f-строка)
def vulnerable_login(conn, login):
    """Уязвимый запрос через f-строку."""
    cursor = conn.cursor()
    # ВНИМАНИЕ! Это опасно!
    sql = f"SELECT * FROM users WHERE login = '{login}'"
    print(f"Выполняется запрос: {sql}")
    cursor.execute(sql)
    return cursor.fetchall()

# Безопасная функция (параметризация)
def secure_login(conn, login):
    """Безопасный запрос через параметризацию."""
    cursor = conn.cursor()
    sql = "SELECT * FROM users WHERE login = ?"
    cursor.execute(sql, (login,))
    return cursor.fetchall()

if __name__ == "__main__":
    conn = get_connection()
    
    print("=== 1. Демонстрация SQL-инъекции (уязвимый код) ===")
    # Обычный логин
    print("\nВход с нормальным логином 'admin':")
    rows = vulnerable_login(conn, "admin")
    print(f"Найдено пользователей: {len(rows)}")
    
    # SQL-инъекция
    print("\nВход с вредоносным логином \"' OR '1'='1\":")
    rows = vulnerable_login(conn, "' OR '1'='1")
    print(f"Найдено пользователей: {len(rows)} (все пользователи! Это взлом)")
    
    print("\n=== 2. Защита (параметризованный запрос) ===")
    # Обычный логин
    print("\nВход с нормальным логином 'admin':")
    rows = secure_login(conn, "admin")
    print(f"Найдено пользователей: {len(rows)}")
    
    # SQL-инъекция
    print("\nВход с вредоносным логином \"' OR '1'='1\":")
    rows = secure_login(conn, "' OR '1'='1")
    print(f"Найдено пользователей: {len(rows)} (инъекция не сработала!)")
    
    conn.close()