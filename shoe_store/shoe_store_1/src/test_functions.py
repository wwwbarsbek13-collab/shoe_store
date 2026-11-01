import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app_functions import (
    calc_discount, pluralize_items, format_full_name, 
    get_client_tier, get_client_loyalty_days, get_connection, place_order, cancel_order
)

def test_calc_discount():
    print("Тестирование calc_discount...")
    assert calc_discount(1000, 10) == 900.0
    assert calc_discount(1000, 0) == 1000.0
    assert calc_discount(1000, 100) == 0.0
    assert calc_discount(1000, -5) == 1000.0
    assert calc_discount(1000, 150) == 0.0
    assert calc_discount(None, 10) == 0.0
    assert calc_discount(1000, None) == 0.0
    assert calc_discount("abc", 10) == 0.0
    print("OK")

def test_pluralize_items():
    print("Тестирование pluralize_items...")
    assert pluralize_items(1) == "1 товар"
    assert pluralize_items(2) == "2 товара"
    assert pluralize_items(5) == "5 товаров"
    assert pluralize_items(0) == "0 товаров"
    assert pluralize_items(11) == "11 товаров"
    assert pluralize_items(21) == "21 товар"
    assert pluralize_items(22) == "22 товара"
    assert pluralize_items(None) == "0 товаров"
    print("OK")

def test_format_full_name():
    print("Тестирование format_full_name...")
    assert format_full_name("иванов", "иван", "иванович") == "Иванов И.И."
    assert format_full_name("Петров", "Пётр", None) == "Петров П."
    assert format_full_name(None, "Иван", "Иванович") == "Аноним"
    assert format_full_name("Иванов", "", "Иванович") == "Аноним"
    print("OK")

def test_get_client_tier():
    print("Тестирование get_client_tier...")
    assert get_client_tier(1000) == "Новичок"
    assert get_client_tier(5000) == "Бронза"
    assert get_client_tier(20000) == "Серебро"
    assert get_client_tier(50000) == "Золото"
    assert get_client_tier(150000) == "Платина"
    assert get_client_tier(None) == "Без статуса"
    assert get_client_tier(-100) == "Без статуса"
    print("OK")

def test_place_and_cancel_order():
    print("Тестирование place_order и cancel_order...")
    conn = get_connection()
    
    # Получаем исходный остаток
    cur = conn.cursor()
    cur.execute("SELECT quantity_available FROM stock_items WHERE stock_item_id = 1")
    initial_stock = cur.fetchone()[0]
    
    # Создаем заказ
    success = place_order(conn, user_id=3, product_id=1, size_id=1, quantity=2)
    assert success is True
    
    # Проверяем, что остаток уменьшился
    cur.execute("SELECT quantity_available FROM stock_items WHERE stock_item_id = 1")
    new_stock = cur.fetchone()[0]
    assert new_stock == initial_stock - 2
    
    # Получаем ID последнего заказа
    cur.execute("SELECT MAX(order_id) FROM orders")
    order_id = cur.fetchone()[0]
    
    # Отменяем заказ
    assert cancel_order(conn, order_id) is True
    
    # Проверяем, что остаток вернулся
    cur.execute("SELECT quantity_available FROM stock_items WHERE stock_item_id = 1")
    final_stock = cur.fetchone()[0]
    assert final_stock == initial_stock
    
    conn.close()
    print("OK")

if __name__ == "__main__":
    print("=== ЗАПУСК ТЕСТОВ ===\n")
    test_calc_discount()
    test_pluralize_items()
    test_format_full_name()
    test_get_client_tier()
    test_place_and_cancel_order()
    print("\n=== ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО! ===")