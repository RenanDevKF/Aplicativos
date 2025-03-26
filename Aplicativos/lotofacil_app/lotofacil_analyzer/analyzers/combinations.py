# lotofacil_analyzer/analyzers/combinations.py
from .base import AnalisadorBase
from itertools import combinations
from collections import Counter
import pandas as pd

class AnalisadorCombinacoes(AnalisadorBase):
    def __init__(self, df=None, arquivo_excel=None, ultimos_n=None):
        super().__init__(df, arquivo_excel, ultimos_n)
        
    def analisar(self, tamanhos_combinacoes=[2, 3, 4, 5]):
        """
        Analisa as combinações mais frequentes nos sorteios.
        
        Args:
            tamanhos_combinacoes (list): Tamanhos das combinações a serem analisadas
        
        Returns:
            dict: Resultados da análise de combinações
        """
        resultados = {}
        
        for tamanho in tamanhos_combinacoes:
            todas_combinacoes = []
            
            # Extrai combinações de cada sorteio
            for numeros in self.df['numeros']:
                # Gera todas as combinações de 'tamanho' números para cada sorteio
                combinacoes_sorteio = list(combinations(sorted(numeros), tamanho))
                todas_combinacoes.extend(combinacoes_sorteio)
            
            # Conta a frequência das combinações
            frequencia_combinacoes = Counter(todas_combinacoes)
            
            # Ordena as combinações por frequência (do mais frequente para o menos)
            top_combinacoes = sorted(
                frequencia_combinacoes.items(), 
                key=lambda x: x[1], 
                reverse=True
            )
            
            # Armazena os resultados
            resultados[f'combinacoes_{tamanho}'] = {
                'top_10': top_combinacoes[:10],
                'total_combinacoes': len(frequencia_combinacoes),
                'frequencia_maxima': max(frequencia_combinacoes.values()) if frequencia_combinacoes else 0
            }
        
        self.resultados = resultados
        return resultados
    
    def calcular_probabilidades(self):
        """
        Calcula probabilidades das combinações mais frequentes.
        
        Returns:
            dict: Probabilidades das combinações
        """
        if not self.resultados:
            self.analisar()
        
        probabilidades = {}
        total_sorteios = len(self.df)
        
        for tamanho, dados in self.resultados.items():
            top_combinacoes = dados['top_10']
            probabilidades[tamanho] = [
                {
                    'combinacao': list(combinacao),
                    'frequencia': freq,
                    'probabilidade': round((freq / total_sorteios) * 100, 2)
                } 
                for combinacao, freq in top_combinacoes
            ]
        
        return probabilidades