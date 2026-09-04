import json
import os
from pathlib import Path


def api_key(config_path: Path):
    environment_key = os.getenv("OPENAI_API_KEY", "").strip()
    if environment_key:
        return environment_key
    if config_path.exists():
        try:
            config = json.loads(config_path.read_text(encoding="utf-8-sig"))
            if not isinstance(config, dict):
                return ""
            value = config.get("openai_api_key", "")
            return value.strip() if isinstance(value, str) else ""
        except (json.JSONDecodeError, OSError):
            return ""
    return ""


def translate_to_portuguese(text: str, source_language: str, config_path: Path):
    key = api_key(config_path)
    if not key:
        raise RuntimeError("Добавьте openai_api_key в config.json.")
    from openai import OpenAI

    source = "English" if source_language == "en" else "Russian"
    response = OpenAI(api_key=key).responses.create(
        model="gpt-4.1-mini",
        instructions=(
            f"Translate workplace daily-report notes from {source} into natural European Portuguese (pt-PT). "
            "Preserve names, numbers, paragraphs and bullet points. Return only the translation."
        ),
        input=text,
    )
    result = response.output_text.strip()
    if not result:
        raise RuntimeError("Сервис перевода вернул пустой ответ.")
    return result
