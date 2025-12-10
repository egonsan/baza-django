from django.urls import path

from .views import (
    EquipmentListView,
    EquipmentDetailView,
    EquipmentUpdateView,
    equipment_import_view,
    admin_equipment_export_view,
    attachment_upload_view,
    attachment_delete_view,
)
from . import views_rooms
from . import views_workers

app_name = "equipment"

urlpatterns = [
    # ====== MAGAZYN ======
    # /baza/magazyn/ → lista sprzętu z room_category = "MAGAZYN"
    path("magazyn/", EquipmentListView.as_view(), name="equipment_list"),

    # Szczegóły karty /baza/magazyn/<pk>/
    path("magazyn/<int:pk>/", EquipmentDetailView.as_view(), name="equipment_detail"),

    # Edycja karty /baza/magazyn/<int:pk>/edit/
    path(
        "magazyn/<int:pk>/edit/",
        EquipmentUpdateView.as_view(),
        name="equipment_edit",
    ),

    # IMPORT Z EXCELA /baza/import/
    path("import/", equipment_import_view, name="equipment_import"),

    # EKSPORT DO EXCELA /baza/export/
    path("export/", admin_equipment_export_view, name="equipment_export"),

    # Upload załącznika /baza/<pk>/upload/
    path("<int:pk>/upload/", attachment_upload_view, name="attachment_upload"),

    # Usuwanie załącznika /baza/attachments/<id>/delete/
    path(
        "attachments/<int:attachment_id>/delete/",
        attachment_delete_view,
        name="attachment_delete",
    ),

    # ====== POMIESZCZENIA / SALE ======
    # /baza/pomieszczenia/
    path(
        "pomieszczenia/",
        views_rooms.rooms_dashboard,
        name="rooms_dashboard",
    ),

    # /baza/pomieszczenia/<category_code>/
    path(
        "pomieszczenia/<str:category_code>/",
        views_rooms.rooms_category_detail,
        name="rooms_category_detail",
    ),

    # /baza/pomieszczenia/<category_code>/<building>/<room>/
    path(
        "pomieszczenia/<str:category_code>/<str:building>/<str:room>/",
        views_rooms.room_equipment_list,
        name="room_equipment_list",
    ),

    # ====== PRACOWNICY ======
    # /baza/pracownicy/
    path(
        "pracownicy/",
        views_workers.workers_list_view,
        name="workers_list",
    ),

    # /baza/pracownicy/<worker_name>/
    path(
        "pracownicy/<path:worker_name>/",
        views_workers.worker_detail_view,
        name="worker_detail",
    ),
]