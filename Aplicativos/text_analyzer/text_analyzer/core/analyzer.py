from typing import Dict, List
from ..utils.text_cleaner import clean_text
from ..utils.file_handler import read_file

class TextAnalyzer:
    """
    Classe para análise de textos, incluindo limpeza e cálculo de frequência de palavras.

    Atributos:
        text (str): Texto armazenado para análise.
        words (List[str]): Lista de palavras limpas extraídas do texto.
        word_frequencies (Dict[str, int]): Dicionário com a contagem de cada palavra.
    """
    
    def __init__(self):
        """Inicializa um analisador de texto vazio."""
        self.text = ""
        self.words = []
        self.word_frequencies = {}

    def load_text(self, text: str) -> None:
        """
        Carrega e prepara o texto para análise.

        O texto é armazenado, limpo utilizando `clean_text` e tem suas frequências calculadas.

        Args:
            text (str): O texto a ser analisado.

        Returns:
            None
        """
        self.text = text
        self.words = clean_text(text)
        self._calculate_frequencies()

    def _calculate_frequencies(self) -> None:
        """
        Calcula a frequência de cada palavra no texto processado.

        O resultado é armazenado no dicionário `word_frequencies`.
        
        Returns:
            None
        """
        self.word_frequencies = {}
        for word in self.words:
            self.word_frequencies[word] = self.word_frequencies.get(word, 0) + 1
