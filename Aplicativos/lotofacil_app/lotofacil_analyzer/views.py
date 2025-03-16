from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'lotofacil_analyzer/home.html')

from django.http import HttpResponse

def criar_jogo(request):
    return HttpResponse("Página de criação de jogo")

def gerar_jogo_rapido(request):
    return HttpResponse("Jogo rápido gerado!")

def resultados(request):
    return render(request, 'resultados.html')  # Certifique-se de que esse template existe

def estatisticas(request):
    return render(request, 'estatisticas.html')  # Certifique-se de que esse template existe
