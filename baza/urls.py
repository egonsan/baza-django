from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Widok logowania
from equipment.views_auth import login_view

urlpatterns = [
    # Panel administracyjny Django
    path("admin/", admin.site.urls),

    # Główna strona /baza/ → okno logowania
    path("baza/", login_view, name="login-root"),

    # Alternatywny adres logowania (np. do linków)
    path("baza/login/", login_view, name="login"),

    # Aplikacja equipment (sprzęt, magazyn, pomieszczenia, oprogramowanie itd.)
    # Wszystkie adresy typu /baza/..., które nie są powyżej, idą do equipment.urls
    path("baza/", include("equipment.urls")),
]

# Serwowanie statycznych plików w trybie DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)