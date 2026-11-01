import sqlite3
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from procedures_functions import get_connection

def run_tests():
    print("=== ТЕСТИРОВАНИЕ ТРИГГЕРОВ ===\n")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    print("1. Обновление цены товара...")
    cursor.execute("SELECT price FROM products WHERE product_id = 1")
    old_price = cursor.fetchone()[0]
    cursor.execute("UPDATE products SET price = price + 1000 WHERE product_id = 1")
    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM audit_log WHERE table_name = 'products' AND operation = 'UPDATE'")
    count = cursor.fetchone()[0]
    print(f"   Записей в audit_log: {count} (должно быть > 0)")
    
    print("\n2. Автоматическое списание остатков...")
    cursor.execute("SELECT quantity_available FROM stock_items WHERE stock_item_id = 1")
    old_stock = cursor.fetchone()[0]
    cursor.execute("INSERT INTO orders (user_id, order_date) VALUES (3, '2024-02-01')")
    order_id = cursor.lastrowid
    cursor.execute("INSERT INTO order_items (order_id, stock_item_id, quantity, price) VALUES (?, 1, 2, 1000)", (order_id,))
    conn.commit()
    cursor.execute("SELECT quantity_available FROM stock_items WHERE stock_item_id = 1")
    new_stock = cursor.fetchone()[0]
    print(f"   Остаток: {old_stock} -> {new_stock} (должно уменьшиться на 2)")
    
    print("\n3. Запрет удаления пользователя с заказами...")
    try:
        cursor.execute("DELETE FROM users WHERE user_id = 3")
        conn.commit()
        print("   ОШИБКА: удаление прошло (триггер не сработал)")
    except sqlite3.IntegrityError as e:
        print(f"   УСПЕХ: {e}")
    
    print("\n4. Проверка на отрицательное количество...")
    try:
        cursor.execute("INSERT INTO stock_items (product_id, size_id, quantity_available) VALUES (1, 1, -5)")
        conn.commit()
        print("   ОШИБКА: вставка прошла (триггер не сработал)")
    except sqlite3.IntegrityError as e:
        print(f"   УСПЕХ: {e}")
    
    print("\n5. Содержимое audit_log:")
    cursor.execute("SELECT * FROM audit_log LIMIT 5")
    for row in cursor.fetchall():
        print(f"   {row}")
    
    conn.close()
    print("\n=== ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ ===")

if __name__ == "__main__":
    run_tests()