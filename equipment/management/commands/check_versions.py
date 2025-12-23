from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from django.core.management.base import BaseCommand

try:
    import platform
    import django
except Exception:
    platform = None
    django = None


class Command(BaseCommand):
    help = "Generuje static/sprzet/version.json z informacją o wersjach i statusem aktualizacji (na razie lokalny stan)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--out",
            default="static/sprzet/version.json",
            help="Ścieżka wyjściowa (domyślnie: static/sprzet/version.json)",
        )
        parser.add_argument(
            "--label",
            default="Update check: not run yet",
            help="Tekst statusu aktualizacji (domyślnie: 'Update check: not run yet')",
        )

    def handle(self, *args, **options):
        out_path = Path(options["out"])
        out_path.parent.mkdir(parents=True, exist_ok=True)

        python_v = platform.python_version() if platform else ""
        django_v = django.get_version() if django else ""

        payload = {
            "python_version": python_v,
            "django_version": django_v,
            "update_label": options["label"],
            "checked_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        }

        out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        self.stdout.write(self.style.SUCCESS(f"OK: zapisano {out_path}"))
        self.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2))
