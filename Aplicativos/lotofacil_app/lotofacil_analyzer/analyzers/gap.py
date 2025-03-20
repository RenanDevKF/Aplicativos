# lotofacil_analyzer/analyzers/gap.py
from .base import AnalisadorBase
import pandas as pd
import numpy as np

class AnalisadorAtraso(AnalisadorBase):
    """Analisador de atraso de números (análise 2)"""
    
    def analisar(self):
        """Analisa há quanto tempo cada número não é sorteado"""
        # Ordena os sorteios do mais recente para o mais antigo
        sorteios_ordenados = self.df.sort_values('concurso', ascending=False)
        
        # Inicializa o dicionário de atrasos
        atrasos_atuais = {i: 0 for i in range(1, 26)}
        historico_atrasos = {i: [] for i in range(1, 26)}
        ultimo_sorteio = {i: None for i in range(1, 26)}
        
        # Percorre os sorteios e calcula os atrasos
        for idx, row in sorteios_ordenados.iterrows():
            concurso = row['concurso']
            numeros = row['numeros']
            
            # Atualiza o atraso para cada número
            for num in range(1, 26):
                if num in numeros:
                    # Se o número foi sorteado, registra o atraso atual e zera
                    if atrasos_atuais[num] > 0:
                        historico_atrasos[num].append(atrasos_atuais[num])
                    atrasos_atuais[num] = 0
                    ultimo_sorteio[num] = concurso
                else:
                    # Se não foi sorteado, incrementa o atraso
                    atrasos_atuais[num] += 1
        
        # Calcula estatísticas dos atrasos históricos
        estatisticas_atrasos = {}
        for num in range(1, 26):
            if historico_atrasos[num]:
                estatisticas_atrasos[num] = {
                    'media': np.mean(historico_atrasos[num]),
                    'maximo': np.max(historico_atrasos[num]),
                    'minimo': np.min(historico_atrasos[num]),
                    'atual': atrasos_atuais[num],
                    'ultimo_sorteio': ultimo_sorteio[num]
                }
            else:
                estatisticas_atrasos[num] = {
                    'media': 0,
                    'maximo': 0,
                    'minimo': 0,
                    'atual': atrasos_atuais[num],
                    'ultimo_sorteio': ultimo_sorteio[num]
                }
        
        # Ordena os números por atraso atual
        numeros_por_atraso = sorted(atrasos_atuais.items(), key=lambda x: x[1], reverse=True)
        
        self.resultados = {
            'atrasos_atuais': atrasos_atuais,
            'estatisticas': estatisticas_atrasos,
            'ranking_atrasos': numeros_por_atraso,
            'maior_atraso_atual': numeros_por_atraso[0] if numeros_por_atraso else None,
            'menor_atraso_atual': numeros_por_atraso[-1] if numeros_por_atraso else None
        }
        
        return self.resultados