from django.urls import path

from .views import (
    EquipmentListView,
    EquipmentDetailView,
    EquipmentUpdateView,
    equipment_import_view,
    attachment_upload_view,
    attachment_delete_view,
)
from . import views_rooms  # widoki pomieszczeń
from .views_auth import oprogramowanie_view
from . import views_workers  # widoki Pracownika

app_name = "equipment"

urlpatterns = [
    # ====== OPROGRAMOWANIE ======
    path("oprogramowanie/", oprogramowanie_view, name="oprogramowanie"),

    # ====== MAGAZYN ======
    path("magazyn/", EquipmentListView.as_view(), name="equipment_list"),
    path("magazyn/<int:pk>/", EquipmentDetailView.as_view(), name="equipment_detail"),
    path("magazyn/<int:pk>/edit/", EquipmentUpdateView.as_view(), name="equipment_edit"),

    # ====== IMPORT / ZAŁĄCZNIKI ======
    path("import/", equipment_import_view, name="equipment_import"),
    path("<int:pk>/upload/", attachment_upload_view, name="attachment_upload"),
    path(
        "attachments/<int:attachment_id>/delete/",
        attachment_delete_view,
        name="attachment_delete",
    ),

    # ====== POMIESZCZENIA / SALE ======
    path("pomieszczenia/", views_rooms.rooms_dashboard, name="rooms_dashboard"),
    path(
        "pomieszczenia/<str:category_code>/",
        views_rooms.rooms_category_detail,
        name="rooms_category_detail",
    ),
    path(
        "pomieszczenia/<str:category_code>/<str:building>/<str:room>/",
        views_rooms.room_equipment_list,
        name="room_equipment_list",
    ),

    # ====== PRACOWNIK – NOWY MODUŁ ======
    # Lista pracowników
    path(
        "pracownicy/",
        views_workers.workers_list_view,
        name="workers_list",
    ),

    # Szczegóły konkretnego pracownika
    # UWAGA: używamy <path:worker_name>, żeby dopuszczać znak "/" w nazwie
    path(
        "pracownicy/<path:worker_name>/",
        views_workers.worker_detail_view,
        name="worker_detail",
    ),
]
