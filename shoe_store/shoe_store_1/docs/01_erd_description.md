# Описание ER-диаграммы «Чудо Обувь»

## Таблицы

### roles
Назначение: справочник ролей пользователей.
Первичный ключ: role_id.
Поля: role_id (PK), role_name.

### users
Назначение: пользователи системы.
Первичный ключ: user_id.
Поля: user_id (PK), last_name, first_name, middle_name, login, role_id (FK → roles.role_id).

### products
Назначение: товары (модели обуви).
Первичный ключ: product_id.
Поля: product_id (PK), category, subcategory, manufacturer, name,
image_path, composition, description, price.

### sizes
Назначение: справочник размеров.
Первичный ключ: size_id.
Поля: size_id (PK), size_value.

### stock_items
Назначение: товарные позиции (сочетание товара и размера).
Первичный ключ: stock_item_id.
Поля: stock_item_id (PK), product_id (FK → products.product_id),
size_id (FK → sizes.size_id), quantity.

### orders
Назначение: заказы.
Первичный ключ: order_id.
Поля: order_id (PK), order_date, user_id (FK → users.user_id).

### order_items
Назначение: состав заказа.
Первичный ключ: order_item_id.
Поля: order_item_id (PK), order_id (FK → orders.order_id),
stock_item_id (FK → stock_items.stock_item_id),
quantity, price_at_order.

## Связи

| Связь | Тип | Описание |
|---|---|---|
| roles — users | 1:N | Одна роль у многих пользователей |
| users — orders | 1:N | Один пользователь оформляет много заказов |
| orders — order_items | 1:N | Один заказ содержит много позиций |
| products — stock_items | 1:N | Один товар имеет много позиций по размерам |
| sizes — stock_items | 1:N | Один размер встречается во многих позициях |
| stock_items — order_items | 1:N | Одна позиция может входить во многие заказы |

## Кардинальность

- roles (1) — users (N)
- users (1) — orders (N)
- orders (1) — order_items (N)
- products (1) — stock_items (N)
- sizes (1) — stock_items (N)
- stock_items (1) — order_items (N)

## Правила именования

Латиница в нижнем регистре, snake_case, имена таблиц во множественном числе.

## Экспорт

- Исходник: ERD_module_1.drawio
- Экспорт: ERD_module_1.pdf (в папке docs/)