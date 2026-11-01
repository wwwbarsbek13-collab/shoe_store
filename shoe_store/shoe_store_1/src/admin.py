import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "shoe_store.sqlite"

PERMISSIONS = {
    "admin_db": ["SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "DROP"],
    "developer": ["SELECT", "INSERT", "UPDATE"],
    "reader": ["SELECT"]
}

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def check_permission(conn, user_id, action):
    """Проверяет, разрешено ли пользователю действие."""
    cursor = conn.cursor()

    cursor.execute("""
        SELECT r.role_name FROM users u
        JOIN roles r ON u.role_id = r.role_id
        WHERE u.user_id = ?
    """, (user_id,))
    row = cursor.fetchone()
    if not row:
        return False
    role = row[0]
    
    allowed = PERMISSIONS.get(role, [])
    return action in allowed

def add_admin_roles(conn):
    """Добавляет три новые роли для администраторов."""
    cursor = conn.cursor()
    roles = ["admin_db", "developer", "reader"]
    for role in roles:
        cursor.execute("INSERT OR IGNORE INTO roles (role_name) VALUES (?)", (role,))
    conn.commit()
    print("Роли admin_db, developer, reader добавлены (или уже существуют).")

if __name__ == "__main__":
    conn = get_connection()
    add_admin_roles(conn)
    
    print("\n=== Тест прав ===")
    print(f"admin (DELETE): {check_permission(conn, 1, 'DELETE')}")
    print(f"reader (DELETE): {check_permission(conn, 3, 'DELETE')}")
    print(f"reader (SELECT): {check_permission(conn, 3, 'SELECT')}")
    conn.close()