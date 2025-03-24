# lotofacil_analyzer/analyzers/frequency.py
from .base import AnalisadorBase
import pandas as pd
import numpy as np

class AnalisadorFrequencia(AnalisadorBase):
    """Analisador de frequência de números (análise 1)"""
    
    def analisar(self):
        """Analisa a frequência de cada número nos sorteios"""
        # Verifica se o DataFrame foi carregado corretamente
        if self.df is None or self.df.empty:
            return {"erro": "DataFrame vazio ou não carregado. Verifique os dados fornecidos."}
        
        # Debug: Exibe informações sobre o DataFrame
        print("Colunas do DataFrame:", self.df.columns)
        print("Primeira linha do DataFrame:", self.df.iloc[0])
        print("Números coletados na primeira linha:", self.df.iloc[0]['numeros'])
        
        # Inicializa contadores
        frequencias = {i: 0 for i in range(1, 26)}
        
        # Conta cada número em cada sorteio
        for _, row in self.df.iterrows():
            # Coleta os números da coluna 'numeros'
            numeros = row['numeros']
            for num in numeros:
                if num in frequencias:
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
            'media': np.mean(valores_frequencias),
            'mediana': np.median(valores_frequencias),
            'desvio_padrao': np.std(valores_frequencias),
            'total_sorteios': total_sorteios
        }
        
        return self.resultados