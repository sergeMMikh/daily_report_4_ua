# Daily Activity Report

Daily Activity Report is available in two product variants maintained in separate branches of this repository.

## Choose a version

| Version | Branch | Best for |
| --- | --- | --- |
| Windows portable | [`main-win`](https://github.com/sergeMMikh/daily_report_4_ua/tree/main-win) | Individual Windows users who want one executable and local data storage |
| Python/Django | [`main-python`](https://github.com/sergeMMikh/daily_report_4_ua/tree/main-python) | Teams that need a shared web application, database, administration, or Docker deployment |

Quick links:

- [Download `DailyReport.exe`](https://github.com/sergeMMikh/daily_report_4_ua/raw/refs/heads/main-win/dist/DailyReport.exe)
- [Windows documentation](https://github.com/sergeMMikh/daily_report_4_ua/blob/main-win/README.md)
- [Python/Django documentation](https://github.com/sergeMMikh/daily_report_4_ua/blob/main-python/README.md)

## Shared capabilities

Both versions provide report entry with date and time, Russian/Portuguese/English interface modes, optional OpenAI-powered translation from Russian or English into European Portuguese, manual Portuguese entry, chronological sorting, and Excel export for the last seven days, current month, or selected year. Both use the `Europe/Lisbon` time zone.

## Windows portable version

The [`main-win`](https://github.com/sergeMMikh/daily_report_4_ua/tree/main-win) branch contains a self-contained Windows 10/11 application built with Flask, Waitress, and PyInstaller. Python, PostgreSQL, and an installer are not required on the destination computer.

[Download `DailyReport.exe`](https://github.com/sergeMMikh/daily_report_4_ua/raw/refs/heads/main-win/dist/DailyReport.exe), place it in a writable folder, and open it. The application starts a local-only interface at `http://127.0.0.1:8765` and creates these files beside the executable on first launch:

- `config.json` — OpenAI API key and selected interface language; Portuguese (`pt`) is the default;
- `reports.json` — report data in readable UTF-8 JSON format.

The Windows edition is intended for one user. Back up or move its data by copying `reports.json`. Do not put the executable in `Program Files`, because it must create and update files beside itself.

To enable automatic translation, close the application, add the key to `config.json`, and start it again:

```json
{
  "openai_api_key": "YOUR_API_KEY",
  "language": "pt"
}
```

The application remains usable without a key; Portuguese text can be entered manually.

### Build the Windows executable

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt -r requirements-build.txt
.\build.ps1
```

The generated file is `dist\DailyReport.exe`.

## Python/Django version

The [`main-python`](https://github.com/sergeMMikh/daily_report_4_ua/tree/main-python) branch is the server-oriented edition. It uses Django with SQLite for local development or PostgreSQL for shared deployments. It includes Django administration, session-based language selection, WhiteNoise static-file serving, Waitress, and Docker Compose configuration.

### Local setup

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

When `POSTGRES_DB` is unset, Django uses `db.sqlite3`. Add `OPENAI_API_KEY` to `.env` for automatic translation. Manual Portuguese input remains available without a key.

- Application: `http://localhost:8000/`
- Administration: `http://localhost:8000/admin/`

### Docker Compose setup

```powershell
Copy-Item .env.example .env
notepad .env
docker compose up -d --build
docker compose exec web python manage.py createsuperuser
```

Before deployment, set secure `DJANGO_SECRET_KEY` and `POSTGRES_PASSWORD` values and configure `DJANGO_ALLOWED_HOSTS`. The default ports are `8000` for the application and `5432` for PostgreSQL. Database data persists in the `postgres_data` Docker volume.

For direct Windows/LAN operation without Docker:

```powershell
.venv\Scripts\waitress-serve.exe --listen=0.0.0.0:8000 daily_report.wsgi:application
```

Allow TCP port `8000` only on trusted networks. See [`docs/postgresql-windows.md`](docs/postgresql-windows.md) for additional PostgreSQL-on-Windows guidance.

## Security and local files

Never commit API keys, `.env`, `config.json`, databases, or personal report data. Repository ignore rules exclude these local files. Use `.env.example` and `config.example.json` as templates.

## Tests

Python/Django branch:

```powershell
python manage.py test
```

Windows branch:

```powershell
.venv\Scripts\python.exe -m unittest discover -s tests -v
```
