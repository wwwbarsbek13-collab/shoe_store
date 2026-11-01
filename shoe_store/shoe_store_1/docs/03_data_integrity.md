# Проверка целостности данных

| Проверка | Ожидание | Факт | Статус |
|----------|----------|------|--------|
| price = -100 | ошибка CHECK | CHECK constraint failed | пройден |
| quantity = -5 | ошибка CHECK | CHECK constraint failed | пройден |
| quantity = 0 в order_items | ошибка CHECK | CHECK constraint failed | пройден |
| login = 'ab' | ошибка CHECK | CHECK constraint failed | пройден |
| size_value = 100 | ошибка CHECK | CHECK constraint failed | пройден |
| удаление роли с пользователями | ошибка FK | FOREIGN KEY constraint failed | пройден |
| удаление пользователя с заказами | ошибка FK | FOREIGN KEY constraint failed | пройден |
| каскадное удаление заказа | позиции удалены | позиции удалены | пройден |

