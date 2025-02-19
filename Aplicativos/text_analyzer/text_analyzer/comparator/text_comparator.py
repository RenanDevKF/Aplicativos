from typing import Dict, List, Tuple, Union
import numpy as np
from collections import Counter
import re
from ..utils.text_cleaner import clean_text
from ..core.analyzer import TextAnalyzer

class TextComparator:
    """
    Classe responsável por comparar textos e calcular métricas de similaridade
    """
    def __init__(self):
        self.analyzer = TextAnalyzer()
        
    def preprocess_texts(self, text1: str, text2: str) -> Tuple[List[str], List[str]]:
        """
        Pré-processa dois textos para comparação
        
        Args:
            text1: Primeiro texto a ser processado
            text2: Segundo texto a ser processado
            
        Returns:
            Tupla contendo listas de palavras processadas para cada texto
        """
        words1 = clean_text(text1)
        words2 = clean_text(text2)
        return words1, words2
    
    def jaccard_similarity(self, text1: str, text2: str) -> float:
        """
        Calcula a similaridade de Jaccard entre dois textos
        (intersecção / união)
        
        Args:
            text1: Primeiro texto
            text2: Segundo texto
            
        Returns:
            Coeficiente de similaridade de Jaccard (0-1)
        """
        words1, words2 = self.preprocess_texts(text1, text2)
        
        # Convertendo listas para conjuntos para remover duplicatas
        set1 = set(words1)
        set2 = set(words2)
        
        # Calculando intersecção e união
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        # Evitando divisão por zero
        if union == 0:
            return 0
        
        return intersection / union