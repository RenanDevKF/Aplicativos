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
            
    def extract_vocabulary(self, include_stopwords: bool = False, 
                           min_word_length: int = 2) -> List[Dict[str, Any]]:
        """
        Extrai e analisa o vocabulário do texto.
        
        Args:
            include_stopwords: Se True, inclui palavras comuns (stopwords)
            min_word_length: Tamanho mínimo de palavra para incluir na análise
            
        Returns:
            Lista de dicionários com palavras e suas estatísticas
        """
        # Limpar e tokenizar o texto
        cleaned_text = self._clean_text(self.text)
        tokens = word_tokenize(cleaned_text)
        
        # Filtrar tokens
        filtered_tokens = []
        for token in tokens:
            # Verificar se é uma palavra válida
            if (len(token) >= min_word_length and 
                token.isalpha() and
                (include_stopwords or token.lower() not in self.stop_words)):
                filtered_tokens.append(token.lower())
        
        # Calcular frequência
        freq_dist = FreqDist(filtered_tokens)
        total_words = len(filtered_tokens)
        
        # Criar lista de vocabulário
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
            min_occurrences: Número mínimo de ocorrências para considerar uma frase
            max_phrase_length: Número máximo de palavras na frase
            
        Returns:
            Lista de dicionários com frases e suas estatísticas
        """
        # Limpar e tokenizar o texto
        cleaned_text = self._clean_text(self.text)
        tokens = word_tokenize(cleaned_text)
        
        # Encontrar n-gramas (sequências de n palavras)
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
        
        # Ordenar por contagem (mais frequentes primeiro)
        phrases.sort(key=lambda x: x["count"], reverse=True)
        
        return phrases
    
    def get_language_level_estimate(self) -> Dict[str, Any]:
        """
        Estima o nível de dificuldade do vocabulário.
        
        Returns:
            Dicionário com estimativa de nível de idioma e estatísticas
        """
        # Extrair vocabulário incluindo stopwords
        vocab = self.extract_vocabulary(include_stopwords=True)
        
        if not vocab:
            return {
                "level": "indeterminado",
                "confidence": 0.0,
                "reason": "Texto muito curto ou sem palavras reconhecíveis"
            }
        
        # Calcular estatísticas
        word_lengths = [v["length"] for v in vocab]
        avg_word_length = sum(word_lengths) / len(word_lengths)
        
        # Contar palavras únicas
        unique_words = len(vocab)
        
        # Texto completo para análise de complexidade
        cleaned_text = self._clean_text(self.text)
        tokens = word_tokenize(cleaned_text)
        sentences = [s.strip() for s in re.split(r'[.!?]', cleaned_text) if s.strip()]
        
        # Calcular comprimento médio de sentença
        avg_sentence_length = len(tokens) / len(sentences) if sentences else 0
        
        # Usar heurísticas para estimar nível
        # (valores aproximados baseados em estudos linguísticos)
        level = "iniciante"
        confidence = 0.6
        reasons = []
        
        # Heurística 1: Comprimento médio de palavras
        if avg_word_length > 6.5:
            level = "avançado"
            reasons.append(f"Palavras longas (média: {avg_word_length:.1f} caracteres)")
        elif avg_word_length > 5.5:
            level = "intermediário"
            reasons.append(f"Palavras de comprimento médio ({avg_word_length:.1f} caracteres)")
        else:
            reasons.append(f"Palavras curtas (média: {avg_word_length:.1f} caracteres)")
        
        # Heurística 2: Comprimento médio de sentenças
        if avg_sentence_length > 15:
            level = max(level, "avançado")
            confidence += 0.1
            reasons.append(f"Sentenças longas (média: {avg_sentence_length:.1f} palavras)")
        elif avg_sentence_length > 10:
            level = max(level, "intermediário")
            reasons.append(f"Sentenças de comprimento médio ({avg_sentence_length:.1f} palavras)")
        else:
            reasons.append(f"Sentenças curtas (média: {avg_sentence_length:.1f} palavras)")
        
        # Heurística 3: Diversidade de vocabulário
        if unique_words > 100:
            level = max(level, "avançado")
            confidence += 0.1
            reasons.append(f"Vocabulário diverso ({unique_words} palavras únicas)")
        elif unique_words > 50:
            level = max(level, "intermediário")
            reasons.append(f"Vocabulário moderado ({unique_words} palavras únicas)")
        else:
            reasons.append(f"Vocabulário limitado ({unique_words} palavras únicas)")
        
        # Normalizar confiança
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