import sqlite3, re, os

DB = os.path.join(os.path.dirname(__file__), '..', 'db', 'shoe_store.sqlite')
RESERVED = {'select','from','where','order','group','by','table','index','column','insert','update','delete','drop','create','alter','join','on','as','and','or','not','null','primary','foreign','key','check','unique','default'}

def get_connection():
    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def get_tables(conn):
    cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    return [r[0] for r in cur.fetchall()]

def get_columns(conn, table):
    cur = conn.execute(f"PRAGMA table_info({table})")
    return [r[1] for r in cur.fetchall()]

def check_name(name):
    errors = []
    if not re.match(r'^[a-z]', name):
        errors.append("должно начинаться со строчной латинской буквы")
    if not re.match(r'^[a-z0-9_]+$', name):
        errors.append("только строчные латинские, цифры, _")
    if name in RESERVED:
        errors.append("зарезервированное слово SQL")
    return errors

def check_database():
    conn = get_connection()
    report = []
    for t in get_tables(conn):
        e = check_name(t)
        report.append((t, 'таблица', e))
        for c in get_columns(conn, t):
            e = check_name(c)
            report.append((c, 'поле', e))
    conn.close()
    return report

if __name__ == "__main__":
    for name, kind, errs in check_database():
        status = "OK" if not errs else "ОШИБКА: " + "; ".join(errs)
        print(f"{kind:8} {name:20} {status}")