# lotofacil_analyzer/analyzers/frequency.py
from .base import AnalisadorBase
import pandas as pd
import numpy as np

class AnalisadorFrequencia(AnalisadorBase):
    """Analisador de frequência de números (análise 1)"""
    
    def analisar(self):
        """Analisa a frequência de cada número nos sorteios"""
        # Inicializa contadores
        frequencias = {i: 0 for i in range(1, 26)}
        
        # Conta cada número em cada sorteio
        for _, row in self.df.iterrows():
            for num in row['numeros']:
                frequencias[num] += 1
        
        # Calcula percentuais
        total_sorteios = len(self.df)
        if total_sorteios == 0:
            return {"erro": "Nenhum sorteio encontrado. Verifique os dados fornecidos."}
        percentuais = {num: (freq / total_sorteios) * 100 
                      for num, freq in frequencias.items()}
        
        # Ordena os resultados
        mais_frequentes = sorted(frequencias.items(), key=lambda x: x[1], reverse=True)
        menos_frequentes = sorted(frequencias.items(), key=lambda x: x[1])
        
        # Armazena os resultados
        valores_frequencias = list(frequencias.values())
        self.resultados = {
            'contagem': frequencias,
            'percentuais': percentuais,
            'mais_frequentes': mais_frequentes[:5],
            'menos_frequentes': menos_frequentes[:5],
            'media': np.mean(list(frequencias.values())),
            'mediana': np.median(list(frequencias.values())),
            'desvio_padrao': np.std(list(frequencias.values())),
            'total_sorteios': total_sorteios
        }
        
        return self.resultados