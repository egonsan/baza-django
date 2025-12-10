from django.contrib import admin
from django.template.response import TemplateResponse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import Equipment, EquipmentAttachment, ROOM_CATEGORY_CHOICES


def _confirm_move_action(request, queryset, action_name, action_verbose, target_label, target_value):
    """
    Helper do prostych akcji zmiany room_category (np. Move to Magazyn).
    """
    if request.POST.get("confirm") == "yes":
        updated_count = queryset.update(room_category=target_value)
        return updated_count
    else:
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

    # Pola tylko do odczytu w adminie – nieedytowalne ręcznie
    readonly_fields = ("last_modified_by", "last_modified_at")

    def save_model(self, request, obj, form, change):
        """
        Przy każdym zapisie w adminie:
        - last_modified_by = aktualnie zalogowany użytkownik
        - last_modified_at = aktualny czas
        """
        if request.user.is_authenticated:
            obj.last_modified_by = request.user
        obj.last_modified_at = timezone.now()
        super().save_model(request, obj, form, change)

    # -------------------------------
    # Akcja: Move to Pomieszczenia / Sale (kategoria + budynek + pomieszczenie)
    # -------------------------------

    def action_move_to_rooms(self, request, queryset):
        """
        Hurtowe przenoszenie zaznaczonych kart do wybranej kategorii pomieszczeń
        ORAZ ustawienie budynku i numeru pomieszczenia.

        Ustawia:
        - room_category (LAB / SALA / POKOJ / INNE),
        - building,
        - room.
        """

        if request.POST.get("confirm") == "yes":
            selected_category = request.POST.get("room_category", "").strip()
            building = request.POST.get("building", "").strip()
            room = request.POST.get("room", "").strip()

            valid_codes = [code for code, _ in ROOM_CATEGORY_CHOICES if code != "MAGAZYN"]

            errors = []
            if selected_category not in valid_codes:
                errors.append("Musisz wybrać poprawną kategorię pomieszczenia.")
            if not building:
                errors.append("Musisz podać budynek.")
            if not room:
                errors.append("Musisz podać numer pomieszczenia.")

            if errors:
                choices = [(c, l) for c, l in ROOM_CATEGORY_CHOICES if c != "MAGAZYN"]
                context = {
                    "title": "Przenieś zaznaczone karty do kategorii Pomieszczenia / Sale",
                    "queryset": queryset,
                    "opts": self.model._meta,
                    "action": "action_move_to_rooms",
                    "room_category_choices": choices,
                    "error_list": errors,
                    "building": building,
                    "room": room,
                }
                return TemplateResponse(
                    request,
                    "admin/equipment/equipment/confirm_move_to_rooms.html",
                    context,
                )

            updated_count = queryset.update(
                room_category=selected_category,
                building=building,
                room=room,
            )

            label_dict = dict(ROOM_CATEGORY_CHOICES)
            label = label_dict.get(selected_category, selected_category)

            self.message_user(
                request,
                f"Przeniesiono {updated_count} kart do kategorii: {label}, budynek: {building}, pomieszczenie: {room}.",
            )
            return None

        # Pierwsze wywołanie – pokazujemy formularz
        choices = [(c, l) for c, l in ROOM_CATEGORY_CHOICES if c != "MAGAZYN"]

        context = {
            "title": "Przenieś zaznaczone karty do kategorii Pomieszczenia / Sale",
            "queryset": queryset,
            "opts": self.model._meta,
            "action": "action_move_to_rooms",
            "room_category_choices": choices,
        }
        return TemplateResponse(
            request,
            "admin/equipment/equipment/confirm_move_to_rooms.html",
            context,
        )

    action_move_to_rooms.short_description = "Move to Pomieszczenia / Sale (wybierz kategorię + budynek + pomieszczenie)"

    # -------------------------------
    # Akcja: Move to Magazyn
    # -------------------------------

    def action_move_to_magazyn(self, request, queryset):
        """
        Ustawia room_category = 'MAGAZYN' dla zaznaczonych kart.
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
            updated_count = context_or_count
            self.message_user(
                request,
                f"Przeniesiono {updated_count} kart do kategorii: Magazyn.",
            )
            return None

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
    # Akcja: Przypisz do użytkownika
    # -------------------------------

    def action_assign_user(self, request, queryset):
        """
        Hurtowa zmiana pola user_full_name dla zaznaczonych kart sprzętu.
        """
        if request.POST.get("apply") == "yes":
            new_user = request.POST.get("new_user_full_name", "").strip()

            if not new_user:
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