from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


def login_view(request):
    """
    Logowanie użytkownika:
    - normalne logowanie (username + password)
    - logowanie jako gość (bez hasła, z flagą w sesji)

    Szablon: templates/sprzet/login.html
    """

    if request.method == "POST":
        action = request.POST.get("action")

        # -----------------------------
        # 1. LOGOWANIE JAKO GOŚĆ
        # -----------------------------
        if action == "guest":
            # ustawiamy flagę w sesji – w szablonach będzie można odróżnić gościa
            request.session["guest"] = True
            # docelowo przekierujemy na zakładkę "Oprogramowanie"
            return redirect("oprogramowanie")

        # -----------------------------
        # 2. NORMALNE LOGOWANIE
        # -----------------------------
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Nieprawidłowy login lub hasło.")
            return render(request, "sprzet/login.html")

        # logowanie poprawne
        login(request, user)
        # upewniamy się, że to nie „gość”
        request.session["guest"] = False
        return redirect("oprogramowanie")

    # -----------------------------
    # 3. METODA GET – wyświetl formularz logowania
    # -----------------------------
    return render(request, "sprzet/login.html")


def oprogramowanie_view(request):
    """
    Docelowa strona 'Oprogramowanie' – landing po zalogowaniu
    (zarówno dla gościa, jak i zwykłego użytkownika).
    """
    return render(request, "sprzet/oprogramowanie.html")


def logout_view(request):
    """
    Wylogowanie użytkownika:
    - czyści sesję logowania Django,
    - usuwa flagę 'guest' z sesji (jeśli była),
    - przekierowuje na stronę logowania (/baza/).
    """
    logout(request)
    request.session.pop("guest", None)
    return redirect("login-root")