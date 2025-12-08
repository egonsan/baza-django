from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import Http404
from django.shortcuts import render

from .models import Equipment, ROOM_CATEGORY_CHOICES


# ============================================
# POZIOM 1 – DASHBOARD KATEGORII
# /baza/pomieszczenia/
# ============================================

@login_required(login_url="/admin/login/")
def rooms_dashboard(request):
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

    categories = []

    # ROOM_CATEGORY_CHOICES zawiera też 'MAGAZYN' – pomijamy go tutaj
    for code, label in ROOM_CATEGORY_CHOICES:
        if code == "MAGAZYN":
            continue

        qs = Equipment.objects.filter(room_category=code)

        rooms_count = (
            qs.exclude(building="", room="")
            .values("building", "room")
            .distinct()
            .count()
        )

        equipment_count = qs.count()

        categories.append(
            {
                "code": code,
                "label": label,
                "rooms_count": rooms_count,
                "equipment_count": equipment_count,
            }
        )

    context = {
        "categories": categories,
    }
    return render(request, "equipment/rooms_overview.html", context)


# ============================================
# POZIOM 2 – LISTA POMIESZCZEŃ DLA KATEGORII
# /baza/pomieszczenia/<category_code>/
# ============================================

@login_required(login_url="/admin/login/")
def rooms_category_detail(request, category_code):
    """
    Widok POZIOM 2:
    Dla danej kategorii (LAB / SALA / POKOJ / INNE) pokazuje listę
    pomieszczeń (building + room) oraz liczbę kart sprzętu w każdym.
    """

    # Mapa kod → etykieta, np. "LAB" → "Lab. komputerowe"
    code_to_label = dict(ROOM_CATEGORY_CHOICES)

    # Sprawdzamy, czy kod jest poprawny i nie jest MAGAZYN
    if category_code not in code_to_label or category_code == "MAGAZYN":
        raise Http404("Nieprawidłowa kategoria pomieszczenia.")

    label = code_to_label[category_code]

    qs = (
        Equipment.objects.filter(room_category=category_code)
        .exclude(building="", room="")
    )

    # Grupujemy po (building, room) i liczymy ilość kart
    rooms = (
        qs.values("building", "room")
        .annotate(equipment_count=Count("id"))
        .order_by("building", "room")
    )

    context = {
        "category_code": category_code,
        "category_label": label,
        "rooms": rooms,
    }
    return render(request, "equipment/rooms_category_detail.html", context)


# ============================================
# POZIOM 3 – LISTA SPRZĘTU W KONKRETNEJ SALI
# /baza/pomieszczenia/<category_code>/<building>/<room>/
# ============================================

@login_required(login_url="/admin/login/")
def room_equipment_list(request, category_code, building, room):
    """
    Widok POZIOM 3:
    Lista kart sprzętu w konkretnym pomieszczeniu (building + room)
    i konkretnej kategorii (LAB / SALA / POKOJ / INNE).
    """

    code_to_label = dict(ROOM_CATEGORY_CHOICES)

    if category_code not in code_to_label or category_code == "MAGAZYN":
        raise Http404("Nieprawidłowa kategoria pomieszczenia.")

    label = code_to_label[category_code]

    equipments = Equipment.objects.filter(
        room_category=category_code,
        building=building,
        room=room,
    ).order_by("inventory_number")

    context = {
        "category_code": category_code,
        "category_label": label,
        "building": building,
        "room": room,
        "equipments": equipments,
    }
    return render(request, "equipment/room_equipment_list.html", context)