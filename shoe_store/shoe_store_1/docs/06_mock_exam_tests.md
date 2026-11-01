# Отчет о тестировании ограничений БД

| № | Ограничение | Ожидаемый результат | Фактический результат | Статус |
| :--- | :--- | :--- | :--- | :--- |
| 1 | UNIQUE (email) | Ошибка UNIQUE constraint failed | UNIQUE constraint failed: clients.email | Пройден |
| 2 | FOREIGN KEY (session_id) | Ошибка FOREIGN KEY constraint failed | FOREIGN KEY constraint failed | Пройден |
| 3 | CHECK (final_price > 0) | Ошибка CHECK constraint failed | CHECK constraint failed: final_price > 0 | Пройден |
| 4 | CHECK (seat_number > 0) | Ошибка CHECK constraint failed | CHECK constraint failed: seat_number > 0 | Пройден |
| 5 | ON DELETE RESTRICT | Ошибка FOREIGN KEY constraint failed | FOREIGN KEY constraint failed | Пройден |
| 6 | ON DELETE CASCADE | Билеты удалились (0 шт.) | Количество билетов: 0 | Пройден |