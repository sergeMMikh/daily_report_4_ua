# Daily Activity Report — Windows Portable

**Language:** [Português](README.md) · [Русский](README-RU.md) · **English**

A self-contained Windows 10/11 application for recording daily work and preparing reports in European Portuguese. Download one executable, place it in a writable folder, and open it — Python, PostgreSQL, and an installer are not required.

## Download

[Download `DailyReport.exe`](https://github.com/sergeMMikh/daily_report_4_ua/raw/refs/heads/main-win/dist/DailyReport.exe)

Windows SmartScreen may warn about the downloaded executable because it is not digitally signed. Review the repository source before running it. If you trust this project, select **Run anyway** in the SmartScreen dialog.

## Features

- local interface in Portuguese, Russian, and English;
- Portuguese selected by default;
- report entry with date and time;
- optional OpenAI-powered translation from Russian or English into European Portuguese;
- manual Portuguese entry when automatic translation is unavailable;
- chronological sorting of saved reports;
- Excel export for the last seven days, current month, or selected year;
- local UTF-8 JSON data storage;
- no external database or installed Python runtime;
- local-only access at `http://127.0.0.1:8765`.

## First launch

1. Download `DailyReport.exe`.
2. Move it to a writable folder such as `Documents\DailyReport`.
3. Open the executable.
4. The application opens in the default browser at `http://127.0.0.1:8765`.

The application automatically creates two files beside the executable:

- `config.json` — OpenAI API key and selected interface language;
- `reports.json` — saved report data.

Do not place the executable in `Program Files`, because the application must create and update these files beside itself.

## Automatic translation

Automatic translation is optional. Close the application, add an OpenAI API key to `config.json`, and start it again:

```json
{
  "openai_api_key": "YOUR_API_KEY",
  "language": "pt"
}
```

Supported language values are `pt` (Portuguese, the default), `ru` (Russian), and `en` (English). Changing the interface language in the application updates `config.json`. Without an API key, enter the Portuguese text manually.

Never share or commit a populated `config.json` because it contains the API key.

## Data and backups

All reports are stored in `reports.json` beside the executable. To back up or move the data, close Daily Activity Report and copy `reports.json` together with the executable. The file is human-readable UTF-8 JSON.

## Build from source

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt -r requirements-build.txt
.\build.ps1
```

The generated executable is written to `dist\DailyReport.exe`.

## Tests

```powershell
.venv\Scripts\python.exe -m unittest discover -s tests -v
```

For a shared server deployment with centralized storage and administration, see the [`main-python`](https://github.com/sergeMMikh/daily_report_4_ua/tree/main-python) edition.
