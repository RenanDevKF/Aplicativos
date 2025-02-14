from typing import Dict, List
from ..utils.text_cleaner import clean_text
from ..utils.file_handler import read_file

class TextAnalyzer:
    def __init__(self):
        self.text = ""
        self.words = []
        self.word_frequencies = {}
    
    def load_text(self, text: str) -> None:
        """Carrega e prepara o texto para análise"""
        self.text = text
        self.words = clean_text(text)
        self._calculate_frequencies()
    
    def _calculate_frequencies(self) -> None:
        """Calcula a frequência de cada palavra"""
        self.word_frequencies = {}
        for word in self.words:
            self.word_frequencies[word] = self.word_frequencies.get(word, 0) + 1