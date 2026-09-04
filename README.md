# Daily Activity Report — Python/Django

This branch contains the server-oriented edition of Daily Activity Report. It is designed for teams that need a shared web application, centralized data storage, administration, and Docker deployment.

## Features

- report entry with date and time;
- Russian, Portuguese, and English interface modes;
- optional OpenAI-powered translation from Russian or English into European Portuguese;
- manual Portuguese entry when automatic translation is unavailable;
- chronological sorting of saved reports;
- Excel export for the last seven days, current month, or selected year;
- Django administration;
- SQLite for local development or PostgreSQL for shared deployments;
- `Europe/Lisbon` time zone.

## Local setup

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

When `POSTGRES_DB` is unset, Django uses `db.sqlite3`. Add `OPENAI_API_KEY` to `.env` to enable automatic translation. Manual Portuguese input remains available without a key.

- Application: `http://localhost:8000/`
- Administration: `http://localhost:8000/admin/`

## Docker Compose setup

```powershell
Copy-Item .env.example .env
notepad .env
docker compose up -d --build
docker compose exec web python manage.py createsuperuser
```

Before deployment, set secure `DJANGO_SECRET_KEY` and `POSTGRES_PASSWORD` values and configure `DJANGO_ALLOWED_HOSTS`. The default ports are `8000` for the application and `5432` for PostgreSQL. Database data persists in the `postgres_data` Docker volume.

Check container state and logs with:

```powershell
docker compose ps
docker compose logs -f web
```

## Direct Windows/LAN deployment

Add the server IP address or DNS name to `DJANGO_ALLOWED_HOSTS`, then run:

```powershell
.venv\Scripts\waitress-serve.exe --listen=0.0.0.0:8000 daily_report.wsgi:application
```

Allow TCP port `8000` only on trusted networks. See [`docs/postgresql-windows.md`](docs/postgresql-windows.md) for additional PostgreSQL-on-Windows guidance.

## Configuration

Copy `.env.example` to `.env` and configure values appropriate for the environment. Important variables include:

- `DJANGO_SECRET_KEY` — a unique secret value for the Django installation;
- `DJANGO_DEBUG` — use `False` outside local development;
- `DJANGO_ALLOWED_HOSTS` — allowed host names or IP addresses;
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, and `POSTGRES_PORT` — PostgreSQL connection settings;
- `OPENAI_API_KEY` — optional key for automatic translation;
- `OPENAI_MODEL` — optional model override; the configured default is `gpt-4.1-mini`.

Never commit `.env`, API keys, local databases, or generated reports. Use `.env.example` as the configuration template.

## Tests

```powershell
python manage.py test
```

## Windows portable edition

Users who need a simple, single-user Windows application without Python, Django, or PostgreSQL can use the separate [`main-win`](https://github.com/sergeMMikh/daily_report_4_ua/tree/main-win) branch.

- [Windows documentation — Português](https://github.com/sergeMMikh/daily_report_4_ua/blob/main-win/README.md)
- [Windows documentation — English](https://github.com/sergeMMikh/daily_report_4_ua/blob/main-win/README-EN.md)
- [Download `DailyReport.exe`](https://github.com/sergeMMikh/daily_report_4_ua/raw/refs/heads/main-win/dist/DailyReport.exe)
