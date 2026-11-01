# УП.11 №8. Представления, индексы и EXPLAIN

## 1. Условия проверки

- Общая база: `db/shoe_store.sqlite` (сохранена из предыдущих занятий).
- SQLite: `3.46.1`.
- Семь пользовательских таблиц, внешние ключи и проверка целостности без ошибок.
- Представлений: **3**, явных индексов: **11**.
- Сравнение плана до создания индекса выполнялось **на копии в оперативной памяти**, не на оригинале.

## 2. Созданные представления

| Представление | Назначение | Строк |
|---|---|---:|
| `v_orders_full` | Заказ, дата, ФИО клиента, сумма по `order_items` | 3 |
| `v_products_with_stock` | Модель, цена, размер, остаток по размеру | 10 |
| `v_user_stats` | ФИО, логин, количество заказов, включая ноль | 3 |

**v_orders_full: первые три строки**

| order_id | order_date | client_name | total_amount |
|---|---|---|---|
| 1 | 2026-10-10 | Иванов Пётр Сергеевич | 7598.9 |
| 2 | 2026-10-11 | Смирнова Анна Олеговна | 13270.5 |
| 3 | 2026-10-12 | Кузнецов Алексей Викторович | 11870.5 |

**v_products_with_stock: первые три строки**

| product_name | price | size_value | quantity_available |
|---|---|---|---|
| Runner Pro | 3499.9 | 36.0 | 9 |
| Runner Pro | 3499.9 | 37.0 | 12 |
| Runner Pro | 3499.9 | 38.0 | 5 |

**v_user_stats: первые три строки**

| client_name | login | order_count |
|---|---|---|
| Иванов Пётр Сергеевич | admin | 1 |
| Смирнова Анна Олеговна | manager | 1 |
| Кузнецов Алексей Викторович | user | 1 |

Для совместимости с прошлыми работами в `v_products_with_stock` также оставлен столбец `total_quantity`, суммарный остаток по всей модели. Теперь каждая строка показывает конкретный размер и его количество.

## 3. Индексы

| Индекс | Поля | Назначение |
|---|---|---|
| `idx_products_category` | products(category) | Быстрый поиск по категории |
| `idx_orders_order_date` | orders(order_date) | Поиск и сортировка по дате заказа |
| `idx_orders_user_id` | orders(user_id) | JOIN с users и заказы пользователя |
| `idx_stock_items_product_id` | stock_items(product_id) | JOIN с products |
| `idx_stock_items_size_id` | stock_items(size_id) | JOIN с sizes |
| `idx_products_manufacturer_category` | products(manufacturer, category) | Уточняющий поиск одновременно по производителю и категории |

Первые пять индексов были созданы в прежних практиках; команды в `views_indexes.sql` используют `IF NOT EXISTS` и не дублируют их. Новый индекс здесь составной. Индекс `idx_products_manufacturer` из старого дня также оставлен для совместимости, хотя он частично перекрывается составным по его первому полю.

## 4. Фактические результаты EXPLAIN QUERY PLAN

**Поиск категории без индекса (временная копия)**

```sql
EXPLAIN QUERY PLAN
SELECT * FROM products WHERE category = 'Кроссовки';
```
- `SCAN products`

**Поиск категории с индексом (рабочая база)**

- `SEARCH products USING INDEX idx_products_category (category=?)`

**Тот же поиск после восстановления индекса во временной копии**

- `SEARCH products USING INDEX idx_products_category (category=?)`

План меняется с `SCAN products` на `SEARCH products USING INDEX idx_products_category`. Это доказательство выбора индекса планировщиком, а не замер скорости выполнения.

**Поиск производителя**

```sql
EXPLAIN QUERY PLAN
SELECT * FROM products WHERE manufacturer = 'Nike';
```
Реальная исходная база:
- `SEARCH products USING INDEX idx_products_manufacturer (manufacturer=?)`
При отсутствии обоих индексов на manufacturer (временная копия):
- `SCAN products`

В отличие от ожидаемого в PDF полного сканирования, в исходном проекте индекс `idx_products_manufacturer` уже существовал. Поэтому реальный план использует индекс; временная копия демонстрирует противоположный сценарий без него.

**JOIN заказов и пользователей**

```sql
EXPLAIN QUERY PLAN
SELECT * FROM orders o JOIN users u ON o.user_id = u.user_id;
```
- `SCAN o`
- `SEARCH u USING INTEGER PRIMARY KEY (rowid=?)`

Полное сканирование `orders` здесь нормально, так как условие WHERE отсутствует и нужны все заказы. Для каждой строки `users` ищется по первичному ключу.

**Составной индекс по двум фильтрам**

- `SEARCH products USING INDEX idx_products_manufacturer_category (manufacturer=? AND category=?)`

Выбор конкретного индекса зависит от статистики, объёма данных и запроса. На маленьком учебном наборе нельзя обещать заметное ускорение по времени.

## 5. Попытка обновить VIEW

```sql
CREATE VIEW v_simple AS SELECT product_id, price FROM products;
UPDATE v_simple SET price = 100 WHERE product_id = 1;
```
- Получена ошибка SQLite: `cannot modify v_simple because it is a view`.
- Цена в исходной таблице до попытки: **3499.9**, после: **3499.9**.
- В SQLite обычные VIEW доступны только на чтение. Для записи необходим специальный триггер `INSTEAD OF`, в этом задании он не нужен.
- Проверка выполнена на временной копии БД, поэтому основная база не изменена.

## 6. Вывод

Представления позволяют обращаться к готовым отчётным запросам как к таблицам и избегать повторного написания JOIN. Индексы ускоряют определённые фильтры, соединения и сортировки, однако увеличивают расходы на запись и место на диске. Команда `EXPLAIN QUERY PLAN` показывает выбранную стратегию: `SCAN` или `SEARCH ... USING INDEX`. Для каждого запроса индекс нужно подбирать по реальной нагрузке, а не создавать индексы для всех полей.
