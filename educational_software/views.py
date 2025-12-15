from urllib.parse import unquote

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Laboratory, Software, SoftwareInstallation


# =========================
# STAŁA MAPA BUDYNKÓW
# =========================

BUILDING_40 = {
    "029C",
    "033",
    "136",
    "303",
    "321",
    "511",
    "514",
    "505",  # 505 -> Budynek 40
}

BUILDING_30 = {
    "159",
    "163",
    "416",
    "500",
    "501",
    "521",
    "701A",
    "708",
    "k5/k7",
}

OTHER_LABS = {
    "Lab Maszynowe 11",
}


def _normalize_lab_number(value: str) -> str:
    if not value:
        return ""
    value = unquote(str(value)).strip()
    if "(" in value:
        value = value.split("(", 1)[0].strip()
    return value


def get_building(lab_number: str) -> str:
    """
    Zwraca klucz grupy: Budynek_30 / Budynek_40 / Inne
    (bez spacji — zgodne z szablonem g.Budynek_30, g.Budynek_40)
    """
    raw = unquote(str(lab_number)).strip()
    norm = _normalize_lab_number(raw)

    if raw in OTHER_LABS or norm in OTHER_LABS:
        return "Inne"
    if norm in BUILDING_40:
        return "Budynek_40"
    if norm in BUILDING_30:
        return "Budynek_30"

    # nowe / nieznane laboratoria -> Inne
    return "Inne"


def _labs_for_software(software: Software) -> list[str]:
    qs = (
        SoftwareInstallation.objects.filter(software=software, status="installed")
        .select_related("laboratory")
    )
    labs = []
    for x in qs:
        if x.laboratory and x.laboratory.number:
            labs.append(str(x.laboratory.number).strip())
    return sorted(set(labs))


def _group_labs_by_building(labs: list[str]) -> dict:
    grouped = {
        "Budynek_30": [],
        "Budynek_40": [],
        "Inne": [],
    }
    for lab in labs:
        grouped[get_building(lab)].append(lab)

    for k in grouped:
        grouped[k] = sorted(grouped[k])

    return grouped


def software_list_view(request):
    q = request.GET.get("q", "").strip()

    qs = Software.objects.all().order_by("name")
    if q:
        qs = qs.filter(name__icontains=q)

    items = []
    for s in qs:
        labs = _labs_for_software(s)
        grouped = _group_labs_by_building(labs)
        items.append(
            {
                "id": s.id,
                "name": s.name,
                "grouped_labs": grouped,
            }
        )

    return render(
        request,
        "educational_software/software_list.html",
        {"items": items, "q": q},
    )


def software_detail_view(request, software_id: int):
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


def laboratory_detail_view(request, number: str):
    raw_number = unquote(str(number)).strip()
    lab = get_object_or_404(Laboratory, number=raw_number)

    qs = (
        SoftwareInstallation.objects.filter(laboratory=lab, status="installed")
        .select_related("software")
        .order_by("software__name")
    )
    softwares = [x.software for x in qs]

    return render(
        request,
        "educational_software/laboratory_detail.html",
        {
            "laboratory": lab,
            "building": get_building(raw_number),
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
