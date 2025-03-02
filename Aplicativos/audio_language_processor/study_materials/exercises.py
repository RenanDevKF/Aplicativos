# Cria exercícios com áudio e textos

from typing import List, Dict, Any
import random

class ExerciseGenerator:
    """Classe para gerar exercícios de estudo de idiomas baseados em análise de áudio."""
    
    def __init__(self, 
                 transcription: str = None, 
                 speech_analysis: Dict[str, Any] = None,
                 pronunciation_analysis: Dict[str, Any] = None,
                 vocabulary: List[Dict[str, Any]] = None):
        """
        Inicializa o gerador de exercícios.
        
        Args:
            transcription: Transcrição do áudio (opcional)
            speech_analysis: Análise de padrões de fala (opcional)
            pronunciation_analysis: Análise de pronúncia (opcional)
            vocabulary: Lista de palavras detectadas com info de frequência (opcional)
        """
        self.transcription = transcription
        self.speech_analysis = speech_analysis
        self.pronunciation_analysis = pronunciation_analysis
        self.vocabulary = vocabulary

    def generate_pronunciation_exercises(self, difficulty: str = "médio") -> List[Dict[str, Any]]:
        """
        Gera exercícios focados em pronúncia.

        Args:
            difficulty: Nível de dificuldade ("fácil", "médio", "difícil")

        Returns:
            Lista de exercícios de pronúncia
        """
        exercises = []
        
        if not isinstance(difficulty, str) or difficulty not in {"fácil", "médio", "difícil"}:
            raise ValueError("O nível de dificuldade deve ser 'fácil', 'médio' ou 'difícil'.")

        if not self.transcription:
            return [{"type": "error", "message": "Transcrição não disponível para criar exercícios"}]
        
        try:
            sentences = [s.strip() for s in self.transcription.split('.') if s.strip()]
        except Exception as e:
            return [{"type": "error", "message": f"Erro ao processar a transcrição: {str(e)}"}]

        try:
            if difficulty == "fácil":
                if not self.vocabulary or not isinstance(self.vocabulary, list):
                    return [{"type": "error", "message": "Vocabulário não disponível ou em formato inválido"}]

                for i in range(min(5, len(self.vocabulary))):
                    word = self.vocabulary[i].get("word")
                    if word:
                        exercises.append({
                            "type": "repetição_palavra",
                            "instruction": f"Repita a palavra: {word}",
                            "target_word": word,
                            "difficulty": "fácil"
                        })

            elif difficulty == "médio":
                short_sentences = [s for s in sentences if len(s.split()) <= 8]
                for i in range(min(3, len(short_sentences))):
                    exercises.append({
                        "type": "repetição_frase",
                        "instruction": f"Repita a frase: {short_sentences[i]}",
                        "target_sentence": short_sentences[i],
                        "difficulty": "médio"
                    })

                if self.speech_analysis and isinstance(self.speech_analysis, dict):
                    speech_rate = self.speech_analysis.get("speech_rate", {}).get("syllables_per_minute")
                    if speech_rate:
                        exercises.append({
                            "type": "ritmo_fala",
                            "instruction": f"Tente falar com uma taxa de {speech_rate:.1f} sílabas por minuto",
                            "target_rate": speech_rate,
                            "difficulty": "médio"
                        })

            else:  # difícil
                long_sentences = [s for s in sentences if len(s.split()) > 8]
                for i in range(min(2, len(long_sentences))):
                    exercises.append({
                        "type": "repetição_frase_complexa",
                        "instruction": f"Repita a frase mantendo o ritmo e entonação natural: {long_sentences[i]}",
                        "target_sentence": long_sentences[i],
                        "difficulty": "difícil"
                    })

                if self.pronunciation_analysis and isinstance(self.pronunciation_analysis, dict):
                    stress_pattern = self.pronunciation_analysis.get("stress_patterns")
                    if isinstance(stress_pattern, list) and stress_pattern and sentences:
                        exercises.append({
                            "type": "entonação",
                            "instruction": f"Pratique a entonação correta da frase: {random.choice(sentences)}",
                            "hint": "Preste atenção nas sílabas enfatizadas",
                            "difficulty": "difícil"
                        })

        except Exception as e:
            return [{"type": "error", "message": f"Erro ao gerar exercícios: {str(e)}"}]

        return exercises

    def _generate_question_from_sentence(self, sentence: str) -> str:
        """
        Gera uma pergunta simples a partir de uma frase.

        Args:
            sentence: Frase para criar pergunta

        Returns:
            Pergunta gerada
        """
        if not isinstance(sentence, str) or not sentence.strip():
            raise ValueError("A frase deve ser uma string não vazia.")

        words = sentence.lower().split()

        try:
            if len(words) >= 6:
                return f"O que está sendo discutido na frase: '{sentence}'?"
            elif len(words) >= 3:
                return f"Qual é o assunto principal da frase ouvida?"
            else:
                return "Sobre o que é este áudio?"
        except Exception as e:
            return f"Erro ao gerar pergunta: {str(e)}"
