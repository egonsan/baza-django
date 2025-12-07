from django.urls import path

from .views import (
    EquipmentListView,
    EquipmentDetailView,
    EquipmentUpdateView,
    equipment_import_view,
    attachment_upload_view,
    attachment_delete_view,
    admin_equipment_export_view,
)

app_name = "equipment"

urlpatterns = [
    # Lista kart sprzętu /baza/
    path("", EquipmentListView.as_view(), name="equipment_list"),

    # Szczegóły karty /baza/<pk>/
    path("<int:pk>/", EquipmentDetailView.as_view(), name="equipment_detail"),

    # Edycja karty /baza/<pk>/edit/
    path("<int:pk>/edit/", EquipmentUpdateView.as_view(), name="equipment_edit"),

    # IMPORT Z EXCELA /baza/import/
    # <- to naprawia błąd "Reverse for 'equipment_import' not found"
    path("import/", equipment_import_view, name="equipment_import"),

    # EKSPORT DO EXCELA /baza/export/
    # Widok admin_equipment_export_view generuje plik XLSX
    path("export/", admin_equipment_export_view, name="equipment_export"),

    # Upload załącznika /baza/<pk>/upload/
    path("<int:pk>/upload/", attachment_upload_view, name="attachment_upload"),

    # Usuwanie załącznika /baza/attachments/<id>/delete/
    path(
        "attachments/<int:attachment_id>/delete/",
        attachment_delete_view,
        name="attachment_delete",
    ),
]
