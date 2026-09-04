import io
import json
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import app as app_module
from openpyxl import load_workbook
from storage import JsonReportStore


class PortableAppTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.data_path = Path(self.temp.name) / "reports.json"
        self.old_config_path = app_module.CONFIG_PATH
        app_module.CONFIG_PATH = Path(self.temp.name) / "config.json"
        app_module.store = JsonReportStore(self.data_path)
        app_module.app.config.update(TESTING=True, SECRET_KEY="test")
        self.client = app_module.app.test_client()

    def tearDown(self):
        app_module.CONFIG_PATH = self.old_config_path
        self.temp.cleanup()

    def test_missing_json_file_is_created(self):
        self.assertTrue(self.data_path.exists())
        self.assertEqual(self.data_path.read_text(encoding="utf-8"), "[]")

    def test_missing_config_is_created_with_portuguese_default(self):
        self.assertFalse(app_module.CONFIG_PATH.exists())
        response = self.client.get("/")
        config = app_module.load_config()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(config, {"openai_api_key": "", "language": "pt"})
        self.assertIn("Relatório diário", response.get_data(as_text=True))

    def test_selected_language_is_saved_without_losing_api_key(self):
        app_module.CONFIG_PATH.write_text(
            json.dumps({"openai_api_key": "secret", "language": "pt"}), encoding="utf-8"
        )
        response = self.client.post("/language", data={"language": "ru"})
        config = json.loads(app_module.CONFIG_PATH.read_text(encoding="utf-8"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(config["language"], "ru")
        self.assertEqual(config["openai_api_key"], "secret")

    def test_portuguese_report_can_be_created_and_edited(self):
        with self.client.session_transaction() as session:
            session["language"] = "pt"
        response = self.client.post("/reports", data={
            "date": "2026-09-03", "time": "10:30", "description_pt": "Primeiro texto"
        })
        self.assertEqual(response.status_code, 302)
        report = app_module.store.all()[0]
        self.assertEqual(report["description_source"], "")
        response = self.client.post(f"/reports/{report['id']}/edit", data={
            "date": "2026-09-04", "time": "11:45", "description_pt": "Texto alterado"
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(app_module.store.get(report["id"])["description_pt"], "Texto alterado")

    def test_export_contains_only_portuguese_description(self):
        app_module.store.add({
            "id": "one", "occurred_at": datetime.now(app_module.LISBON).isoformat(),
            "source_language": "ru", "description_source": "Русский текст",
            "description_pt": "Texto português", "created_at": "", "updated_at": "",
        })
        response = self.client.get("/export/year")
        workbook = load_workbook(io.BytesIO(response.data))
        values = list(workbook.active.values)
        self.assertEqual(values[0], ("Data", "Hora", "Descrição (PT)"))
        self.assertEqual(values[1][2], "Texto português")
        self.assertNotIn("Русский текст", str(values))

    def test_delete_report(self):
        app_module.store.add({
            "id": "delete-me", "occurred_at": datetime.now(app_module.LISBON).isoformat(),
            "source_language": "pt", "description_source": "", "description_pt": "Apagar",
            "created_at": "", "updated_at": "",
        })
        response = self.client.post("/reports/delete-me/delete")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(app_module.store.all(), [])

    def test_missing_api_key_is_a_normal_unavailable_response(self):
        response = self.client.post("/translate", data={"text": "Выполнил работу"})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.get_json()["available"])


if __name__ == "__main__":
    unittest.main()
