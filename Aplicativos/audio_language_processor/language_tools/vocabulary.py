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
    """
    Classe para analisar vocabulário em textos para estudo de idiomas.
    """
    
    def __init__(self, text: str, language: str = "english"):
        """
        Inicializa o analisador de vocabulário.
        
        Args:
            text (str): Texto a ser analisado.
            language (str): Idioma do texto (para stopwords e processamento).
        """
        self.text = text
        self.language = language
        
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
        
        self.nltk_language = self.lang_map.get(language, language)
        
        try:
            self.stop_words = set(stopwords.words(self.nltk_language))
        except:
            self.stop_words = set(stopwords.words('english'))
            print(f"Stopwords para {language} não disponíveis. Usando inglês como fallback.")
            
    def extract_vocabulary(self, include_stopwords: bool = False, 
                           min_word_length: int = 2) -> List[Dict[str, Any]]:
        """
        Extrai e analisa o vocabulário do texto.
        
        Args:
            include_stopwords (bool): Se True, inclui palavras comuns (stopwords).
            min_word_length (int): Tamanho mínimo de palavra para incluir na análise.
            
        Returns:
            List[Dict[str, Any]]: Lista de dicionários com palavras e suas estatísticas.
        """
        cleaned_text = self._clean_text(self.text)
        tokens = word_tokenize(cleaned_text)
        
        filtered_tokens = []
        for token in tokens:
            if (len(token) >= min_word_length and 
                token.isalpha() and
                (include_stopwords or token.lower() not in self.stop_words)):
                filtered_tokens.append(token.lower())
        
        freq_dist = FreqDist(filtered_tokens)
        total_words = len(filtered_tokens)
        
        vocabulary = []
        for word, count in freq_dist.most_common():
            vocabulary.append({
                "word": word,
                "count": count,
                "frequency": count / total_words if total_words > 0 else 0,
                "length": len(word)
            })
        
        return vocabulary
    
    def identify_phrases(self, min_occurrences: int = 2, 
                         max_phrase_length: int = 4) -> List[Dict[str, Any]]:
        """
        Identifica frases e expressões recorrentes no texto.
        
        Args:
            min_occurrences (int): Número mínimo de ocorrências para considerar uma frase.
            max_phrase_length (int): Número máximo de palavras na frase.
            
        Returns:
            List[Dict[str, Any]]: Lista de dicionários com frases e suas estatísticas.
        """
        cleaned_text = self._clean_text(self.text)
        tokens = word_tokenize(cleaned_text)
        
        phrases = []
        for n in range(2, max_phrase_length + 1):
            ngrams = self._extract_ngrams(tokens, n)
            ngram_freq = FreqDist(ngrams)
            
            for ngram, count in ngram_freq.items():
                if count >= min_occurrences:
                    phrase = " ".join(ngram)
                    phrases.append({
                        "phrase": phrase,
                        "count": count,
                        "length": len(ngram)
                    })
        
        phrases.sort(key=lambda x: x["count"], reverse=True)
        
        return phrases
    
    def get_language_level_estimate(self) -> Dict[str, Any]:
        """
        Estima o nível de dificuldade do vocabulário.
        
        Returns:
            Dict[str, Any]: Dicionário com estimativa de nível de idioma e estatísticas.
        """
        vocab = self.extract_vocabulary(include_stopwords=True)
        
        if not vocab:
            return {
                "level": "indeterminado",
                "confidence": 0.0,
                "reason": "Texto muito curto ou sem palavras reconhecíveis"
            }
        
        word_lengths = [v["length"] for v in vocab]
        avg_word_length = sum(word_lengths) / len(word_lengths)
        
        unique_words = len(vocab)
        cleaned_text = self._clean_text(self.text)
        tokens = word_tokenize(cleaned_text)
        sentences = [s.strip() for s in re.split(r'[.!?]', cleaned_text) if s.strip()]
        
        avg_sentence_length = len(tokens) / len(sentences) if sentences else 0
        
        level = "iniciante"
        confidence = 0.6
        reasons = []
        
        if avg_word_length > 6.5:
            level = "avançado"
            reasons.append(f"Palavras longas (média: {avg_word_length:.1f} caracteres)")
        elif avg_word_length > 5.5:
            level = "intermediário"
            reasons.append(f"Palavras de comprimento médio ({avg_word_length:.1f} caracteres)")
        else:
            reasons.append(f"Palavras curtas (média: {avg_word_length:.1f} caracteres)")
        
        confidence = min(confidence, 1.0)
        
        return {
            "level": level,
            "confidence": confidence,
            "reasons": reasons,
            "stats": {
                "unique_words": unique_words,
                "avg_word_length": avg_word_length,
                "avg_sentence_length": avg_sentence_length,
                "total_words": len(tokens),
                "total_sentences": len(sentences)
            }
        }
        
    def _clean_text(self, text: str) -> str:
        """
        Limpa o texto para análise.
        
        Args:
            text (str): Texto a ser limpo.
            
        Returns:
            str: Texto limpo.
        """
        text = re.sub(r'[^\w\s.!?]', '', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _extract_ngrams(self, tokens: List[str], n: int) -> List[tuple]:
        """
        Extrai n-gramas (sequências de n palavras) de uma lista de tokens.
        
        Args:
            tokens (List[str]): Lista de tokens/palavras.
            n (int): Tamanho do n-grama.
            
        Returns:
            List[tuple]: Lista de tuplas representando n-gramas.
        """
        return [tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1) if all(token.isalpha() for token in tokens[i:i+n])]
