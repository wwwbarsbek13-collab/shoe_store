# Результаты проверки структуры БД

## Таблицы (7 из 7)
| Таблица | Полей | FK | Индексов |
|---------|-------|----|----------|
| order_items | 5 | 2 | 2 |
| orders | 3 | 1 | 2 |
| products | 9 | 0 | 1 |
| roles | 2 | 0 | 0 |
| sizes | 2 | 0 | 0 |
| stock_items | 4 | 2 | 2 |
| users | 6 | 1 | 1 |

**Отсутствуют:** —
**Лишние:** —

## Детали по таблицам

### roles
- role_id — INTEGER, PK, NOT NULL
- role_name — TEXT, NOT NULL, UNIQUE

### sizes
- size_id — INTEGER, PK, NOT NULL
- size_value — REAL, NOT NULL, UNIQUE, CHECK (20 < value < 50)

### users
- user_id — INTEGER, PK, NOT NULL
- last_name — TEXT, NOT NULL
- first_name — TEXT, NOT NULL
- middle_name — TEXT, NULL
- login — TEXT, NOT NULL, UNIQUE, CHECK (3 ≤ length ≤ 20)
- role_id — INTEGER, NOT NULL, FK → roles(role_id) ON DELETE RESTRICT

### products
- product_id — INTEGER, PK, NOT NULL
- category — TEXT, NOT NULL
- subcategory — TEXT, NULL
- manufacturer — TEXT, NOT NULL
- product_name — TEXT, NOT NULL, CHECK (length > 0)
- image_path — TEXT, NULL
- composition — TEXT, NULL
- description — TEXT, NULL
- price — REAL, NOT NULL, CHECK (0 < price < 1000000)

### stock_items
- stock_item_id — INTEGER, PK, NOT NULL
- product_id — INTEGER, NOT NULL, FK → products(product_id) ON DELETE RESTRICT
- size_id — INTEGER, NOT NULL, FK → sizes(size_id) ON DELETE RESTRICT
- quantity_available — INTEGER, NOT NULL, DEFAULT 0, CHECK (≥ 0)

### orders
- order_id — INTEGER, PK, NOT NULL
- order_date — TEXT, NOT NULL, DEFAULT CURRENT_DATE
- user_id — INTEGER, NOT NULL, FK → users(user_id) ON DELETE RESTRICT

### order_items
- order_item_id — INTEGER, PK, NOT NULL
- order_id — INTEGER, NOT NULL, FK → orders(order_id) ON DELETE CASCADE
- stock_item_id — INTEGER, NOT NULL, FK → stock_items(stock_item_id) ON DELETE RESTRICT
- quantity — INTEGER, NOT NULL, CHECK (> 0)
- price — REAL, NOT NULL, CHECK (> 0)

## Индексы (8 шт.)
| Индекс | Таблица |
|--------|---------|
| idx_users_role_id | users(role_id) |
| idx_orders_user_id | orders(user_id) |
| idx_orders_order_date | orders(order_date) |
| idx_products_category | products(category) |
| idx_stock_items_product_id | stock_items(product_id) |
| idx_stock_items_size_id | stock_items(size_id) |
| idx_order_items_order_id | order_items(order_id) |
| idx_order_items_stock_item_id | order_items(stock_item_id) |

## Итог

- Все 7 таблиц созданы.
- PK, FK, CHECK, UNIQUE, NOT NULL, DEFAULT — на месте.
- 8 индексов созданы: 5 на FK + 3 на поля поиска/сортировки.
- `PRAGMA foreign_keys = ON` включён при подключении.