from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from lotofacil.models import JogoGerado  # Importe o modelo correto do seu app

def registrar_usuario(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")  # Redireciona para a página inicial
    else:
        form = UserCreationForm()
    return render(request, "usuarios/registro.html", {"form": form})

def login_usuario(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "usuarios/login.html", {"form": form})

def logout_usuario(request):
    logout(request)
    return redirect("login")



