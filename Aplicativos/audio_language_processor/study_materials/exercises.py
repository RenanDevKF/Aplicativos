# Cria exercicios com audio e textos

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
        
        if not self.transcription:
            return [{"type": "error", "message": "Transcrição não disponível para criar exercícios"}]
        
        # Dividir a transcrição em sentenças
        sentences = [s.strip() for s in self.transcription.split('.') if s.strip()]
        
        # Criar exercícios com base no nível de dificuldade
        if difficulty == "fácil":
            # Repetição de palavras isoladas
            if self.vocabulary:
                for i in range(min(5, len(self.vocabulary))):
                    word = self.vocabulary[i]["word"]
                    exercises.append({
                        "type": "repetição_palavra",
                        "instruction": f"Repita a palavra: {word}",
                        "target_word": word,
                        "difficulty": "fácil"
                    })
        
        elif difficulty == "médio":
            # Repetição de frases curtas
            short_sentences = [s for s in sentences if len(s.split()) <= 8]
            for i in range(min(3, len(short_sentences))):
                sentence = short_sentences[i]
                exercises.append({
                    "type": "repetição_frase",
                    "instruction": f"Repita a frase: {sentence}",
                    "target_sentence": sentence,
                    "difficulty": "médio"
                })
                
            # Exercício de ritmo
            if self.speech_analysis and "speech_rate" in self.speech_analysis:
                target_rate = self.speech_analysis["speech_rate"]["syllables_per_minute"]
                exercises.append({
                    "type": "ritmo_fala",
                    "instruction": f"Tente falar com uma taxa de {target_rate:.1f} sílabas por minuto",
                    "target_rate": target_rate,
                    "difficulty": "médio"
                })
        
        else:  # difícil
            # Repetição de frases longas
            long_sentences = [s for s in sentences if len(s.split()) > 8]
            for i in range(min(2, len(long_sentences))):
                sentence = long_sentences[i]
                exercises.append({
                    "type": "repetição_frase_complexa",
                    "instruction": f"Repita a frase mantendo o ritmo e entonação natural: {sentence}",
                    "target_sentence": sentence,
                    "difficulty": "difícil"
                })
                
            # Exercício de entonação
            if self.pronunciation_analysis and "stress_patterns" in self.pronunciation_analysis:
                stress_pattern = self.pronunciation_analysis["stress_patterns"]
                if isinstance(stress_pattern, list) and len(stress_pattern) > 0:
                    # Escolher uma frase e marcar sílabas enfatizadas
                    if sentences:
                        sentence = random.choice(sentences)
                        exercises.append({
                            "type": "entonação",
                            "instruction": f"Pratique a entonação correta da frase: {sentence}",
                            "target_sentence": sentence,
                            "hint": "Preste atenção nas sílabas enfatizadas",
                            "difficulty": "difícil"
                        })
        
        return exercises
    
    
    def _generate_question_from_sentence(self, sentence: str) -> str:
        """
        Gera uma pergunta simples a partir de uma frase.
        
        Args:
            sentence: Frase para criar pergunta
            
        Returns:
            Pergunta gerada
        """
        words = sentence.lower().split()
        
        # Perguntas simples baseadas no conteúdo
        if len(words) >= 6:
            return f"O que está sendo discutido na frase: '{sentence}'?"
        elif len(words) >= 3:
            return f"Qual é o assunto principal da frase ouvida?"
        else:
            return "Sobre o que é este áudio?"