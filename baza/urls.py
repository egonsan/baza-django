from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Widok logowania
from equipment.views_auth import login_view

urlpatterns = [
    path("admin/", admin.site.urls),

    # /baza/ → strona logowania
    path("baza/", login_view, name="login-root"),

    # /baza/login/ → też strona logowania (drugi alias)
    path("baza/login/", login_view, name="login"),

    # Pozostałe adresy aplikacji (oprogramowanie, magazyn, pomieszczenia, pracownicy...)
    path("baza/", include("equipment.urls")),
]

# Serwowanie statycznych plików i mediów w trybie DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)