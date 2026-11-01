# 03. Финальные ограничения CHECK

| Таблица | Поле | Ограничение | Обоснование |
|---------|------|-------------|-------------|
| products | product_name | CHECK (length(product_name) > 0) | наименование не пустое |
| products | price | CHECK (price > 0 AND price < 1000000) | цена в разумных пределах |
| stock_items | quantity | CHECK (quantity >= 0) | количество не отрицательное |
| order_items | quantity | CHECK (quantity > 0) | количество в заказе > 0 |
| order_items | price_at_order | CHECK (price_at_order > 0) | цена позиции > 0 |
| users | login | CHECK (length(login) >= 3 AND length(login) <= 20) | логин разумной длины |
| sizes | size_value | CHECK (size_value > 20 AND size_value < 50) | размеры в диапазоне |
| orders | order_date | CHECK (date(order_date) IS NOT NULL) | дата в формате ISO 8601 |