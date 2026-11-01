# Отчет о проверке структуры БД

| Таблица | Количество полей | Наличие PK | Наличие FK | Статус |
| roles | 2 | Да (role_id) | Нет | OK |
| genres | 2 | Да (genre_id) | Нет | OK |
| halls | 4 | Да (hall_id) | Нет | OK |
| movies | 6 | Да (movie_id) | Да (genre_id) | OK |
| clients | 5 | Да (client_id) | Да (role_id) | OK |
| sessions | 5 | Да (session_id) | Да (movie_id, hall_id) | OK |
| tickets | 6 | Да (ticket_id) | Да (session_id, client_id) | OK |

