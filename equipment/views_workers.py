from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Equipment


def _normalize_worker_name(name: str) -> str:
    """
    Normalizacja nazwy pracownika na potrzeby grupowania:
    - zamiana na string,
    - strip spacji,
    - zamiana na wielkie litery,
    - redukcja wielu spacji do jednej.

    Dzięki temu "Wojnowski Adrian", "WOJNOWSKI ADRIAN ",
    "wojnowSKI   ADRIAN" trafią do jednej grupy.
    """
    if not name:
        return ""
    s = str(name).strip().upper()
    # redukcja wielu spacji do jednej
    parts = s.split()
    return " ".join(parts)


@login_required(login_url="/baza/")
def workers_list_view(request):
    """
    Lista unikalnych pracowników:
    - grupowanie po _normalize_worker_name(user_full_name),
    - pomijamy puste i techniczne wpisy ('', '-', '—'),
    - sortujemy alfabetycznie po kluczu,
    - liczymy ilość kart sprzętu w każdej grupie.
    """

    # pobieramy wszystkie niepuste user_full_name
    qs = Equipment.objects.exclude(user_full_name__isnull=True).exclude(
        user_full_name=""
    )

    groups = {}

    for eq in qs:
        raw_name = eq.user_full_name
        if not raw_name:
            continue

        clean = str(raw_name).strip()
        if clean in ["", "-", "—"]:
            continue

        key = _normalize_worker_name(clean)
        if not key:
            continue

        if key not in groups:
            groups[key] = {
                "key": key,             # klucz techniczny (do URL)
                "display_name": clean,  # pierwszy napotkany zapis do wyświetlenia
                "item_count": 0,
            }

        groups[key]["item_count"] += 1

    # zamiana na listę + sortowanie alfabetyczne po kluczu
    workers = sorted(groups.values(), key=lambda x: x["key"])

    context = {
        "workers": workers,
    }
    return render(request, "equipment/workers_list.html", context)


@login_required(login_url="/baza/")
def worker_detail_view(request, worker_name):
    """
    Lista kart sprzętu przypisanych do pracownika.
    Parametr worker_name w URL to *znormalizowany klucz* (DUŻE LITERY).
    """

    key = worker_name
    if not key:
        # zabezpieczenie – nie powinniśmy tu trafić
        items = []
        display_name = ""
    else:
        # pobieramy wszystkie potencjalne rekordy
        qs = Equipment.objects.exclude(user_full_name__isnull=True).exclude(
            user_full_name=""
        )

        matched = []
        for eq in qs:
            norm = _normalize_worker_name(eq.user_full_name)
            if norm == key:
                matched.append(eq)

        items = sorted(matched, key=lambda e: (e.inventory_number or ""))

        if items:
            # jako nagłówek bierzemy pierwszy "ładny" zapis z bazy
            display_name = str(items[0].user_full_name).strip()
        else:
            display_name = key

    context = {
        "worker_name": display_name,
        "items": items,
    }
    return render(request, "equipment/worker_detail.html", context)
