from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


def login_view(request):
    """
    Logowanie użytkownika:
    - normalne logowanie (username + password)
    - logowanie jako gość (bez hasła, z flagą w sesji)

    Po zalogowaniu ZAWSZE przechodzimy do:
    /baza/oprogramowanie/ (educational_software)
    """

    if request.method == "POST":
        action = request.POST.get("action")

        # -----------------------------
        # 1. LOGOWANIE JAKO GOŚĆ
        # -----------------------------
        if action == "guest":
            request.session["guest"] = True
            return redirect("educational_software:software_list")

        # -----------------------------
        # 2. NORMALNE LOGOWANIE
        # -----------------------------
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Nieprawidłowy login lub hasło.")
            return render(request, "sprzet/login.html")

        login(request, user)
        request.session["guest"] = False
        return redirect("educational_software:software_list")

    # -----------------------------
    # 3. METODA GET – formularz logowania
    # -----------------------------
    return render(request, "sprzet/login.html")


def logout_view(request):
    """
    Wylogowanie użytkownika:
    - czyści sesję
    - usuwa flagę guest
    - wraca do strony logowania
    """
    logout(request)
    request.session.pop("guest", None)
    return redirect("login-root")