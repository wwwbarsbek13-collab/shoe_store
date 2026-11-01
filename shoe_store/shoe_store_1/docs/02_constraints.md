# Ограничения таблиц базы данных shoe_store

## roles
 role_id — PRIMARY KEY, NOT NULL, UNIQUE, AUTOINCREMENT
 role_name — NOT NULL, UNIQUE

## users
 user_id — PRIMARY KEY, NOT NULL, UNIQUE, AUTOINCREMENT
 last_name — NOT NULL
 first_name — NOT NULL
 middle_name — DEFAULT NULL (может быть пустым)
 login — NOT NULL, UNIQUE (система различает пользователей по логину)
 role_id — NOT NULL, FOREIGN KEY → roles(role_id) ON DELETE RESTRICT

## orders
 order_id — PRIMARY KEY, NOT NULL, UNIQUE, AUTOINCREMENT
 user_id — NOT NULL, FOREIGN KEY → users(user_id) ON DELETE RESTRICT
 order_date — NOT NULL, DEFAULT CURRENT_DATE
 status — NOT NULL, DEFAULT 'новый'

## order_items
 order_item_id — PRIMARY KEY, NOT NULL, UNIQUE, AUTOINCREMENT
 order_id — NOT NULL, FOREIGN KEY → orders(order_id) ON DELETE CASCADE
 stock_item_id — NOT NULL, FOREIGN KEY → stock_items(stock_item_id) ON DELETE RESTRICT
 quantity — NOT NULL, CHECK (quantity > 0)
 price_at_order — NOT NULL, CHECK (price_at_order > 0)

## stock_items
 stock_item_id — PRIMARY KEY, NOT NULL, UNIQUE, AUTOINCREMENT
 product_id — NOT NULL, FOREIGN KEY → products(product_id) ON DELETE CASCADE
 size_id — NOT NULL, FOREIGN KEY → sizes(size_id) ON DELETE RESTRICT
 quantity — NOT NULL, DEFAULT 0, CHECK (quantity >= 0)

## products
 product_id — PRIMARY KEY, NOT NULL, UNIQUE, AUTOINCREMENT
 product_name — NOT NULL
 category — NOT NULL
 manufacturer — NOT NULL
 price — NOT NULL, CHECK (price > 0)
 image_path — DEFAULT NULL

## sizes
 size_id — PRIMARY KEY, NOT NULL, UNIQUE, AUTOINCREMENT
 size_value — NOT NULL, UNIQUE

## Итог по CHECK
 products.price > 0
 stock_items.quantity >= 0
 order_items.quantity > 0
 order_items.price_at_order > 0

## Итог по DEFAULT
 orders.order_date = CURRENT_DATE
 orders.status = 'новый'
 stock_items.quantity = 0
 users.middle_name = NULL
 products.image_path = NULL

## Итог по ON DELETE
 users.role_id → roles: RESTRICT
 orders.user_id → users: RESTRICT
 stock_items.product_id → products: CASCADE
 stock_items.size_id → sizes: RESTRICT
 order_items.order_id → orders: CASCADE
 order_items.stock_item_id → stock_items: RESTRICT