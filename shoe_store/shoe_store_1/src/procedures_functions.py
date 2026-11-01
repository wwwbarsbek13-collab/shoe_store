import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "shoe_store.sqlite"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def calc_order_total(price, quantity):
    """Задание 1.1: Умножение цены на количество."""
    if price is None or quantity is None:
        return 0.0
    try:
        price = float(price)
        quantity = int(quantity)
    except (ValueError, TypeError):
        return 0.0
    
    if quantity <= 0:
        return 0.0
    return round(price * quantity, 2)

def get_category_count(conn, category_name):
    """Задание 1.2: Количество товаров в категории (обращается к БД)."""
    if not category_name:
        return 0
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM products WHERE category = ?", (category_name,))
    result = cursor.fetchone()
    return result[0] if result else 0

def format_phone(phone):
    """Задание 1.3: Форматирование телефона в вид +7 (999) 123-45-67."""
    if not phone:
        return phone
    digits = ''.join(filter(str.isdigit, str(phone)))
 
    if len(digits) == 11 and digits[0] in ('7', '8'):
        return f"+7 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:11]}"

    elif len(digits) == 10:
        return f"+7 ({digits[0:3]}) {digits[3:6]}-{digits[6:8]}-{digits[8:10]}"
    else:
        return phone  # Если формат неверный, возвращаем как есть


def create_order(conn, user_id, product_id, size_id, quantity):
    """Процедура создания заказа с проверкой остатков."""
    cursor = conn.cursor()
    try:
        
        cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
        if not cursor.fetchone():
            print("Ошибка: пользователь не найден.")
            return False

        cursor.execute("""
            SELECT stock_item_id, quantity_available 
            FROM stock_items 
            WHERE product_id = ? AND size_id = ?
        """, (product_id, size_id))
        row = cursor.fetchone()
        if not row:
            print("Ошибка: товарная позиция не найдена.")
            return False
        
        stock_item_id, available = row

        if available < quantity:
            print(f"Ошибка: недостаточно товара. Доступно: {available}, запрошено: {quantity}")
            return False

        # 4. Создание заказа
        order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO orders (order_date, user_id) VALUES (?, ?)", (order_date, user_id))
        order_id = cursor.lastrowid

        # 5. Получение цены
        cursor.execute("SELECT price FROM products WHERE product_id = ?", (product_id,))
        price = cursor.fetchone()[0]

       
        cursor.execute("""
            INSERT INTO order_items (order_id, stock_item_id, quantity, price) 
            VALUES (?, ?, ?, ?)
        """, (order_id, stock_item_id, quantity, price))

       
        cursor.execute("""
            UPDATE stock_items 
            SET quantity_available = quantity_available - ? 
            WHERE stock_item_id = ?
        """, (quantity, stock_item_id))

        conn.commit()
        print(f"Заказ #{order_id} успешно создан.")
        return True
    except Exception as e:
        print(f"Ошибка при создании заказа: {e}")
        conn.rollback()  # Откат при ошибке
        return False

def update_stock(conn, stock_item_id, quantity_change):
    """Процедура изменения остатка с откатом, если уходит в минус."""
    cursor =conn.cursor()
    try:
       
        cursor.execute("SELECT quantity_available FROM stock_items WHERE stock_item_id = ?", (stock_item_id,))
        row = cursor.fetchone()
        if not row:
            print("Ошибка: позиция не найдена.")
            return False
        
        current = row[0]
        new_value = current + quantity_change
        
        if new_value < 0:
            print(f"Ошибка: остаток не может быть отрицательным (текущий: {current}, изменение: {quantity_change}). Транзакция отменена.")
            conn.rollback()
            return False

    
        cursor.execute("UPDATE stock_items SET quantity_available = ? WHERE stock_item_id = ?", (new_value, stock_item_id))
        conn.commit()
        print(f"Остаток обновлен: {current} -> {new_value}")
        return True
    except Exception as e:
        print(f"Ошибка: {e}")
        conn.rollback()
        return False

def get_sales_report(conn):
    """Процедура для получения отчета по продажам (возвращает данные)."""
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT p.product_name, SUM(oi.quantity) as total_sold, SUM(oi.quantity * oi.price) as revenue
            FROM order_items oi
            JOIN stock_items si ON oi.stock_item_id = si.stock_item_id
            JOIN products p ON si.product_id = p.product_id
            GROUP BY p.product_name
            ORDER BY revenue DESC
        """)
        return cursor.fetchall()
    except Exception as e:
        print(f"Ошибка при формировании отчета: {e}")
        return []

def register_functions(conn):
    """Регистрирует Python-функции в SQLite."""
    conn.create_function("calculate_total", 2, calc_order_total)
    conn.create_function("count_in_category", 1, lambda cat: get_category_count(conn, cat))
    conn.create_function("format_phone_sql", 1, format_phone)
    print("Функции зарегистрированы в базе данных.")

if __name__ == "__main__":
    conn = get_connection()
    register_functions(conn)
    print("\n--- Тест: создание заказа ---")
    create_order(conn, user_id=3, product_id=1, size_id=1, quantity=2)
    
    print("\n--- Тест: изменение остатка (в минус) ---")
    update_stock(conn, stock_item_id=1, quantity_change=-999)
    
    print("\n--- Отчет по продажам ---")
    report = get_sales_report(conn)
    for row in report:
        print(row)
    
    conn.close()