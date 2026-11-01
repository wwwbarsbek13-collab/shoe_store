# 03. Финальная проверка схемы именования

| Имя | Тип | Соответствует | Замечания |
|-----|-----|---------------|-----------|
| roles | таблица | да | мн. ч., snake_case |
| users | таблица | да | мн. ч. |
| products | таблица | да | мн. ч. |
| sizes | таблица | да | мн. ч. |
| stock_items | таблица | да | мн. ч., snake_case |
| orders | таблица | да | мн. ч., не order |
| order_items | таблица | да | мн. ч., snake_case |
| role_id | поле | да | суффикс _id |
| role_name | поле | да | snake_case |
| user_id | поле | да | суффикс _id |
| last_name | поле | да | snake_case |
| first_name | поле | да | snake_case |
| middle_name | поле | да | snake_case |
| login | поле | да | ед. ч. |
| product_id | поле | да | суффикс _id |
| product_name | поле | да | snake_case |
| category | поле | да | ед. ч. |
| manufacturer | поле | да | ед. ч. |
| price | поле | да | ед. ч. |
| image_path | поле | да | snake_case |
| size_id | поле | да | суффикс _id |
| size_value | поле | да | snake_case |
| stock_item_id | поле | да | суффикс _id |
| quantity | поле | да | ед. ч. |
| order_id | поле | да | суффикс _id |
| order_date | поле | да | snake_case |
| status | поле | да | ед. ч. |
| order_item_id | поле | да | суффикс _id |
| price_at_order | поле | да | snake_case |

