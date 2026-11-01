import sqlite3
from procedures_functions import get_connection, register_functions

conn = get_connection()
register_functions(conn) # Регистрируем наши кастомные функции (calculate_total и т.д.)
cursor = conn.cursor()

print("=== 1. Проверка функции calculate_total ===")
cursor.execute("""
    SELECT order_id, price, quantity, calculate_total(price, quantity) AS total
    FROM order_items
    LIMIT 3;
""")
for row in cursor.fetchall():
    print(row)

print("\n=== 2. Проверка функции format_phone_sql ===")
cursor.execute("""
    SELECT last_name, phone, format_phone_sql(phone) AS formatted
    FROM users;
""")
for row in cursor.fetchall():
    print(row)

print("\n=== 3. Проверка функции count_in_category ===")
cursor.execute("""
    SELECT category, count_in_category(category) AS cnt
    FROM products
    GROUP BY category;
""")
for row in cursor.fetchall():
    print(row)

print("\n=== 4. Проверка процедуры create_order (через Python) ===")
# Это не SQL-запрос, а вызов Python-функции, эмулирующей процедуру
from procedures_functions import create  р     ри _order
result = create_order(conn, user_id=3, product_id=1, size_id=1, quantity=2)
print(f"Результат создания заказа: {result}")

conn.close()