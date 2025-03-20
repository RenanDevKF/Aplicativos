# lotofacil_analyzer/generators/frequency.py
from .base import GeradorBase
import random
import numpy as np

class GeradorFrequencia(GeradorBase):
    """Gerador baseado na frequência dos números"""
    
    def gerar(self, quantidade=1, salvar=True):
        """
        Gera apostas baseadas na frequência dos números
        
        Args:
            quantidade (int): Número de jogos a gerar
            salvar (bool): Se True, salva as apostas no banco de dados
            
        Returns:
            list: Lista de apostas geradas
        """
        # Verifica se temos o analisador de frequência
        if 'AnalisadorFrequencia' not in self.analisadores:
            raise ValueError("É necessário o analisador de frequência")
        
        # Obtém os resultados da análise de frequência
        resultados = self.analisadores['AnalisadorFrequencia']
        frequencias = resultados['contagem']
        
        # Cria uma lista ponderada com base na frequência
        numeros = list(range(1, 26))
        pesos = [frequencias[num] for num in numeros]
        
        # Normaliza os pesos
        pesos = np.array(pesos) / sum(pesos)
        
        # Gera as apostas
        apostas = []
        for _ in range(quantidade):
            # Escolhe 15 números com probabilidade proporcional à frequência
            aposta = set()
            while len(aposta) < 15:
                aposta.add(np.random.choice(numeros, p=pesos))
            
            aposta_ordenada = sorted(list(aposta))
            apostas.append(aposta_ordenada)
            
            # Salva a aposta se solicitado
            if salvar and self.usuario:
                self.salvar_aposta(aposta_ordenada)
        
        return apostas