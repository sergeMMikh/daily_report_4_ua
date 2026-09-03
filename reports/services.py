import os


class TranslationUnavailable(RuntimeError):
    pass


def translate_to_portuguese(text: str, source_language: str = "ru") -> str:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise TranslationUnavailable("OPENAI_API_KEY не задан. Введите перевод вручную или добавьте ключ в .env.")

    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    source_name = "English" if source_language == "en" else "Russian"
    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        instructions=(
            f"Translate workplace daily-report notes from {source_name} into natural European Portuguese (pt-PT). "
            "Preserve meaning, dates, names, numbers, paragraph structure and bullet points. "
            "Return only the translation, without comments or quotation marks."
        ),
        input=text,
    )
    result = response.output_text.strip()
    if not result:
        raise TranslationUnavailable("Сервис перевода вернул пустой ответ.")
    return result
