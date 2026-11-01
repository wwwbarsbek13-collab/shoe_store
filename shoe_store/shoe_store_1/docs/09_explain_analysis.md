# Анализ запросов с помощью EXPLAIN QUERY PLAN

## 1. Созданные индексы и их обоснование

| Индекс | Таблица | Поля | Обоснование |
|--------|---------|------|-------------|
| `idx_products_category` | products | category | Ускоряет поиск и фильтрацию товаров по категории (частый запрос в интерфейсе). |
| `idx_orders_order_date` | orders | order_date | Ускоряет сортировку заказов по дате (например, для вывода последних заказов). |
| `idx_orders_user_id` | orders | user_id | Внешний ключ. Ускоряет JOIN с таблицей users и поиск заказов конкретного пользователя. |
| `idx_stock_items_product_id` | stock_items | product_id | Внешний ключ. Ускоряет JOIN с таблицей products. |
| `idx_stock_items_size_id` | stock_items | size_id | Внешний ключ. Ускоряет JOIN с таблицей sizes. |
| `idx_products_manufacturer_category` | products | manufacturer, category | Составной индекс. Ускоряет поиск по производителю и категории одновременно. |


