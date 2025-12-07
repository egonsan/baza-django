from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path

from .models import Equipment, EquipmentAttachment


class EquipmentAttachmentInline(admin.TabularInline):
    model = EquipmentAttachment
    extra = 0


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = (
        "inventory_number",
        "equipment_name",
        "user_full_name",
        "building",
        "room",
        "status",
        "warranty_until",
        "warranty_status",
        "last_modified_by",
        "last_modified_at",
    )
    search_fields = (
        "inventory_number",
        "equipment_name",
        "hostname",
        "user_full_name",
        "building",
        "room",
    )
    list_filter = ("status", "building", "supplier")
    inlines = [EquipmentAttachmentInline]

    # Nie pokazujemy pola użytkownika w formularzu – ustawiamy je automatycznie
    exclude = ("last_modified_by",)

    # Własny template listy – żeby dodać przycisk "Import z Excela"
    change_list_template = "admin/equipment/equipment/change_list.html"

    def save_model(self, request, obj, form, change):
        """
        Ustawiamy last_modified_by zawsze na aktualnego użytkownika.
        """
        if request.user.is_authenticated:
            obj.last_modified_by = request.user
        super().save_model(request, obj, form, change)

    def get_urls(self):
        """
        Dodajemy własny URL w obrębie admina:
        /admin/equipment/equipment/import-excel/
        """
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-excel/",
                self.admin_site.admin_view(self.import_excel_view),
                name="equipment_import_excel",
            ),
        ]
        return custom_urls + urls

    def import_excel_view(self, request):
        """
        Proste przekierowanie do istniejącego widoku importu:
        /baza/import/
        """
        return redirect("/baza/import/")


@admin.register(EquipmentAttachment)
class EquipmentAttachmentAdmin(admin.ModelAdmin):
    list_display = ("file", "equipment", "uploaded_at")
    search_fields = ("file", "equipment__inventory_number")
