import sqlite3

conn = sqlite3.connect("db/cinema.sqlite")
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute("INSERT INTO roles (role_name) VALUES ('Клиент');")
cursor.execute("INSERT INTO genres (genre_name) VALUES ('Боевик');")
cursor.execute("INSERT INTO halls (hall_name, rows_count, seats_per_row) VALUES ('Зал 1', 10, 10);")
cursor.execute("INSERT INTO movies (title, genre_id, duration_minutes, age_rating) VALUES ('Фильм 1', 1, 120, '16+');")
cursor.execute("INSERT INTO clients (full_name, email, role_id) VALUES ('Иванов И.И.', 'ivanov@mail.ru', 1);")
cursor.execute("INSERT INTO sessions (movie_id, hall_id, start_datetime, base_price) VALUES (1, 1, '2024-01-01 12:00:00', 500);")
cursor.execute("INSERT INTO tickets (session_id, client_id, row_number, seat_number, final_price) VALUES (1, 1, 5, 5, 500);")
conn.commit()
print("Тестовые данные добавлены.")

tests = [
    ("Уникальность email", "INSERT INTO clients (full_name, email, role_id) VALUES ('Петров П.П.', 'ivanov@mail.ru', 1);"),
    ("Внешний ключ (сеанс)", "INSERT INTO tickets (session_id, client_id, row_number, seat_number, final_price) VALUES (99, 1, 1, 1, 500);"),
    ("CHECK цена > 0", "INSERT INTO tickets (session_id, client_id, row_number, seat_number, final_price) VALUES (1, 1, 1, 1, -100);"),
    ("CHECK место > 0", "INSERT INTO tickets (session_id, client_id, row_number, seat_number, final_price) VALUES (1, 1, 1, -1, 500);"),
    ("RESTRICT удаление фильма", "DELETE FROM movies WHERE movie_id = 1;"),
]

for name, sql in tests:
    try:
        cursor.execute(sql)
        conn.commit()
        print(f"[FAIL] {name}: ошибка не возникла.")
    except sqlite3.Error as e:
        print(f"[OK] {name}: {e}")

cursor.execute("DELETE FROM sessions WHERE session_id = 1;")
conn.commit()
cursor.execute("SELECT COUNT(*) FROM tickets WHERE session_id = 1;")
count = cursor.fetchone()[0]
print(f"[CASCADE] Билетов после удаления сеанса: {count} (ожидалось 0)")

conn.close()