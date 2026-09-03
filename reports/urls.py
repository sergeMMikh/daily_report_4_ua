from django.urls import path
from . import views

urlpatterns = [
    path("", views.report_list, name="report-list"),
    path("reports/create/", views.create_report, name="report-create"),
    path("translate/", views.translate, name="translate"),
    path("language/", views.set_language, name="set-language"),
    path("export/<str:period>/", views.export_reports, name="export-reports"),
]
