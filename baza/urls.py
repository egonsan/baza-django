from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from equipment.views_auth import login_view, logout_view

urlpatterns = [
    path("admin/", admin.site.urls),

    # Strona logowania – główny root /baza/
    path("baza/", login_view, name="login-root"),

    # Strona logowania (alias)
    path("baza/login/", login_view, name="login"),

    # Wylogowanie
    path("baza/logout/", logout_view, name="logout"),

    # OPROGRAMOWANIE (NOWE) – publiczny widok listy + szczegóły
    # /baza/oprogramowanie/
    path("baza/oprogramowanie/", include("educational_software.urls")),

    # Aplikacja equipment (sprzęt, magazyn, pomieszczenia, pracownicy, import/eksport sprzętu)
    path("baza/", include("equipment.urls")),
]

# Serwowanie plików statycznych i mediów w trybie DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
