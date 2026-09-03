from django import forms
from django.utils import timezone

from .i18n import TRANSLATIONS
from .models import Report


class ReportForm(forms.ModelForm):
    date = forms.DateField(label="Дата", widget=forms.DateInput(attrs={"type": "date"}))
    time = forms.TimeField(label="Время", widget=forms.TimeInput(attrs={"type": "time", "step": "60"}))

    class Meta:
        model = Report
        fields = ["description_ru", "description_pt"]
        widgets = {
            "description_ru": forms.Textarea(attrs={"placeholder": "Опишите выполненную работу на русском...", "rows": 10}),
            "description_pt": forms.Textarea(attrs={"placeholder": "Перевод появится здесь...", "rows": 10}),
        }

    def __init__(self, *args, **kwargs):
        language = kwargs.pop("language", "ru")
        super().__init__(*args, **kwargs)
        text = TRANSLATIONS.get(language, TRANSLATIONS["ru"])
        if language == "pt":
            self.fields["description_ru"].required = False
            self.fields["description_pt"].widget.attrs["placeholder"] = "Descreva o trabalho realizado..."
            return
        self.fields["description_ru"].widget.attrs["placeholder"] = text["ru_placeholder"]
        self.fields["description_pt"].widget.attrs["placeholder"] = text["pt_placeholder"]
        now = timezone.localtime()
        self.fields["date"].initial = now.date()
        self.fields["time"].initial = now.time().replace(second=0, microsecond=0)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("date") and cleaned.get("time"):
            cleaned["occurred_at"] = timezone.make_aware(
                timezone.datetime.combine(cleaned["date"], cleaned["time"]),
                timezone.get_current_timezone(),
            )
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.occurred_at = self.cleaned_data["occurred_at"]
        if commit:
            instance.save()
        return instance
