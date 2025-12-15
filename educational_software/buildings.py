# /var/www/baza/educational_software/buildings.py

from __future__ import annotations

from typing import Dict, List, Tuple


# ============================================================
# STAŁA MAPA BUDYNKÓW (nie pochodzi z Excela)
# - Jeśli w przyszłości dojdzie nowe laboratorium w Excelu,
#   a nie będzie na listach poniżej -> trafi do "INNE".
# ============================================================

# Uzupełnij listy numerami laboratoriów (takimi jak w Excelu, np. "033", "708", "k5", itp.)
BUILDING_30: List[str] = [
    # TODO: wpisz numery laboratoriów z Budynku 30
]

BUILDING_40: List[str] = [
    # TODO: wpisz numery laboratoriów z Budynku 40
]

# Laboratoria bez budynku / specjalne (np. "Lab Maszynowe 11")
# Jeśli w Excelu to jest samo "11" -> wpisz "11"
# Jeśli w Excelu jest tekst -> wpisz dokładnie ten tekst.
SPECIAL_OTHER: List[str] = [
    "Lab Maszynowe 11",
    "11",
]


def normalize_lab_number(value: str) -> str:
    """
    Normalizacja numeru laboratorium (bez zmian semantycznych):
    - trim
    """
    return (value or "").strip()


def lab_building_group(lab_number: str) -> str:
    """
    Zwraca nazwę grupy budynku:
    - "BUDYNEK 30"
    - "BUDYNEK 40"
    - "INNE"
    """
    n = normalize_lab_number(lab_number)

    if n in SPECIAL_OTHER:
        return "INNE"

    if n in BUILDING_30:
        return "BUDYNEK 30"

    if n in BUILDING_40:
        return "BUDYNEK 40"

    return "INNE"


def group_labs(labs: List[str]) -> Dict[str, List[str]]:
    """
    Grupuje listę laboratoriów do 3 sekcji.
    Zwraca dict z kluczami: "BUDYNEK 30", "BUDYNEK 40", "INNE"
    """
    out: Dict[str, List[str]] = {"BUDYNEK 30": [], "BUDYNEK 40": [], "INNE": []}

    for lab in labs:
        n = normalize_lab_number(lab)
        if not n:
            continue
        out[lab_building_group(n)].append(n)

    # unikalne + sort
    for k in out:
        out[k] = sorted(set(out[k]))

    return out
