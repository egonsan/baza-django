from django.contrib import admin
from django.template.response import TemplateResponse
from django.utils.translation import gettext_lazy as _

from .models import Equipment, EquipmentAttachment, ROOM_CATEGORY_CHOICES


# =====================================================================
# Helper do akcji przenoszenia pomiędzy kategoriami pomieszczeń
# =====================================================================


def _confirm_move_action(request, queryset, action_name, action_verbose, target_label, target_value):
    """
    Wspólny helper do akcji z potwierdzeniem zmiany room_category.
    - action_name: nazwa akcji (string, np. 'action_move_to_rooms')
    - action_verbose: etykieta akcji (np. 'Move to Pomieszczenia / Sale')
    - target_label: tekst w nagłówku (np. 'Pomieszczenia / Sale', 'Magazyn')
    - target_value: wartość room_category, np. 'INNE', 'MAGAZYN'
    """
    if request.POST.get("confirm") == "yes":
        # Użytkownik potwierdził operację
        updated_count = queryset.update(room_category=target_value)
        return updated_count
    else:
        # Pierwsze wywołanie – pokaż stronę potwierdzenia
        context = {
            "title": f"Potwierdź akcję: {action_verbose}",
            "queryset": queryset,
            "action_name": action_name,
            "target_label": target_label,
        }
        return context


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = (
        "inventory_number",
        "equipment_name",
        "building",
        "room_category",
        "room",
        "user_full_name",
        "status",
        "warranty_status",
    )
    list_filter = ("building", "room_category", "status")
    search_fields = (
        "inventory_number",
        "equipment_name",
        "hostname",
        "user_full_name",
        "building",
        "room",
    )

    actions = [
        "action_move_to_rooms",
        "action_move_to_magazyn",
        "action_assign_user",
        "delete_selected",
    ]

    # -------------------------------
    # Akcja: Move to Pomieszczenia / Sale
    # -------------------------------

    def action_move_to_rooms(self, request, queryset):
        """
        Ustawia room_category = 'INNE' dla zaznaczonych kart,
        co logicznie przenosi je do zakładki 'Pomieszczenia / Sale'.
        """
        context_or_count = _confirm_move_action(
            request=request,
            queryset=queryset,
            action_name="action_move_to_rooms",
            action_verbose="Move to Pomieszczenia / Sale",
            target_label="Pomieszczenia / Sale",
            target_value="INNE",
        )

        if isinstance(context_or_count, int):
            # Akcja została wykonana (confirm = yes)
            updated_count = context_or_count
            self.message_user(
                request,
                f"Przeniesiono {updated_count} kart do kategorii: Pomieszczenia / Sale (INNE).",
            )
            return None

        # Pierwsze wywołanie – pokaż stronę potwierdzenia
        context = context_or_count
        context.update(
            {
                "opts": self.model._meta,
                "action": "action_move_to_rooms",
            }
        )
        return TemplateResponse(
            request,
            "admin/equipment/equipment/confirm_move.html",
            context,
        )

    action_move_to_rooms.short_description = "Move to Pomieszczenia / Sale"

    # -------------------------------
    # Akcja: Move to Magazyn
    # -------------------------------

    def action_move_to_magazyn(self, request, queryset):
        """
        Ustawia room_category = 'MAGAZYN' dla zaznaczonych kart,
        co logicznie przenosi je do zakładki 'Magazyn'.
        """
        context_or_count = _confirm_move_action(
            request=request,
            queryset=queryset,
            action_name="action_move_to_magazyn",
            action_verbose="Move to Magazyn",
            target_label="Magazyn",
            target_value="MAGAZYN",
        )

        if isinstance(context_or_count, int):
            # Akcja została wykonana (confirm = yes)
            updated_count = context_or_count
            self.message_user(
                request,
                f"Przeniesiono {updated_count} kart do kategorii: Magazyn.",
            )
            return None

        # Pierwsze wywołanie – pokaż stronę potwierdzenia
        context = context_or_count
        context.update(
            {
                "opts": self.model._meta,
                "action": "action_move_to_magazyn",
            }
        )
        return TemplateResponse(
            request,
            "admin/equipment/equipment/confirm_move.html",
            context,
        )

    action_move_to_magazyn.short_description = "Move to Magazyn"

    # -------------------------------
    # NOWA AKCJA: Przypisz do użytkownika
    # -------------------------------

    def action_assign_user(self, request, queryset):
        """
        Hurtowa zmiana pola user_full_name dla zaznaczonych kart sprzętu.
        Krok 1: wyświetla stronę z polem tekstowym „Nowy użytkownik”.
        Krok 2: po zatwierdzeniu ustawia user_full_name na podaną wartość.
        """
        if request.POST.get("apply") == "yes":
            new_user = request.POST.get("new_user_full_name", "").strip()

            if not new_user:
                # Brak nazwy – ponownie wyświetlamy formularz z komunikatem
                context = {
                    "title": "Przypisz do użytkownika – podaj nazwę użytkownika",
                    "queryset": queryset,
                    "opts": self.model._meta,
                    "action": "action_assign_user",
                    "error": "Musisz podać nazwę użytkownika.",
                }
                return TemplateResponse(
                    request,
                    "admin/equipment/equipment/confirm_assign_user.html",
                    context,
                )

            updated_count = queryset.update(user_full_name=new_user)
            self.message_user(
                request,
                f"Zmieniono użytkownika dla {updated_count} kart na: {new_user}."
            )
            return None

        # Pierwsze wywołanie akcji – pokazujemy formularz z polem tekstowym
        context = {
            "title": "Przypisz zaznaczone karty do użytkownika",
            "queryset": queryset,
            "opts": self.model._meta,
            "action": "action_assign_user",
        }
        return TemplateResponse(
            request,
            "admin/equipment/equipment/confirm_assign_user.html",
            context,
        )

    action_assign_user.short_description = "Przypisz do użytkownika..."


@admin.register(EquipmentAttachment)
class EquipmentAttachmentAdmin(admin.ModelAdmin):
    list_display = ("file", "equipment", "uploaded_at")
    search_fields = ("file", "equipment__inventory_number", "equipment__equipment_name")
