from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.mail import send_mail
from django.conf import settings

class RegistroForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        widgets = {"password": forms.PasswordInput()}

def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"]
            )
            # Enviar correo de bienvenida
            send_mail(
                "Bienvenido a la plataforma",
                f"Hola {user.username}, gracias por registrarte.",
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            return redirect("login")
    else:
        form = RegistroForm()
    return render(request, "cuentas/registro.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST["username"],
            password=request.POST["password"]
        )
        if user:
            login(request, user)
            return redirect("dashboard")
    return render(request, "cuentas/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def dashboard(request):
    return render(request, "cuentas/dashboard.html")

from django.shortcuts import render

def home(request):
    return render(request, 'cuentas/home.html')
