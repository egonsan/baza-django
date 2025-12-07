from django.urls import path
from django.shortcuts import redirect

from .views import (
    EquipmentListView,
    EquipmentDetailView,
    EquipmentUpdateView,
    equipment_import_view,
    attachment_upload_view,
    attachment_delete_view,
)
from .views_auth import login_view, oprogramowanie_view

app_name = "equipment"

urlpatterns = [

    # 🔥 Nowość: /baza/ → login
    path("", lambda request: redirect("equipment:login"), name="root_redirect"),

    # Logowanie
    path("login/", login_view, name="login"),

    # Strona Oprogramowanie (landing po zalogowaniu)
    path("oprogramowanie/", oprogramowanie_view, name="oprogramowanie"),

    # Lista kart sprzętu → przeniesiemy to później pod "Magazyn"
    path("sprzet/", EquipmentListView.as_view(), name="equipment_list"),

    # Szczegóły karty
    path("sprzet/<int:pk>/", EquipmentDetailView.as_view(), name="equipment_detail"),

    # Edycja karty
    path("sprzet/<int:pk>/edit/", EquipmentUpdateView.as_view(), name="equipment_edit"),

    # Import z Excela
    path("sprzet/import/", equipment_import_view, name="equipment_import"),

    # Upload załącznika
    path("sprzet/<int:pk>/upload/", attachment_upload_view, name="attachment_upload"),

    # Usuwanie załącznika
    path(
        "sprzet/attachments/<int:attachment_id>/delete/",
        attachment_delete_view,
        name="attachment_delete",
    ),
]