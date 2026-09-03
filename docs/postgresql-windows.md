# PostgreSQL на Windows и доступ из локальной сети

1. Установите PostgreSQL как обычную Windows-службу (не Docker), запомните пароль пользователя `postgres`.
2. В `psql` создайте отдельную БД и пользователя приложения:

```sql
CREATE USER daily_reports_app WITH PASSWORD 'replace-with-a-strong-password';
CREATE DATABASE daily_reports OWNER daily_reports_app ENCODING 'UTF8';
```

3. Укажите эти данные в `.env`. Не публикуйте файл `.env`.
4. Для прямого подключения с другой машины задайте в `postgresql.conf`:

```conf
listen_addresses = '*'
```

5. В `pg_hba.conf` разрешите только вашу подсеть (пример для LAN `192.168.1.0/24`):

```conf
host    daily_reports    daily_reports_app    192.168.1.0/24    scram-sha-256
```

6. Перезапустите службу PostgreSQL и добавьте входящее правило Windows Firewall для TCP 5432 только из той же подсети. Никогда не открывайте 5432 для всего интернета (`0.0.0.0/0`).
7. Проверка с другой машины: `psql -h <IP-сервера> -U daily_reports_app -d daily_reports`.

Файлы `postgresql.conf` и `pg_hba.conf` обычно находятся в каталоге `data` установленной версии PostgreSQL. Точное имя службы и каталог зависят от версии и выбранного пути установки.

## Если забыт пароль `postgres`

Пароль `postgres` — тот, который был задан в установщике PostgreSQL, а не пароль Windows. Если он неизвестен, откройте PowerShell **от имени администратора** и временно замените в `pg_hba.conf` метод `scram-sha-256` на `trust` только для строки `127.0.0.1/32`. Затем:

```powershell
Restart-Service postgresql-x64-18
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -h 127.0.0.1 -c "ALTER USER postgres WITH PASSWORD 'NEW-STRONG-PASSWORD'"
```

Сразу верните `scram-sha-256` вместо `trust` и ещё раз перезапустите службу. Не оставляйте `trust`: при нём локальное подключение не проверяет пароль.
