import sqlite3
import os

def create_database():
    os.makedirs("db", exist_ok=True)
    
    conn = sqlite3.connect("db/cinema.sqlite")
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS roles (
        role_id INTEGER PRIMARY KEY AUTOINCREMENT,
        role_name TEXT NOT NULL UNIQUE
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS genres (
        genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
        genre_name TEXT NOT NULL UNIQUE
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS halls (
        hall_id INTEGER PRIMARY KEY AUTOINCREMENT,
        hall_name TEXT NOT NULL UNIQUE,
        rows_count INTEGER NOT NULL CHECK(rows_count > 0),
        seats_per_row INTEGER NOT NULL CHECK(seats_per_row > 0)
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        genre_id INTEGER NOT NULL,
        duration_minutes INTEGER NOT NULL CHECK(duration_minutes > 0),
        age_rating TEXT NOT NULL,
        poster_url TEXT,
        FOREIGN KEY (genre_id) REFERENCES genres(genre_id) ON DELETE RESTRICT
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        client_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        phone TEXT,
        role_id INTEGER NOT NULL,
        FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE RESTRICT
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        session_id INTEGER PRIMARY KEY AUTOINCREMENT,
        movie_id INTEGER NOT NULL,
        hall_id INTEGER NOT NULL,
        start_datetime TEXT NOT NULL,
        base_price REAL NOT NULL CHECK(base_price > 0),
        FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE RESTRICT,
        FOREIGN KEY (hall_id) REFERENCES halls(hall_id) ON DELETE RESTRICT
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER NOT NULL,
        client_id INTEGER NOT NULL,
        row_number INTEGER NOT NULL CHECK(row_number > 0),
        seat_number INTEGER NOT NULL CHECK(seat_number > 0),
        final_price REAL NOT NULL CHECK(final_price > 0),
        FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE,
        FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE RESTRICT,
        UNIQUE(session_id, row_number, seat_number)
    );
    """)
    
    conn.commit()
    conn.close()
    print("База данных cinema.sqlite успешно создана.")

if __name__ == "__main__":
    create_database()