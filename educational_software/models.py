from django.db import models


class Laboratory(models.Model):
    """
    Laboratorium (np. 033).
    Na ten moment informację o SpaceMouse robimy prosto: flaga + ładna nazwa.
    """
    number = models.CharField(max_length=32, unique=True)
    has_space_mouse = models.BooleanField(default=False)

    class Meta:
        ordering = ["number"]

    def __str__(self) -> str:
        return self.display_name

    @property
    def display_name(self) -> str:
        # Na później ustawisz has_space_mouse=True i automatycznie pokaże „(SpaceMouse)”
        return f"{self.number} (SpaceMouse)" if self.has_space_mouse else self.number


class Software(models.Model):
    """
    Oprogramowanie z kolumny A.
    """
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class SoftwareInstallation(models.Model):
    """
    Powiązanie: oprogramowanie zainstalowane w laboratorium.
    Status na przyszłość (na razie i tak będzie 'installed').
    """
    STATUS_CHOICES = [
        ("installed", "Installed"),
        ("unknown", "Unknown"),
        ("not_installed", "Not installed"),
    ]

    software = models.ForeignKey(Software, on_delete=models.CASCADE)
    laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default="installed")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("software", "laboratory")
        indexes = [
            models.Index(fields=["software", "laboratory"]),
            models.Index(fields=["laboratory", "status"]),
        ]

    def __str__(self) -> str:
        return f"{self.software} @ {self.laboratory}"