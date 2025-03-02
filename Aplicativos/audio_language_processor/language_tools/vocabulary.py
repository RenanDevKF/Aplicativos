import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from typing import List, Dict, Any

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
        self.text = text
        self.language = language
        
        self.lang_map = {
            "en": "english", "en-US": "english", "en-GB": "english",
            "pt": "portuguese", "pt-BR": "portuguese", "es": "spanish",
            "fr": "french", "de": "german", "it": "italian", "nl": "dutch",
            "ru": "russian"
        }
        
        self.nltk_language = self.lang_map.get(language, language)
        
        try:
            self.stop_words = set(stopwords.words(self.nltk_language))
        except Exception as e:
            self.stop_words = set(stopwords.words('english'))
            print(f"Erro ao carregar stopwords para {language}: {e}. Usando inglês como fallback.")

    def extract_vocabulary(self, include_stopwords: bool = False, min_word_length: int = 2) -> List[Dict[str, Any]]:
        try:
            cleaned_text = self._clean_text(self.text)
            tokens = word_tokenize(cleaned_text)
            filtered_tokens = [token.lower() for token in tokens if token.isalpha() and len(token) >= min_word_length and (include_stopwords or token.lower() not in self.stop_words)]
            
            freq_dist = FreqDist(filtered_tokens)
            total_words = len(filtered_tokens)
            
            return [{
                "word": word,
                "count": count,
                "frequency": count / total_words if total_words > 0 else 0,
                "length": len(word)
            } for word, count in freq_dist.most_common()]
        except Exception as e:
            print(f"Erro ao extrair vocabulário: {e}")
            return []

    def identify_phrases(self, min_occurrences: int = 2, max_phrase_length: int = 4) -> List[Dict[str, Any]]:
        try:
            cleaned_text = self._clean_text(self.text)
            tokens = word_tokenize(cleaned_text)
            phrases = []
            
            for n in range(2, max_phrase_length + 1):
                ngrams = self._extract_ngrams(tokens, n)
                ngram_freq = FreqDist(ngrams)
                
                for ngram, count in ngram_freq.items():
                    if count >= min_occurrences:
                        phrases.append({"phrase": " ".join(ngram), "count": count, "length": len(ngram)})
            
            return sorted(phrases, key=lambda x: x["count"], reverse=True)
        except Exception as e:
            print(f"Erro ao identificar frases: {e}")
            return []

    def _clean_text(self, text: str) -> str:
        try:
            text = re.sub(r'[^\w\s.!?]', '', text)
            text = re.sub(r'\s+', ' ', text).strip()
            return text
        except Exception as e:
            print(f"Erro ao limpar o texto: {e}")
            return ""
    
    def _extract_ngrams(self, tokens: List[str], n: int) -> List[tuple]:
        try:
            return [tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1) if all(token.isalpha() for token in tokens[i:i+n])]
        except Exception as e:
            print(f"Erro ao extrair n-gramas: {e}")
            return []
