from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from urllib.parse import unquote

from .models import Software, Laboratory, SoftwareInstallation


# =========================
# STAŁA MAPA BUDYNKÓW
# =========================

BUILDING_40 = {
    "029C", "033", "136", "303", "321", "505", "511", "514",
}

OTHER_LABS = {
    "Lab Maszynowe 11",
}


def _normalize_lab_key(lab: str) -> str:
    """
    Normalizuje numer laboratorium:
    - usuwa dopiski typu (SpaceMouse)
    - trimuje spacje
    """
    if not lab:
        return ""
    return lab.split("(")[0].strip()


def get_building(lab_number: str) -> str:
    """
    Zwraca klucz budynku:
    - Budynek_40
    - Budynek_30
    - Inne
    """
    raw = (lab_number or "").strip()

    if raw in OTHER_LABS:
        return "Inne"

    normalized = _normalize_lab_key(raw)

    if normalized in BUILDING_40:
        return "Budynek_40"

    return "Budynek_30"


# =========================
# POMOCNICZE
# =========================

def _labs_for_software(software):
    """
    Zwraca listę laboratoriów (stringi) dla danego Software.
    """
    qs = (
        SoftwareInstallation.objects
        .filter(software=software)
        .select_related("laboratory")
    )

    labs = []
    for x in qs:
        if x.laboratory and x.laboratory.number:
            labs.append(str(x.laboratory.number).strip())

    return sorted(set(labs))


def _group_labs_by_building(labs):
    grouped = {
        "Budynek_30": [],
        "Budynek_40": [],
        "Inne": [],
    }

    for lab in labs:
        grouped[get_building(lab)].append(lab)

    return grouped


# =========================
# WIDOKI
# =========================

def software_list_view(request):
    q = request.GET.get("q", "").strip()

    qs = Software.objects.all().order_by("name")
    if q:
        qs = qs.filter(name__icontains=q)

    items = []
    for s in qs:
        labs = _labs_for_software(s)
        grouped = _group_labs_by_building(labs)

        items.append({
            "id": s.id,
            "name": s.name,
            "grouped_labs": grouped,
        })

    return render(
        request,
        "educational_software/software_list.html",
        {
            "items": items,
            "q": q,
        },
    )


def software_detail_view(request, software_id):
    software = get_object_or_404(Software, pk=software_id)

    labs = _labs_for_software(software)
    grouped = _group_labs_by_building(labs)

    return render(
        request,
        "educational_software/software_detail.html",
        {
            "software": software,
            "grouped_labs": grouped,
        },
    )


def laboratory_detail_view(request, number):
    # Naprawa podwójnego kodowania typu %2520 -> %20 -> " "
    decoded = number or ""
    for _ in range(2):
        decoded = unquote(decoded)

    lab = get_object_or_404(Laboratory, number=decoded)

    qs = (
        SoftwareInstallation.objects
        .filter(laboratory=lab)
        .select_related("software")
        .order_by("software__name")
    )

    softwares = [x.software for x in qs]

    return render(
        request,
        "educational_software/laboratory_detail.html",
        {
            "laboratory": lab,
            "building": get_building(str(lab.number).strip()),
            "softwares": softwares,
        },
    )


def software_suggest_view(request):
    q = request.GET.get("q", "").strip()
    results = []

    if q:
        qs = Software.objects.filter(name__icontains=q).order_by("name")[:10]
        results = [{"id": s.id, "name": s.name} for s in qs]

    return JsonResponse({"results": results})
