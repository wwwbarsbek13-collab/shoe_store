## Порядок создания таблиц:

1. roles (role_id PK, role_name UNIQUE)
2. sizes (size_id PK, size_value REAL, CHECK 20<size<50)
3. users (user_id PK, login UNIQUE, CHECK 3≤len≤20, FK role_id → roles RESTRICT)
4. products (product_id PK, CHECK price 0<price<1млн, CHECK len(product_name)>0)
5. stock_items (PK stock_item_id, FK product_id → products RESTRICT, FK size_id → sizes RESTRICT, CHECK quantity_available ≥ 0)
6. orders (order_id PK, FK user_id → users RESTRICT, order_date NOT NULL, DEFAULT CURRENT_DATE)
7. order_items (PK order_item_id, FK order_id → orders CASCADE, FK stock_item_id → stock_items RESTRICT, CHECK quantity>0, CHECK price>0)

Индексы: idx_users_role_id, idx_orders_user_id, idx_orders_order_date,
idx_products_category, idx_stock_items_product_id, idx_stock_items_size_id,
idx_order_items_order_id, idx_order_items_stock_item_id

# Результаты проверки структуры БД

## Таблицы 
| Таблица | Полей | FK | Индексов |
|||||
| roles | 2 | 0 | 1 |
| sizes | 2 | 0 | 1 |
| users | 6 | 1 | 2 |
| products | 9 | 0 | 1 |
| stock_items | 4 | 2 | 2 |
| orders | 3 | 1 | 2 |
| order_items | 5 | 2 | 2 |

## Детали по таблицам

### roles
 role_id (INTEGER, PK, NN)
 role_name (TEXT, NN, UNIQUE)

### sizes
 size_id (INTEGER, PK, NN)
 size_value (REAL, NN, UNIQUE, CHECK)

### users
 user_id (INTEGER, PK, NN)
 last_name (TEXT, NN)
 first_name (TEXT, NN)
 middle_name (TEXT, NULL)
 login (TEXT, NN, UNIQUE, CHECK)
 role_id (INTEGER, NN, FK → roles RESTRICT)

### products
 product_id (INTEGER, PK, NN)
 category (TEXT, NN)
 subcategory (TEXT, NULL)
 manufacturer (TEXT, NN)
 product_name (TEXT, NN, CHECK)
 image_path (TEXT, NULL)
 composition (TEXT, NULL)
 description (TEXT, NULL)
 price (REAL, NN, CHECK)

### stock_items
 stock_item_id (INTEGER, PK, NN)
 product_id (INTEGER, NN, FK → products RESTRICT)
 size_id (INTEGER, NN, FK → sizes RESTRICT)
 quantity_available (INTEGER, NN, DEFAULT 0, CHECK)

### orders
 order_id (INTEGER, PK, NN)
 order_date (TEXT, NN, DEFAULT CURRENT_DATE)
 user_id (INTEGER, NN, FK → users RESTRICT)

### order_items
 order_item_id (INTEGER, PK, NN)
 order_id (INTEGER, NN, FK → orders CASCADE)
 stock_item_id (INTEGER, NN, FK → stock_items RESTRICT)
 quantity (INTEGER, NN, CHECK)
 price (REAL, NN, CHECK)

## Итог
Все 7 таблиц созданы. PK, FK, CHECK, UNIQUE, DEFAULT на месте.
8 индексов созданы.