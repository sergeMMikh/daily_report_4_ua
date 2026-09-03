#!/bin/sh
set -eu

python - <<'PY'
import os
import time
import psycopg

for attempt in range(30):
    try:
        with psycopg.connect(
            dbname=os.environ["POSTGRES_DB"],
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
            host=os.environ.get("POSTGRES_HOST", "db"),
            port=os.environ.get("POSTGRES_PORT", "5432"),
        ):
            break
    except psycopg.OperationalError:
        if attempt == 29:
            raise
        time.sleep(2)
PY

python manage.py migrate --noinput
python manage.py collectstatic --noinput
exec waitress-serve --listen=0.0.0.0:8000 daily_report.wsgi:application

