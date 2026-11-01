# Отчёт о финальном DDL-скрипте

## Порядок создания таблиц
1. **Справочники:** roles, sizes
2. **Пользователи и товары:** users, products
3. **Товарные позиции:** stock_items
4. **Заказы:** orders
5. **Состав заказов:** order_items
6. **Индексы:** 9 штук

## Ограничения по таблицам
- **roles:** PK role_id, UNIQUE role_name
- **sizes:** PK size_id, UNIQUE size_value, CHECK 20 < size_value < 50
- **users:** PK user_id, UNIQUE login, CHECK 3 ≤ length(login) ≤ 20, FK role_id → roles RESTRICT
- **products:** PK product_id, CHECK length(product_name) > 0, CHECK 0 < price < 1000000
- **stock_items:** PK stock_item_id, CHECK quantity ≥ 0, FK product_id → products CASCADE, FK size_id → sizes RESTRICT
- **orders:** PK order_id, CHECK date(order_date) IS NOT NULL, FK user_id → users RESTRICT, DEFAULT order_date = CURRENT_DATE, DEFAULT status = 'новый'
- **order_items:** PK order_item_id, CHECK quantity > 0, CHECK price_at_order > 0, FK order_id → orders CASCADE, FK stock_item_id → stock_items RESTRICT

## Индексы
| Индекс | Таблица | Обоснование |
|--------|---------|-------------|
| idx_users_role_id | users(role_id) | JOIN с roles |
| idx_orders_user_id | orders(user_id) | JOIN с users |
| idx_orders_order_date | orders(order_date) | сортировка |
| idx_products_category | products(category) | фильтрация |
| idx_products_manufacturer | products(manufacturer) | фильтрация |
| idx_stock_items_product_id | stock_items(product_id) | JOIN |
| idx_stock_items_size_id | stock_items(size_id) | JOIN |
| idx_order_items_order_id | order_items(order_id) | JOIN |
| idx_order_items_stock_item_id | order_items(stock_item_id) | JOIN |

## Стратегии ON DELETE
- **RESTRICT:** roles→users, users→orders, sizes→stock_items, stock_items→order_items, products→stock_items
- **CASCADE:** orders→order_items, products→stock_items

## PRAGMA
`PRAGMA foreign_keys = ON` — включено при подключении.

## Экспорт
Схема экспортирована в `db/schema.sql`:
```bash
sqlite3 db/shoe_store.sqlite ".schema" > db/schema.sql