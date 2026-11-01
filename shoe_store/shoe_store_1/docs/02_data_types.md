# Типы данных SQLite для базы данных shoe_store

## Структура таблиц, полей и ключей

### Таблица roles
 role_id — идентификатор роли (PK)
 role_name — название роли (обычный атрибут)

### Таблица users
 user_id — идентификатор пользователя (PK)
 last_name — фамилия (обычный атрибут)
 first_name — имя (обычный атрибут)
 middle_name — отчество (обычный атрибут)
 login — логин (обычный атрибут)
 role_id — ссылка на роль (FK → roles.role_id)

### Таблица orders
 order_id — идентификатор заказа (PK)
 user_id — ссылка на пользователя (FK → users.user_id)
 order_date — дата заказа (обычный атрибут)
 status — статус заказа (обычный атрибут)

### Таблица order_items
 order_item_id — идентификатор позиции заказа (PK)
 order_id — ссылка на заказ (FK → orders.order_id)
 stock_item_id — ссылка на товарную позицию (FK → stock_items.stock_item_id)
 quantity — количество в заказе (обычный атрибут)
 price_at_order — цена на момент заказа (обычный атрибут)

### Таблица stock_items
 stock_item_id — идентификатор товарной позиции (PK)
 product_id — ссылка на товар (FK → products.product_id)
 size_id — ссылка на размер (FK → sizes.size_id)
 quantity — доступное количество (обычный атрибут)

### Таблица products
 product_id — идентификатор товара (PK)
 product_name — наименование товара (обычный атрибут)
 category — категория (обычный атрибут)
 manufacturer — производитель (обычный атрибут)
 price — цена (обычный атрибут)
 image_path — путь к изображению (обычный атрибут)

### Таблица sizes
 size_id — идентификатор размера (PK)
 size_value — размер обуви (обычный атрибут)