from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from lotofacil_analyzer.models import ApostaGerada  # Importe o modelo correto do seu app
from django.contrib import messages
from .forms import RegistroForm

def registrar_usuario(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)  # Use o formulário personalizado

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Bem-vindo, {user.username}! Sua conta foi criada com sucesso.")
            return redirect("home")
        else:
            # Exibe erros específicos para cada campo
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = RegistroForm()  # Use o formulário personalizado

    return render(request, "usuarios/registro.html", {"form": form})

def login_usuario(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Usuário ou senha incorretos. Tente novamente.")
            print("Erro de login: Usuário ou senha incorretos")  # Debug

    else:
        form = AuthenticationForm()

    return render(request, "usuarios/login.html", {"form": form})

def logout_usuario(request):
    logout(request)
    return redirect("login")

@login_required
def historico_jogos(request):
    jogos = JogoGerado.objects.filter(usuario=request.user).order_by("-data_geracao")  # Pega os jogos do usuário logado
    return render(request, "usuarios/historico.html", {"jogos": jogos})
