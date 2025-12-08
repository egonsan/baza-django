from datetime import date

from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

# ============================================================
# KATEGORIE POMIESZCZEŃ
# ============================================================

ROOM_CATEGORY_CHOICES = [
    ("LAB", "Lab. komputerowe"),
    ("SALA", "Sala wykładowa"),
    ("POKOJ", "Pokój"),
    ("INNE", "Inne"),
    ("MAGAZYN", "Magazyn"),
]


class Equipment(models.Model):
    """
    Model karty sprzętu.
    Pola są dostosowane do Twojego Excela oraz obecnego działania aplikacji.
    """

    # Podstawowe identyfikatory
    inventory_number = models.CharField(
        "Numer inwentarzowy",
        max_length=50,
        unique=True,
    )
    equipment_name = models.CharField(
        "Nazwa sprzętu",
        max_length=255,
        blank=True,
        default="",
    )
    equipment_type = models.CharField(
        "Typ sprzętu",
        max_length=100,
        blank=True,
        default="",
    )

    # Lokalizacja
    building = models.CharField(
        "Budynek",
        max_length=100,
        blank=True,
        default="",
    )

    # 🔹 NOWE POLE – Kategoria pomieszczenia (nad "Pomieszczenie")
    room_category = models.CharField(
        "Kategoria pomieszczenia",
        max_length=20,
        choices=ROOM_CATEGORY_CHOICES,
        default="MAGAZYN",  # domyślnie wszystko ląduje w Magazynie
    )

    room = models.CharField(
        "Pomieszczenie",
        max_length=100,
        blank=True,
        default="",
    )

    # Dane techniczne jednostki
    hostname = models.CharField(
        "Nazwa domenowa",
        max_length=255,
        blank=True,
        default="",
    )
    ip_address = models.CharField(
        "Adres IP",
        max_length=50,
        blank=True,
        default="",  # ważne: brak NULL w bazie
    )
    mac_address = models.CharField(
        "Adres MAC",
        max_length=50,
        blank=True,
        default="",
    )
    unit_serial_number = models.CharField(
        "Nr seryjny jednostki",
        max_length=100,
        blank=True,
        default="",
    )
    monitor_serial_number = models.CharField(
        "Nr seryjny monitora",
        max_length=100,
        blank=True,
        default="",
    )

    # System operacyjny
    os_name = models.CharField(
        "System operacyjny",
        max_length=100,
        blank=True,
        default="",
    )
    os_version = models.CharField(
        "Wersja systemu",
        max_length=100,
        blank=True,
        default="",
    )
    os_serial_key = models.CharField(
        "Klucz systemu",
        max_length=255,
        blank=True,
        default="",
    )

    # Pakiet Office
    office_name = models.CharField(
        "Pakiet Office",
        max_length=100,
        blank=True,
        default="",
    )
    office_version = models.CharField(
        "Wersja Office",
        max_length=100,
        blank=True,
        default="",
    )
    office_serial_key = models.CharField(
        "Klucz MS Office",
        max_length=255,
        blank=True,
        default="",
    )

    # Użytkownik / wypożyczenia
    user_full_name = models.CharField(
        "Użytkownik (nazwisko i imię)",
        max_length=255,
        blank=True,
        default="",
    )
    borrowed_to = models.CharField(
        "Wypożyczono do",
        max_length=255,
        blank=True,
        default="",
    )

    # Status / dostawca / zakup / gwarancja
    status = models.CharField(
        "Status",
        max_length=100,
        blank=True,
        default="",
    )
    supplier = models.CharField(
        "Dostawca",
        max_length=255,
        blank=True,
        default="",
    )

    # DATA_ZAKUP z Excela
    purchase_date = models.DateField(
        "Data zakupu",
        null=True,
        blank=True,
    )

    warranty_until = models.DateField(
        "Gwarancja do",
        null=True,
        blank=True,
    )

    # Dodatkowe informacje
    notes = models.TextField(
        "Uwagi",
        blank=True,
        default="",
    )

    # Kto / kiedy ostatnio zmodyfikował kartę
    last_modified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="modified_equipment",
        verbose_name="Ostatnio modyfikował",
    )
    last_modified_at = models.DateTimeField(
        "Ostatnia modyfikacja",
        auto_now=True,
        null=True,
        blank=True,
    )

    def warranty_status(self):
        """
        Metoda używana w adminie w list_display jako 'warranty_status'.
        Zwraca prostą informację tekstową.
        """
        if not self.warranty_until:
            return "brak danych"

        today = date.today()
        if self.warranty_until >= today:
            return "na gwarancji"
        return "po gwarancji"

    warranty_status.short_description = "Status gwarancji"
    warranty_status.admin_order_field = "warranty_until"

    def __str__(self):
        """
        W adminie ma być:
        'Change Karta sprzętu : 30149850000'
        dlatego zwracamy tylko numer inwentarzowy.
        """
        return self.inventory_number or ""

    class Meta:
        verbose_name = "Karta sprzętu"
        verbose_name_plural = "Karty sprzętu"
        ordering = ["inventory_number"]


class EquipmentAttachment(models.Model):
    """
    Załącznik powiązany z kartą sprzętu.
    """

    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name="attachments",
        verbose_name="Karta sprzętu",
    )
    file = models.FileField(
        "Plik",
        upload_to="equipment_attachments/",
    )
    description = models.CharField(
        "Opis (opcjonalnie)",
        max_length=255,
        blank=True,
    )
    uploaded_at = models.DateTimeField(
        "Dodano",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Załącznik"
        verbose_name_plural = "Załączniki"

    def __str__(self):
        # pokazujemy samą nazwę pliku, bez ścieżki
        return self.file.name.split("/")[-1] if self.file.name else "Załącznik"