from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .models import ApostaGerada, SorteioLotofacil
from django.http import HttpResponse
from bs4 import BeautifulSoup
from django.utils import timezone
import json
import requests


def home(request):
    return render(request, 'lotofacil_analyzer/home.html')

from django.http import HttpResponse
@login_required
def criar_jogo(request):
    
    return HttpResponse("Página de criação de jogo")

def gerar_jogo_rapido(request):
    return HttpResponse("Jogo rápido gerado!")

def resultados(request):
    # Obtém todos os concursos (ou filtra conforme necessário)
    concursos = SorteioLotofacil.objects.all().order_by('-numero')

    # Passa os concursos para o template
    return render(request, 'lotofacil_analyzer/resultados.html', {'concursos': concursos})


def estatisticas(request):
    return render(request, 'lotofacil_analyzer/estatisticas.html')  # Certifique-se de que esse template existe

def planos(request):
    return render(request, 'planos.html')  # Certifique-se de que esse template existe

def newsletter_signup(request):
    return render(request, 'newsletter.html')  # Certifique-se de que esse template existe