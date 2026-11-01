import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "shoe_store.sqlite"


def get_connection():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def drop_all_tables():
    conn = get_connection()
    tables = ["order_items", "orders", "stock_items", "products", "users", "sizes", "roles"]
    for t in tables:
        conn.execute(f"DROP TABLE IF EXISTS {t}")
    conn.commit()
    conn.close()


def create_tables():
    conn = get_connection()
    c = conn.cursor()

    # 1. roles
    c.execute("""CREATE TABLE IF NOT EXISTS roles (
        role_id INTEGER PRIMARY KEY AUTOINCREMENT,
        role_name TEXT NOT NULL UNIQUE
    )""")

    # 2. sizes
    c.execute("""CREATE TABLE IF NOT EXISTS sizes (
        size_id INTEGER PRIMARY KEY AUTOINCREMENT,
        size_value REAL NOT NULL UNIQUE
            CHECK (size_value > 20 AND size_value < 50)
    )""")

    # 3. users
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        last_name TEXT NOT NULL,
        first_name TEXT NOT NULL,
        middle_name TEXT,
        login TEXT NOT NULL UNIQUE
            CHECK (length(login) >= 3 AND length(login) <= 20),
        role_id INTEGER NOT NULL,
        FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE RESTRICT
    )""")

    # 4. products
    c.execute("""CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        subcategory TEXT,
        manufacturer TEXT NOT NULL,
        product_name TEXT NOT NULL CHECK (length(product_name) > 0),
        image_path TEXT,
        composition TEXT,
        description TEXT,
        price REAL NOT NULL CHECK (price > 0 AND price < 1000000)
    )""")

    # 5. stock_items
    c.execute("""CREATE TABLE IF NOT EXISTS stock_items (
        stock_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        size_id INTEGER NOT NULL,
        quantity_available INTEGER NOT NULL DEFAULT 0
            CHECK (quantity_available >= 0),
        FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE RESTRICT,
        FOREIGN KEY (size_id) REFERENCES sizes(size_id) ON DELETE RESTRICT
    )""")

    # 6. orders
    c.execute("""CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_date TEXT NOT NULL DEFAULT CURRENT_DATE,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT
    )""")

    # 7. order_items
    c.execute("""CREATE TABLE IF NOT EXISTS order_items (
        order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        stock_item_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL CHECK (quantity > 0),
        price REAL NOT NULL CHECK (price > 0),
        FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
        FOREIGN KEY (stock_item_id) REFERENCES stock_items(stock_item_id) ON DELETE RESTRICT
    )""")

    # Индексы
    indexes = [
        ("idx_users_role_id", "users(role_id)"),
        ("idx_orders_user_id", "orders(user_id)"),
        ("idx_orders_order_date", "orders(order_date)"),
        ("idx_products_category", "products(category)"),
        ("idx_stock_items_product_id", "stock_items(product_id)"),
        ("idx_stock_items_size_id", "stock_items(size_id)"),
        ("idx_order_items_order_id", "order_items(order_id)"),
        ("idx_order_items_stock_item_id", "order_items(stock_item_id)"),
    ]
    for name, target in indexes:
        c.execute(f"CREATE INDEX IF NOT EXISTS {name} ON {target}")

    conn.commit()
    conn.close()


def main():
    drop_all_tables()
    create_tables()
    print(f"База создана: {DB_PATH}")


if __name__ == "__main__":
    main()