from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Przekierowanie /baza/ → login
from equipment.views_auth import login_view

urlpatterns = [
    path("admin/", admin.site.urls),

    # Strona logowania
    path("baza/login/", login_view, name="login"),

    # Aplikacja equipment (sprzęt)
    path("baza/", include("equipment.urls")),
]

# Serwowanie statycznych plików w trybie DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)