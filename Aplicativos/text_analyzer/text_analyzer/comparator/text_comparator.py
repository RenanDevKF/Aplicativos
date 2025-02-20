from typing import Dict, List, Tuple, Union
import numpy as np
from collections import Counter
import re
from ..utils.text_cleaner import clean_text
from ..utils.file_handler import read_file
from ..utils.web_handler import fetch_webpage_text

class TextComparator:
    """
    Classe responsável por comparar textos e calcular métricas de similaridade.
    
    Essa classe permite carregar e processar textos, além de calcular métricas de similaridade
    como Jaccard e Cosseno. Também pode identificar termos comuns e exclusivos entre dois textos.
    """

    def load_text(self, file_path: str, job_url: str) -> Tuple[str, str]:
        """
        Carrega textos do currículo e da vaga de emprego.

        Args:
            file_path (str): Caminho do arquivo contendo o currículo.
            job_url (str): URL da página com a descrição da vaga.

        Returns:
            Tuple[str, str]: Tupla contendo o texto do currículo e o da vaga.
        """
        resume_text = read_file(file_path)
        job_text = fetch_webpage_text(job_url)
        return resume_text, job_text

    def preprocess_texts(self, text1: str, text2: str) -> Tuple[List[str], List[str]]:
        """
        Pré-processa dois textos para comparação.

        Aplica limpeza básica dos textos e os converte em listas de palavras.

        Args:
            text1 (str): Primeiro texto a ser processado.
            text2 (str): Segundo texto a ser processado.

        Returns:
            Tuple[List[str], List[str]]: Tupla contendo listas de palavras processadas para cada texto.
        """
        words1 = clean_text(text1)
        words2 = clean_text(text2)
        return words1, words2

    def jaccard_similarity(self, text1: str, text2: str) -> float:
        """
        Calcula a similaridade de Jaccard entre dois textos.

        Essa métrica é definida como o tamanho da interseção dividido pelo tamanho da união dos conjuntos de palavras.

        Args:
            text1 (str): Primeiro texto.
            text2 (str): Segundo texto.

        Returns:
            float: Coeficiente de similaridade de Jaccard (0 a 1), onde 1 indica textos idênticos.
        """
        words1, words2 = self.preprocess_texts(text1, text2)
        set1, set2 = set(words1), set(words2)

        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))

        return intersection / union if union != 0 else 0

    def cosine_similarity(self, text1: str, text2: str) -> float:
        """
        Calcula a similaridade do cosseno entre dois textos.

        Essa métrica mede a similaridade angular entre vetores de frequência de palavras.

        Args:
            text1 (str): Primeiro texto.
            text2 (str): Segundo texto.

        Returns:
            float: Coeficiente de similaridade do cosseno (0 a 1), onde 1 indica textos idênticos.
        """
        words1, words2 = self.preprocess_texts(text1, text2)

        counter1, counter2 = Counter(words1), Counter(words2)
        all_words = set(counter1.keys()).union(counter2.keys())

        vec1 = [counter1.get(word, 0) for word in all_words]
        vec2 = [counter2.get(word, 0) for word in all_words]

        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        return float(np.dot(vec1, vec2) / (norm1 * norm2)) if norm1 and norm2 else 0.0

    def get_common_terms(self, text1: str, text2: str, top_n: int = 10) -> List[str]:
        """
        Obtém os termos mais comuns entre dois textos.

        Args:
            text1 (str): Primeiro texto.
            text2 (str): Segundo texto.
            top_n (int): Número de termos comuns a retornar.

        Returns:
            List[str]: Lista dos termos mais frequentes entre os dois textos.
        """
        words1, words2 = self.preprocess_texts(text1, text2)
        common_terms = set(words1) & set(words2)

        counter1, counter2 = Counter(words1), Counter(words2)
        common_counter = {term: counter1[term] + counter2[term] for term in common_terms}

        return [term for term, _ in sorted(common_counter.items(), key=lambda x: x[1], reverse=True)[:top_n]]

    def get_unique_terms(self, text1: str, text2: str, from_first: bool = True, top_n: int = 10) -> List[str]:
        """
        Obtém os termos exclusivos de um texto em relação ao outro.

        Args:
            text1 (str): Primeiro texto.
            text2 (str): Segundo texto.
            from_first (bool): Se True, retorna termos únicos do primeiro texto. Se False, do segundo.
            top_n (int): Número de termos únicos a retornar.

        Returns:
            List[str]: Lista dos termos únicos mais frequentes.
        """
        words1, words2 = self.preprocess_texts(text1, text2)
        unique_words = set(words1) - set(words2) if from_first else set(words2) - set(words1)

        counter = Counter(words1) if from_first else Counter(words2)
        unique_counter = {term: counter[term] for term in unique_words}

        return [term for term, _ in sorted(unique_counter.items(), key=lambda x: x[1], reverse=True)[:top_n]]

    def compare_documents(self, file_path: str, job_url: str) -> Dict[str, Union[float, List[str], str]]:
        """
        Realiza uma comparação completa entre um currículo e uma vaga de emprego.

        Args:
            file_path (str): Caminho do arquivo do currículo.
            job_url (str): URL contendo a descrição da vaga.

        Returns:
            Dict[str, Union[float, List[str], str]]: Dicionário contendo métricas de similaridade e análise textual.
        """
        resume_text, job_text = self.load_text(file_path, job_url)

        jaccard = self.jaccard_similarity(resume_text, job_text)
        cosine = self.cosine_similarity(resume_text, job_text)

        result = {
            'jaccard_similarity': jaccard,
            'cosine_similarity': cosine,
            'common_terms': self.get_common_terms(resume_text, job_text),
            'unique_terms_resume': self.get_unique_terms(resume_text, job_text, from_first=True),
            'unique_terms_job': self.get_unique_terms(resume_text, job_text, from_first=False),
            'match_level': 'Alto' if (jaccard + cosine) / 2 > 0.7 else 'Médio' if (jaccard + cosine) / 2 > 0.4 else 'Baixo'
        }
        return result
