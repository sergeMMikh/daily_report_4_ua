from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [migrations.CreateModel(
        name="Report",
        fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("occurred_at", models.DateTimeField(verbose_name="Дата и время")),
            ("description_ru", models.TextField(verbose_name="Описание на русском")),
            ("description_pt", models.TextField(verbose_name="Описание на португальском")),
            ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создано")),
            ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Изменено")),
        ],
        options={"verbose_name": "отчёт", "verbose_name_plural": "отчёты", "ordering": ["-occurred_at"]},
    )]

