# Результаты проверки ограничений

| Ограничение | Ожидаемый результат | Фактический результат | Статус |
|-------------|---------------------|----------------------|--------|
| UNIQUE на login | ошибка | ошибка IntegrityError | пройден |
| NOT NULL на last_name | ошибка | ошибка IntegrityError | пройден |
| CHECK на price | ошибка | ошибка IntegrityError | пройден |
| CHECK на quantity | ошибка | ошибка IntegrityError | пройден |
| FOREIGN KEY на role_id | ошибка | ошибка IntegrityError | пройден |
| ON DELETE RESTRICT | ошибка | ошибка IntegrityError | пройден |
| ON DELETE CASCADE | каскадное удаление | каскадное удаление | пройден |