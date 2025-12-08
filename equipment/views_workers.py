from collections import Counter

from django.shortcuts import render
from django.http import Http404

from .models import Equipment


def workers_list_view(request):
    """
    Lista pracowników na podstawie pola user_full_name z modelu Equipment.

    Uproszczona logika:
    - pobieramy WSZYSTKIE rekordy, gdzie user_full_name nie jest pusty,
    - w Pythonie zliczamy wystąpienia poszczególnych nazwisk (Counter),
    - budujemy listę słowników:
        {
            "user_full_name": "...",
            "equipment_count": X,
        }
    - sortujemy alfabetycznie po user_full_name.
    """

    # Pobieramy tylko rekordy z niepustym user_full_name
    equipment_with_users = Equipment.objects.exclude(user_full_name__isnull=True).exclude(
        user_full_name__exact=""
    )

    # Lista wszystkich nazw użytkowników
    names = [eq.user_full_name for eq in equipment_with_users]

    # Zliczamy karty per użytkownik
    counter = Counter(names)

    # Budujemy listę słowników
    workers = [
        {"user_full_name": name, "equipment_count": count}
        for name, count in counter.items()
    ]

    # Sortujemy alfabetycznie po nazwisku/imieniu tak, jak wpisane w bazie
    workers.sort(key=lambda w: w["user_full_name"])

    context = {
        "workers": workers,
    }

    return render(request, "equipment/workers_list.html", context)


def worker_detail_view(request, worker_name):
    """
    Szczegóły konkretnego pracownika – lista jego kart sprzętu.

    - worker_name przychodzi z URL jako string (Django już dekoduje %20 → spacja),
    - filtrujemy Equipment po user_full_name == worker_name,
    - jeśli nic nie ma → 404,
    - przekazujemy listę kart do szablonu workers_detail.html.
    """

    full_name = worker_name

    equipment_qs = Equipment.objects.filter(user_full_name=full_name).order_by(
        "inventory_number"
    )

    if not equipment_qs.exists():
        raise Http404("Taki pracownik nie istnieje w bazie sprzętu.")

    context = {
        "worker_name": full_name,
        "equipment_list": equipment_qs,
    }

    return render(request, "equipment/workers_detail.html", context)
