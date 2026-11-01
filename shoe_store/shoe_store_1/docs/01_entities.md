# Сущности, атрибуты и связи «Чудо Обувь»

## 1. Сущности 

| № | Сущность | Назначение |
|---|---|---|
| 1 | roles | Справочник ролей |
| 2 | users | Пользователи |
| 3 | products | Товары (модели обуви) |
| 4 | sizes | Справочник размеров |
| 5 | stock_items | Товарные позиции |
| 6 | orders | Заказы |
| 7 | order_items | Состав заказа |

## 2. Атрибуты

| Сущность | Атрибуты |
|---|---|
| roles | `role_id` (PK), `role_name` |
| users | `user_id` (PK), `last_name`, `first_name`, `middle_name`, `login`, `role_id` (FK) |
| products | `product_id` (PK), `category`, `subcategory`, `manufacturer`, `name`, `image_path`, `composition`, `description`, `price` |
| sizes | `size_id` (PK), `size_value` |
| stock_items | `stock_item_id` (PK), `product_id` (FK), `size_id` (FK), `quantity` |__
| orders | `order_id` (PK), `order_date`, `user_id` (FK) |
| order_items | `order_item_id` (PK), `order_id` (FK), `stock_item_id` (FK), `quantity`, `price_at_order` |

## 3. Обязательные / необязательные

| Сущность | NOT NULL | NULL |
|---|---|---|
| roles | role_id, role_name | — |
| users | user_id, last_name, first_name, login, role_id | middle_name |
| products | product_id, category, subcategory, manufacturer, name, price | image_path, composition, description |
| sizes | size_id, size_value | — |
| stock_items | stock_item_id, product_id, size_id, quantity | — |
| orders | order_id, order_date, user_id | — |
| order_items | order_item_id, order_id, stock_item_id, quantity, price_at_order | — |

## 4. Уникальные атрибуты

| Сущность | Атрибут |
|---|---|
| users | login |
| roles | role_name |
| products | name + manufacturer |
| stock_items | product_id + size_id |
| sizes | size_value |

## 5. Значения по умолчанию

| Сущность | Атрибут | Значение |
|---|---|---|
| orders | order_date | CURRENT_DATE |
| stock_items | quantity | 0 |

## 6. Связи

| № | Связь | Тип | Ограничение |
|---|---|---|---|
| 1 | roles — users | 1:N | RESTRICT |
| 2 | users — orders | 1:N | CASCADE |
| 3 | orders — order_items | 1:N | CASCADE |
| 4 | products — stock_items | 1:N | RESTRICT |
| 5 | sizes — stock_items | 1:N | RESTRICT |
| 6 | stock_items — order_items | 1:N | RESTRICT |

**M:N:** products ↔ sizes (через stock_items), orders ↔ stock_items (через order_items).

## 7. Пояснения

**Товарная позиция — отдельная сущность:** у модели много размеров, для каждого своё количество. Иначе — нарушение 1НФ.

**Роль — справочник:** иначе `role_name` зависит от `role_id`, а не от `user_id` — нарушение 3НФ.