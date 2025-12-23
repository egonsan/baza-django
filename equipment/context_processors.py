from __future__ import annotations

import json
import platform
from pathlib import Path

import django


def _load_version_status() -> dict:
    """
    Czyta wynik ostatniego sprawdzenia aktualizacji z pliku JSON (jeśli istnieje).
    Plik będzie generowany osobnym krokiem/komendą (w następnym kroku).
    """
    candidates = [
        Path("/var/www/baza/staticfiles/sprzet/version.json"),
        Path("/var/www/baza/static/sprzet/version.json"),
    ]
    for p in candidates:
        try:
            if p.exists():
                return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def version_info(request):
    data = _load_version_status()

    python_v = platform.python_version()
    django_v = django.get_version()

    # Domyślne wartości, jeśli jeszcze nie wykonaliśmy sprawdzenia aktualizacji
    update_label = data.get("update_label", "Update check: not run yet")
    checked_at = data.get("checked_at", "")

    return {
        "APP_PYTHON_VERSION": python_v,
        "APP_DJANGO_VERSION": django_v,
        "APP_UPDATE_LABEL": update_label,
        "APP_UPDATE_CHECKED_AT": checked_at,
    }
