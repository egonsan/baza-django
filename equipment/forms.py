from django import forms
from .models import Equipment


class EquipmentForm(forms.ModelForm):
    """
    Formularz do edycji karty sprzętu.
    Na razie prosty – później go "upiększymy" i dodamy np. przyciski KOPIUJ.
    """

    class Meta:
        model = Equipment
        # Na start edytujemy WSZYSTKIE pola – potem zawęzimy, jak będzie potrzeba.
        fields = "__all__"

        widgets = {
            # Daty jako ładne pickery
            "purchase_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "warranty_until": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            # Notatki jako większe pole
            "notes": forms.Textarea(
                attrs={"rows": 4, "class": "form-control"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Prosty "bootstrapopodobny" wygląd – wszystkie pola dostają klasę CSS
        for name, field in self.fields.items():
            existing_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (existing_classes + " form-control").strip()

        # Pola tylko do odczytu (informacyjne)
        for readonly_name in ["created_at", "updated_at"]:
            if readonly_name in self.fields:
                self.fields[readonly_name].widget.attrs["readonly"] = True
                self.fields[readonly_name].widget.attrs["style"] = (
                    "background-color: #eee;"
                )

        # last_modified_by ustawimy automatycznie w widoku – tu można ukryć z formularza
        if "last_modified_by" in self.fields:
            self.fields["last_modified_by"].widget.attrs["readonly"] = True
            self.fields["last_modified_by"].widget.attrs["style"] = (
                "background-color: #eee;"
            )
