from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .models import ApostaGerada, SorteioLotofacil
from django.http import HttpResponse
from bs4 import BeautifulSoup
from django.utils import timezone
from lotofacil_analyzer.data.processor import LotofacilDataImporter
from .analyzers.frequency import AnalisadorFrequencia
from .analyzers.gap import AnalisadorAtraso
import json
import requests
import logging

logger = logging.getLogger(__name__)


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
    try:
        # Carrega os dados usando o LotofacilDataImporter
        importer = LotofacilDataImporter()
        df = importer.importar_xlsx()
        logger.info("Dados carregados com sucesso.")
        
        # Processa os dados usando os analisadores
        analisador_frequencia = AnalisadorFrequencia(df)
        resultados_frequencia = analisador_frequencia.analisar()
        logger.info("Análise de frequência concluída.")
        
        analisador_atraso = AnalisadorAtraso(df)
        resultados_atraso = analisador_atraso.analisar()
        logger.info("Análise de atraso concluída.")
        
        # Passa os resultados completos para o template
        context = {
            'frequencia': resultados_frequencia,
            'atraso': resultados_atraso,
        }
        return render(request, 'lotofacil_analyzer/estatisticas.html', context)
    
    except FileNotFoundError:
        logger.error("Arquivo de dados não encontrado.")
        return render(request, 'lotofacil_analyzer/erro.html', {'mensagem': 'Arquivo de dados não encontrado.'})
    
    except Exception as e:
        logger.error(f"Erro ao processar os dados: {str(e)}")
        return render(request, 'lotofacil_analyzer/erro.html', {'mensagem': f"Erro ao processar os dados: {str(e)}"})

def planos(request):
    return render(request, 'planos.html')  # Certifique-se de que esse template existe

def newsletter_signup(request):
    return render(request, 'newsletter.html')  # Certifique-se de que esse template existe