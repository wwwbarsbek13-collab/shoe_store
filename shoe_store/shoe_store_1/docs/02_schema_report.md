# Отчёт о созданной структуре базы данных

Создано 7 таблиц в базе данных `db/shoe_store.sqlite`:

1. **roles** — справочник ролей. PK: role_id. UNIQUE: role_name.
2. **sizes** — справочник размеров. PK: size_id. UNIQUE: size_value.
3. **users** — пользователи. PK: user_id. FK: role_id → roles. UNIQUE: login.
4. **products** — товары. PK: product_id. CHECK: price > 0.
5. **stock_items** — товарные позиции. PK: stock_item_id. FK: product_id → products, size_id → sizes. CHECK: quantity >= 0.
6. **orders** — заказы. PK: order_id. FK: user_id → users. DEFAULT: order_date = CURRENT_DATE, status = 'новый'.
7. **order_items** — состав заказов. PK: order_item_id. FK: order_id → orders (CASCADE), stock_item_id → stock_items (RESTRICT). CHECK: quantity > 0, price_at_order > 0.

Внешние ключи включены через `PRAGMA foreign_keys = ON`.