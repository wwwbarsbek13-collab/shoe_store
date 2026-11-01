import sqlite3
import shutil
import os
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "shoe_store.sqlite"
BACKUP_DIR = Path(__file__).parent.parent / "db" / "backups"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def backup_simple():
    """Бэкап через shutil."""
    BACKUP_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
    backup_path = BACKUP_DIR / f"backup_{timestamp}.sqlite"
    shutil.copy2(DB_PATH, backup_path)
    print(f"Бэкап (shutil) создан: {backup_path}")
    return backup_path

def backup_safe():
    """Бэкап через sqlite3.backup()."""
    BACKUP_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
    backup_path = BACKUP_DIR / f"backup_safe_{timestamp}.sqlite"
    
    source = sqlite3.connect(DB_PATH)
    dest = sqlite3.connect(backup_path)
    source.backup(dest)
    source.close()
    dest.close()
    print(f"Бэкап (safe) создан: {backup_path}")
    return backup_path

def check_integrity(conn):
    """Проверка целостности через PRAGMA."""
    cursor = conn.cursor()
    cursor.execute("PRAGMA integrity_check")
    result = cursor.fetchone()
    if result and result[0] == "ok":
        print("Целостность базы: OK")
        return True
    else:
        print(f"Ошибка целостности: {result}")
        return False

def get_db_stats(conn):
    """Сбор статистики."""
    cursor = conn.cursor()
    cursor.execute("PRAGMA page_size")
    page_size = cursor.fetchone()[0]
    cursor.execute("PRAGMA page_count")
    page_count = cursor.fetchone()[0]
    total_size = page_size * page_count
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = [row[0] for row in cursor.fetchall()]
    
    print(f"\nСтатистика базы:")
    print(f"  Размер страницы: {page_size} байт")
    print(f"  Количество страниц: {page_count}")
    print(f"  Общий размер: {total_size} байт")
    print(f"  Таблицы: {', '.join(tables)}")
    return {"page_size": page_size, "page_count": page_count, "total_size": total_size, "tables": tables}

if __name__ == "__main__":
    conn = get_connection()
    check_integrity(conn)
    backup_simple()
    backup_safe()
    get_db_stats(conn)
    conn.close()