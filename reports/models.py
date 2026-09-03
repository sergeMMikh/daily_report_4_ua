from django.db import models


class Report(models.Model):
    occurred_at = models.DateTimeField("Дата и время")
    description_ru = models.TextField("Описание на русском", blank=True)
    description_pt = models.TextField("Описание на португальском")
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Изменено", auto_now=True)

    class Meta:
        ordering = ["-occurred_at"]
        verbose_name = "отчёт"
        verbose_name_plural = "отчёты"

    def __str__(self):
        return f"{self.occurred_at:%d.%m.%Y %H:%M} — {self.description_ru[:60]}"
