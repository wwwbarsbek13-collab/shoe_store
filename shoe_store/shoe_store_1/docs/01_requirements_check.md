# Проверка требований

## 1. Функциональные требования

| № | Требование | Таблица | Поле | Операция |
|---|---|---|---|---|
| 1 | Хранение количества позиций | stock_items | quantity | SELECT, UPDATE |
| 2 | Изображение модели | products | image_path | SELECT |
| 3 | Выбор одной или нескольких пар | stock_items, order_items | stock_item_id, quantity | INSERT |
| 4 | Просмотр списка заказов | orders, users | order_date, last_name, first_name | SELECT |
| 5 | Управление заказами | orders, order_items | order_id, order_item_id | INSERT, UPDATE, DELETE |

 Схема покрывает все 5 требований.

## 2. Роли пользователей

| Роль | Таблицы | Операции |
|---|---|---|
| Неавторизованный | products, stock_items | SELECT |
| Авторизованный | products, stock_items, orders, order_items | SELECT, INSERT |
| Менеджер | orders, order_items, products, stock_items | SELECT, INSERT, DELETE |
| Администратор | все таблицы | SELECT, INSERT, UPDATE, DELETE |

 Все 4 роли покрыты.

## 3. Вывод

Схема полная, покрывает все требования и роли.