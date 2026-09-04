import json
import os
import threading
from pathlib import Path


class JsonReportStore:
    def __init__(self, path: Path):
        self.path = path
        self._lock = threading.RLock()
        self.ensure_exists()

    def ensure_exists(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write([])

    def _read(self):
        self.ensure_exists()
        try:
            content = self.path.read_text(encoding="utf-8-sig")
            data = json.loads(content or "[]")
        except (json.JSONDecodeError, OSError) as exc:
            raise RuntimeError(f"Не удалось прочитать {self.path.name}: {exc}") from exc
        if not isinstance(data, list):
            raise RuntimeError(f"{self.path.name} должен содержать JSON-массив.")
        return data

    def _write(self, records):
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(
            json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        os.replace(temporary, self.path)

    def all(self):
        with self._lock:
            return self._read()

    def get(self, report_id):
        with self._lock:
            return next((item for item in self._read() if item["id"] == report_id), None)

    def add(self, record):
        with self._lock:
            records = self._read()
            records.append(record)
            self._write(records)

    def update(self, report_id, changes):
        with self._lock:
            records = self._read()
            for record in records:
                if record["id"] == report_id:
                    record.update(changes)
                    self._write(records)
                    return record
            return None

    def delete(self, report_id):
        with self._lock:
            records = self._read()
            remaining = [record for record in records if record["id"] != report_id]
            if len(remaining) == len(records):
                return False
            self._write(remaining)
            return True

