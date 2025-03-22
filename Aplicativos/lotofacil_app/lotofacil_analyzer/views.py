from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .models import ApostaGerada, SorteioLotofacil
from django.http import HttpResponse
from bs4 import BeautifulSoup
from django.utils import timezone
from .data.processor import load_data
from .analyzers.frequency import AnalisadorFrequencia
from .analyzers.gap import AnalisadorAtraso
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
    # Carrega os dados
    df = load_data()
    
    # Processa os dados usando os analisadores
    analisador_frequencia = AnalisadorFrequencia(df)
    resultados_frequencia = analisador_frequencia.analisar()
    
    analisador_atraso = AnalisadorAtraso(df)  # Exemplo de outro analisador
    resultados_atraso = analisador_atraso.analisar()
    
    # Passa os resultados para o template
    context = {
        'frequencia': {
            'mais_frequentes': resultados_frequencia['mais_frequentes'],
            'menos_frequentes': resultados_frequencia['menos_frequentes'],
            'percentuais': resultados_frequencia['percentuais'],
        },
        'atraso': {
            'ranking_atrasos': resultados_atraso['ranking_atrasos'],
            'estatisticas': resultados_atraso['estatisticas'],
        },
    }
    return render(request, 'lotofacil_analyzer/estatisticas.html', context)

def planos(request):
    return render(request, 'planos.html')  # Certifique-se de que esse template existe

def newsletter_signup(request):
    return render(request, 'newsletter.html')  # Certifique-se de que esse template existe