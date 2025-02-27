# Analisa vocabulario e frequencia

import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from typing import List, Dict, Any, Optional

# Garantir que os recursos necessários do NLTK estejam disponíveis
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

class VocabularyAnalyzer:
    """Classe para analisar vocabulário em textos para estudo de idiomas."""
    
    def __init__(self, text: str, language: str = "english"):
        """
        Inicializa o analisador de vocabulário.
        
        Args:
            text: Texto a ser analisado
            language: Idioma do texto (para stopwords e processamento)
        """
        self.text = text
        self.language = language
        
        # Mapeamento de códigos de idioma
        self.lang_map = {
            "en": "english",
            "en-US": "english",
            "en-GB": "english",
            "pt": "portuguese",
            "pt-BR": "portuguese",
            "es": "spanish",
            "fr": "french",
            "de": "german",
            "it": "italian",
            "nl": "dutch",
            "ru": "russian"
        }
        
        # Normalizar código de idioma
        self.nltk_language = self.lang_map.get(language, language)
        
        # Carregar stopwords do idioma se disponível
        try:
            self.stop_words = set(stopwords.words(self.nltk_language))
        except:
            # Fallback para inglês se o idioma não estiver disponível
            self.stop_words = set(stopwords.words('english'))
            print(f"Stopwords para {language} não disponíveis. Usando inglês como fallback.")
            
    