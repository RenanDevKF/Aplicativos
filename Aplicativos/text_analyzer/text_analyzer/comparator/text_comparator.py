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
    
    import numpy as np
from collections import Counter

def cosine_similarity(self, text1: str, text2: str) -> float:
    """
    Calcula a similaridade do cosseno entre dois textos.

    Args:
        text1: Primeiro texto
        text2: Segundo texto

    Returns:
        Coeficiente de similaridade do cosseno (0 a 1)
    """
    words1, words2 = self.preprocess_texts(text1, text2)

    # Criando contadores de palavras
    counter1 = Counter(words1)
    counter2 = Counter(words2)

    # Obtendo todas as palavras únicas
    all_words = set(counter1.keys()).union(set(counter2.keys()))

    # Criando vetores de frequência
    vec1 = [counter1.get(word, 0) for word in all_words]
    vec2 = [counter2.get(word, 0) for word in all_words]

    # Calculando norma dos vetores
    norm1 = np.sqrt(sum(val ** 2 for val in vec1))
    norm2 = np.sqrt(sum(val ** 2 for val in vec2))

    # Evitando divisão por zero
    if norm1 == 0 or norm2 == 0:
        return 0.0

    # Calculando o produto escalar dos vetores
    dot_product = sum(v1 * v2 for v1, v2 in zip(vec1, vec2))

    # Calculando e retornando a similaridade do cosseno
    return dot_product / (norm1 * norm2)

def get_common_terms(self, text1: str, text2: str, top_n: int = 10) -> List[str]:
        """
        Obtém os termos mais comuns entre dois textos
        
        Args:
            text1: Primeiro texto
            text2: Segundo texto
            top_n: Número de termos comuns a retornar
            
        Returns:
            Lista dos top_n termos mais comuns entre os textos
        """
        words1, words2 = self.preprocess_texts(text1, text2)
        
        # Convertendo listas para conjuntos
        set1 = set(words1)
        set2 = set(words2)
        
        # Encontrando intersecção
        common_terms = set1.intersection(set2)
        
        # Contando frequência dos termos comuns em ambos os textos
        counter1 = Counter(words1)
        counter2 = Counter(words2)
        
        # Somando frequências
        common_counter = {term: counter1[term] + counter2[term] for term in common_terms}
        
        # Ordenando por frequência
        sorted_terms = sorted(common_counter.items(), key=lambda x: x[1], reverse=True)
        
        return [term for term, count in sorted_terms[:top_n]]

def get_unique_terms(self, text1: str, text2: str, from_first: bool = True, top_n: int = 10) -> List[str]:
        """
        Obtém os termos únicos de um texto em relação ao outro
        
        Args:
            text1: Primeiro texto
            text2: Segundo texto
            from_first: Se True, retorna termos únicos do primeiro texto. Se False, do segundo.
            top_n: Número de termos únicos a retornar
            
        Returns:
            Lista dos top_n termos únicos mais frequentes
        """
        words1, words2 = self.preprocess_texts(text1, text2)
        
        if from_first:
            # Termos que estão em words1 mas não em words2
            unique_set = set(words1) - set(words2)
            counter = Counter(words1)
        else:
            # Termos que estão em words2 mas não em words1
            unique_set = set(words2) - set(words1)
            counter = Counter(words2)
        
        # Filtrando o contador para incluir apenas termos únicos
        unique_counter = {term: counter[term] for term in unique_set}
        
        # Ordenando por frequência
        sorted_terms = sorted(unique_counter.items(), key=lambda x: x[1], reverse=True)
        
        return [term for term, count in sorted_terms[:top_n]]   