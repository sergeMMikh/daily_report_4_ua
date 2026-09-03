from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("reports", "0001_initial")]
    operations = [
        migrations.AlterField(
            model_name="report",
            name="description_ru",
            field=models.TextField(blank=True, verbose_name="Описание на русском"),
        ),
    ]
