from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from .models import Equipment, ROOM_CATEGORY_CHOICES


@method_decorator(login_required(login_url="/admin/login/"), name="dispatch")
class RoomsOverviewView(TemplateView):
    """
    Widok POZIOM 1:
    Pomieszczenia / Sale – przegląd kategorii:
      - Lab. komputerowe
      - Sala wykładowa
      - Pokój
      - Inne

    Dla każdej kategorii liczymy:
      - ile jest unikalnych pomieszczeń (building + room),
      - ile jest kart sprzętu w tej kategorii.
    """

    template_name = "equipment/rooms_overview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = []

        for code, label in ROOM_CATEGORY_CHOICES:
            # Pomijamy MAGAZYN – on będzie obsługiwany osobno w zakładce Magazyn
            if code == "MAGAZYN":
                continue

            qs = Equipment.objects.filter(room_category=code)

            # Liczba unikalnych pomieszczeń (building + room, bez pustych)
            rooms_count = (
                qs.exclude(building="", room="")
                .values("building", "room")
                .distinct()
                .count()
            )

            # Liczba kart sprzętu w tej kategorii
            equipment_count = qs.count()

            categories.append(
                {
                    "code": code,
                    "label": label,
                    "rooms_count": rooms_count,
                    "equipment_count": equipment_count,
                }
            )

        context["categories"] = categories
        return context