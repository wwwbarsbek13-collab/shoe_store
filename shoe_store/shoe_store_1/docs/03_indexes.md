| Таблица | Поле | Тип | Обоснование |
|---------|------|-----|-------------|
| users | role_id | обычный | ускоряет JOIN с roles |
| orders | user_id | обычный | ускоряет JOIN с users |
| orders | order_date | обычный | сортировка заказов по дате |
| products | category | обычный | фильтрация по категории |
| products | manufacturer | обычный | фильтрация по производителю |
| stock_items | product_id | обычный | JOIN с products |
| stock_items | size_id | обычный | JOIN с sizes |
| order_items | order_id | обычный | JOIN с orders |
| order_items | stock_item_id | обычный | JOIN с stock_items |