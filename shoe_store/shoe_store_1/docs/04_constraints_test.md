# Результаты проверки ограничений

| Ограничение | Ожидание | Факт | Статус |
|-------------|----------|------|--------|
| UNIQUE на login | ошибка | UNIQUE constraint failed: users.login | пройден |
| NOT NULL на last_name | ошибка | NOT NULL constraint failed: users.last_name | пройден |
| CHECK на price | ошибка | CHECK constraint failed: price > 0 AND price < 1000000 | пройден |
| CHECK на quantity_available | ошибка | CHECK constraint failed: quantity_available >= 0 | пройден |
| FOREIGN KEY на role_id | ошибка | FOREIGN KEY constraint failed | пройден |
| ON DELETE RESTRICT | ошибка | FOREIGN KEY constraint failed | пройден |

## Итог

Все 6 проверок пройдены.

- **UNIQUE** защищает от дубликатов логинов.
- **NOT NULL** не даёт вставить пользователя без фамилии.
- **CHECK** контролирует корректность цены и количества.
- **FOREIGN KEY** не позволяет ссылаться на несуществующую роль.
- **ON DELETE RESTRICT** запрещает удаление роли, пока на неё ссылаются пользователи.

Ограничения работают на уровне СУБД. Даже при ошибке в коде приложения
некорректные данные в базу не попадут.