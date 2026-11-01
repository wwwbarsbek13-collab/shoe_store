import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "shoe_store.sqlite"

def get_connection():
    """Подключение к БД с включением внешних ключей."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# ==========================================
# 1. Функции для обработки данных
# ==========================================

def calc_discount(price, discount_percent):
    """Расчет цены со скидкой с защитой от None и некорректных значений."""
    if price is None or discount_percent is None:
        return 0.0
    try:
        price = float(price)
        discount_percent = float(discount_percent)
    except (ValueError, TypeError):
        return 0.0
    
    if discount_percent < 0:
        discount_percent = 0
    if discount_percent > 100:
        discount_percent = 100
        
    result = price - (price * discount_percent / 100)
    return round(result, 2)

def pluralize_items(count):
    """Склонение слова 'товар' в зависимости от числа."""
    if count is None:
        return "0 товаров"
    try:
        count = int(count)
    except (ValueError, TypeError):
        return "0 товаров"
        
    count = abs(count)
    last_digit = count % 10
    last_two_digits = count % 100
    
    if 11 <= last_two_digits <= 19:
        return f"{count} товаров"
    
    if last_digit == 1:
        return f"{count} товар"
    elif last_digit in (2, 3, 4):
        return f"{count} товара"
    else:
        return f"{count} товаров"

def format_full_name(last, first, middle):
    """Форматирование ФИО в вид 'Фамилия И.О.'."""
    if not last or not first:
        return "Аноним"
    
    last = str(last).strip().capitalize()
    first = str(first).strip().capitalize()
    
    if middle and str(middle).strip():
        middle = str(middle).strip().capitalize()
        return f"{last} {first[0]}.{middle[0]}."
    else:
        return f"{last} {first[0]}."

# ==========================================
# 2. Эмуляция процедур (Транзакции)
# ==========================================

def place_order(conn, user_id, product_id, size_id, quantity):
    """Создание заказа с проверкой остатков и списанием со склада."""
    cursor = conn.cursor()
    try:
        # 1. Проверка пользователя
        cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
        if not cursor.fetchone():
            return False
            
        # 2. Поиск stock_item_id
        cursor.execute("""
            SELECT stock_item_id, quantity_available 
            FROM stock_items 
            WHERE product_id = ? AND size_id = ?
        """, (product_id, size_id))
        row = cursor.fetchone()
        if not row:
            return False
            
        stock_item_id, available = row
        
        # 3. Проверка остатка
        if available < quantity:
            print(f"Ошибка: недостаточно товара. Доступно: {available}, запрошено: {quantity}")
            return False
            
        # 4. Создание заказа
        order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO orders (order_date, user_id) VALUES (?, ?)", (order_date, user_id))
        order_id = cursor.lastrowid
        
        # 5. Получение цены товара
        cursor.execute("SELECT price FROM products WHERE product_id = ?", (product_id,))
        price = cursor.fetchone()[0]
        
        # 6. Добавление позиции
        cursor.execute("""
            INSERT INTO order_items (order_id, stock_item_id, quantity, price) 
            VALUES (?, ?, ?, ?)
        """, (order_id, stock_item_id, quantity, price))
        
        # 7. Списание со склада
        cursor.execute("""
            UPDATE stock_items 
            SET quantity_available = quantity_available - ? 
            WHERE stock_item_id = ?
        """, (quantity, stock_item_id))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Ошибка при создании заказа: {e}")
        conn.rollback()
        return False

def cancel_order(conn, order_id):
    """Отмена заказа с возвратом товара на склад."""
    cursor = conn.cursor()
    try:
        # 1. Проверка заказа
        cursor.execute("SELECT order_id FROM orders WHERE order_id = ?", (order_id,))
        if not cursor.fetchone():
            return False
            
        # 2. Получение позиций заказа
        cursor.execute("""
            SELECT stock_item_id, quantity 
            FROM order_items 
            WHERE order_id = ?
        """, (order_id,))
        items = cursor.fetchall()
        
        # 3. Возврат на склад
        for stock_item_id, quantity in items:
            cursor.execute("""
                UPDATE stock_items 
                SET quantity_available = quantity_available + ? 
                WHERE stock_item_id = ?
            """, (quantity, stock_item_id))
            
        # 4. Удаление позиций
        cursor.execute("DELETE FROM order_items WHERE order_id = ?", (order_id,))
        
        # 5. Удаление заказа
        cursor.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Ошибка при отмене заказа: {e}")
        conn.rollback()
        return False

# ==========================================
# 3. Аналитические функции
# ==========================================

def get_client_tier(total_spent):
    """Определение уровня клиента по сумме покупок."""
    if total_spent is None:
        return "Без статуса"
    try:
        total_spent = float(total_spent)
    except (ValueError, TypeError):
        return "Без статуса"
        
    if total_spent < 0:
        return "Без статуса"
    if total_spent < 5000:
        return "Новичок"
    if total_spent < 20000:
        return "Бронза"
    if total_spent < 50000:
        return "Серебро"
    if total_spent < 100000:
        return "Золото"
    return "Платина"

def get_client_loyalty_days(first_order_date_str):
    """Количество дней с первого заказа."""
    if not first_order_date_str:
        return 0
    try:
        # Пытаемся распарсить дату (может быть с временем или без)
        date_str = str(first_order_date_str).split()[0]
        first_date = datetime.strptime(date_str, "%Y-%m-%d")
        delta = datetime.now() - first_date
        return delta.days
    except (ValueError, TypeError):
        return 0

# ==========================================
# Регистрация функций в БД
# ==========================================

def register_functions(conn):
    """Регистрирует все Python-функции в SQLite."""
    conn.create_function("calc_discount", 2, calc_discount)
    conn.create_function("pluralize_items", 1, pluralize_items)
    conn.create_function("format_full_name", 3, format_full_name)
    conn.create_function("get_client_tier", 1, get_client_tier)
    conn.create_function("get_client_loyalty_days", 1, get_client_loyalty_days)
    print("Все функции зарегистрированы в базе данных.")

if __name__ == "__main__":
    conn = get_connection()
    register_functions(conn)
    conn.close()