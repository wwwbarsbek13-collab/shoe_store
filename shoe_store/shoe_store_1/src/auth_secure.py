import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / "db" / "shoe_store.sqlite"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def hash_password(password):
    """Хэширование пароля через SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def add_password_hash_column(conn):
    """Добавляет поле password_hash в таблицу users, если его нет."""
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN password_hash TEXT")
        conn.commit()
        print("Поле password_hash добавлено.")
    except sqlite3.OperationalError:
        print("Поле password_hash уже существует.")

def create_login_audit_table(conn):
    """Создает таблицу аудита входов."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS login_audit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL,
            status TEXT NOT NULL,
            login_time TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    print("Таблица login_audit создана (или уже существует).")

def register_user(conn, login, password):
    """Регистрация пользователя с хэшированием пароля."""
    cursor = conn.cursor()
    hashed = hash_password(password)
    try:
        cursor.execute("""
            INSERT INTO users (last_name, first_name, login, password_hash, role_id)
            VALUES ('Новый', 'Пользователь', ?, ?, 3)
        """, (login, hashed))
        conn.commit()
        print(f"Пользователь {login} зарегистрирован.")
        return True
    except sqlite3.IntegrityError:
        print(f"Ошибка: логин {login} уже существует.")
        return False

def check_password(conn, login, password):
    """Безопасная проверка пароля с логированием."""
    cursor = conn.cursor()
    # Получаем хэш из базы
    cursor.execute("SELECT password_hash FROM users WHERE login = ?", (login,))
    row = cursor.fetchone()
    
    if not row:
        # Логируем неудачу
        cursor.execute("INSERT INTO login_audit (login, status) VALUES (?, ?)", (login, "отказ (нет пользователя)"))
        conn.commit()
        return False
    
    stored_hash = row[0]
    input_hash = hash_password(password)
    
    if stored_hash == input_hash:
        cursor.execute("INSERT INTO login_audit (login, status) VALUES (?, ?)", (login, "успех"))
        conn.commit()
        return True
    else:
        cursor.execute("INSERT INTO login_audit (login, status) VALUES (?, ?)", (login, "отказ (неверный пароль)"))
        conn.commit()
        return False

if __name__ == "__main__":
    conn = get_connection()
    
    # Подготовка
    add_password_hash_column(conn)
    create_login_audit_table(conn)
    
    # Регистрация
    print("\n=== Регистрация ===")
    register_user(conn, "test_user", "admin123")
    
    # Проверка пароля
    print("\n=== Проверка пароля ===")
    print(f"Вход с правильным паролем: {check_password(conn, 'test_user', 'admin123')}")
    print(f"Вход с неправильным паролем: {check_password(conn, 'test_user', 'wrongpass')}")
    
    # Просмотр аудита
    print("\n=== Аудит входов ===")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM login_audit")
    for row in cursor.fetchall():
        print(row)
    
    conn.close()