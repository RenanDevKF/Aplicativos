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
from pathlib import Path
from .analyzers.combinations import AnalisadorCombinacoes
import json
import requests
import logging
import pandas as pd


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
        # Caminho relativo ao arquivo CSV
        caminho_arquivo_csv = Path(__file__).parent / 'data' / 'files' / 'base_dados.csv'
        
        # Debug: Exibe informações detalhadas
        print(f"Caminho do arquivo CSV: {caminho_arquivo_csv}")
        print(f"Arquivo existe: {caminho_arquivo_csv.exists()}")
        
        # Verifica se o arquivo existe
        if not caminho_arquivo_csv.exists():
            logger.error(f"Arquivo não encontrado: {caminho_arquivo_csv}")
            return render(request, 'lotofacil_analyzer/erro.html', {'mensagem': 'Arquivo de dados não encontrado.'})
        
        # Usa o LotofacilDataImporter para carregar e processar os dados
        print("Tentando criar LotofacilDataImporter...")
        importer = LotofacilDataImporter(file_path=caminho_arquivo_csv)
        
        print("Tentando importar CSV...")
        df = importer.importar_csv()  # Importa diretamente do CSV
        
        # Processa os dados usando os analisadores
        analisador_frequencia = AnalisadorFrequencia(df=df)
        resultados_frequencia = analisador_frequencia.analisar()
        logger.info("Análise de frequência concluída.")
        
        analisador_atraso = AnalisadorAtraso(df=df)
        resultados_atraso = analisador_atraso.analisar()
        logger.info("Análise de atraso concluída.")
        
        analisador_combinacoes = AnalisadorCombinacoes(df=df)
        resultados_combinacoes = analisador_combinacoes.analisar()
        probabilidades_combinacoes = analisador_combinacoes.calcular_probabilidades()
        logger.info("Análise de combinções concluída.")
        
        # Debug: Exibe os resultados no console
        print("Resultados Frequência:", resultados_frequencia)
        print("Resultados Atraso:", resultados_atraso)
        
        # Passa os resultados completos para o template
        context = {
            'frequencia': resultados_frequencia,
            'atraso': resultados_atraso,
            'combinacoes': {
                'resultados': resultados_combinacoes,
                'probabilidades': probabilidades_combinacoes
            }
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