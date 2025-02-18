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