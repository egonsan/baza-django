from django.urls import path

from .views import (
    software_list_view,
    software_detail_view,
    laboratory_detail_view,
    software_suggest_view,
)
from .admin_views import software_excel_import_view

app_name = "educational_software"

urlpatterns = [
    # /baza/oprogramowanie/
    path("", software_list_view, name="software_list"),

    # /baza/oprogramowanie/suggest/
    path("suggest/", software_suggest_view, name="software_suggest"),

    # /baza/oprogramowanie/<id>/
    path("<int:software_id>/", software_detail_view, name="software_detail"),

    # /baza/oprogramowanie/laboratorium/<number>/
    path(
        "laboratorium/<path:number>/",
        laboratory_detail_view,
        name="laboratory_detail",
    ),

    # /baza/oprogramowanie/import/  (import Excela dla Oprogramowania)
    path("import/", software_excel_import_view, name="software_import"),
]
