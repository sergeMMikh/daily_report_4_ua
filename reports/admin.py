from django.contrib import admin
from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("occurred_at", "short_ru", "short_pt", "created_at")
    list_filter = ("occurred_at", "created_at")
    search_fields = ("description_ru", "description_pt")
    date_hierarchy = "occurred_at"
    ordering = ("-occurred_at",)

    @admin.display(description="Описание RU")
    def short_ru(self, obj):
        return obj.description_ru[:80]

    @admin.display(description="Descrição PT")
    def short_pt(self, obj):
        return obj.description_pt[:80]

admin.site.site_header = "Daily Report — администрирование"
admin.site.site_title = "Daily Report"

