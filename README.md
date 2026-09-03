# Daily Activity Report

Небольшое Django-приложение для двуязычных ежедневных отчётов (RU → PT-PT), хранения в PostgreSQL и экспорта в Excel.

## Быстрый запуск

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

Если переменная `POSTGRES_DB` не задана, приложение использует SQLite для локальной разработки. Для рабочего режима заполните параметры PostgreSQL в `.env`. Для автоматического перевода добавьте `OPENAI_API_KEY`; без ключа перевод можно ввести вручную.

Интерфейс: `http://localhost:8000/`, админка: `http://localhost:8000/admin/`.

## Запуск через Docker Compose

На новой машине установите Docker, скопируйте проект и выполните:

```powershell
Copy-Item .env.example .env
notepad .env
docker compose up -d --build
docker compose exec web python manage.py createsuperuser
```

В `.env` обязательно замените `DJANGO_SECRET_KEY` и `POSTGRES_PASSWORD`, а в `DJANGO_ALLOWED_HOSTS` укажите IP или имя новой машины. Приложение будет доступно на порту `8000`, PostgreSQL — на порту `5432`. Данные БД сохраняются в томе `postgres_data` при пересоздании контейнеров. Ограничьте доступ к порту 5432 правилами firewall локальной сети.

Проверка состояния и журналов:

```powershell
docker compose ps
docker compose logs -f web
```

## Запуск в локальной сети

Добавьте IP или DNS-имя сервера в `DJANGO_ALLOWED_HOSTS`, затем запустите:

```powershell
.venv\Scripts\waitress-serve.exe --listen=0.0.0.0:8000 daily_report.wsgi:application
```

Откройте TCP 8000 в Windows Firewall только для профиля Private/LAN. Настройка прямого LAN-доступа к PostgreSQL описана в `docs/postgresql-windows.md`; самому веб-приложению безопаснее обращаться к БД локально, а пользователям — к HTTP-интерфейсу.
