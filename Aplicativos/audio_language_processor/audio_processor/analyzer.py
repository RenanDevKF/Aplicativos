# Analisa carcteristicas de um audio

import numpy as np # Usado para cálculos estatísticos, como média (mean), desvio padrão (std), e mínimos/máximos.
import scipy.stats # Fornece funções estatísticas avançadas, como norm.cdf (função de distribuição acumulada normal).
from typing import Dict, List, Any # Define tipos de dados usados nos retornos e argumentos, melhorando a legibilidade e manutenção do código.

class AudioAnalyzer:
    """Classe para analisar características extraídas de áudio para estudo de idiomas."""
    
    def __init__(self, extractor):
        """
        Inicializa o analisador com um extrator de áudio.
        
        Args:
            extractor: Instância de AudioExtractor
        """
        self.extractor = extractor
        
    def analyze_speech_patterns(self) -> Dict[str, Any]:
            """
            Analisa padrões de fala como ritmo, entonação e pausas.
            
            Returns:
                Dicionário com análise de padrões de fala
            """
            # Obter taxa de fala
            speech_rate = self.extractor.get_speech_rate() # Obtém a taxa de fala (ex.: sílabas por minuto).
            
            # Obter estatísticas de pitch
            pitch_stats = self.extractor.get_pitch_stats() # Obtém estatísticas do pitch da fala (frequência fundamental).
            
            # Obter segmentos
            segments = self.extractor.segment_audio() # Divide o áudio em segmentos baseados em pausas ou entonação.

            
            # Calcular estatísticas de duração dos segmentos
            segment_durations = [seg["duration"] for seg in segments] # Lista com as durações de cada segmento do áudio.
            
            if segment_durations:
                segment_stats = {
                    "segment_count": len(segments),
                    "avg_segment_duration": np.mean(segment_durations),
                    "min_segment_duration": np.min(segment_durations),
                    "max_segment_duration": np.max(segment_durations),
                    "segment_duration_std": np.std(segment_durations)
                }
            else:
                segment_stats = {
                    "segment_count": 0,
                    "avg_segment_duration": 0,
                    "min_segment_duration": 0,
                    "max_segment_duration": 0,
                    "segment_duration_std": 0
                }
            
            # Calcular pausas entre segmentos
            pauses = []
            for i in range(len(segments) - 1):
                pause_duration = segments[i+1]["start"] - segments[i]["end"]
                pauses.append(pause_duration)
            
            if pauses:
                pause_stats = {
                    "pause_count": len(pauses),
                    "avg_pause_duration": np.mean(pauses),
                    "min_pause_duration": np.min(pauses),
                    "max_pause_duration": np.max(pauses),
                    "pause_duration_std": np.std(pauses)
                }
            else:
                pause_stats = {
                    "pause_count": 0,
                    "avg_pause_duration": 0,
                    "min_pause_duration": 0,
                    "max_pause_duration": 0,
                    "pause_duration_std": 0
                }
            
            # Classificação de ritmo
            speech_rate_percentile = self._classify_speech_rate(speech_rate["syllables_per_minute"])
            
            return {
                "speech_rate": speech_rate,
                "pitch_stats": pitch_stats,
                "segment_stats": segment_stats,
                "pause_stats": pause_stats,
                "speech_rate_percentile": speech_rate_percentile,
                "fluency_score": self._calculate_fluency_score(speech_rate, segment_stats, pause_stats)
            }
            
    def _classify_speech_rate(self, syllables_per_minute: float) -> Dict[str, Any]:
            """
            Classifica a taxa de fala com base em distribuições típicas.
            
            Args:
                syllables_per_minute: Taxa de fala em sílabas por minuto
                
            Returns:
                Classificação da taxa de fala
            """
            # Valores aproximados baseados em estudos linguísticos
            # (Valores específicos podem variar por idioma)
            mean_spm = 250.0  # Média para fala normal em muitos idiomas
            std_spm = 50.0    # Desvio padrão
            
            z_score = (syllables_per_minute - mean_spm) / std_spm
            percentile = scipy.stats.norm.cdf(z_score) * 100
            
            if syllables_per_minute < 150:
                category = "lenta"
            elif syllables_per_minute < 220:
                category = "moderada-lenta"
            elif syllables_per_minute < 280:
                category = "moderada"
            elif syllables_per_minute < 350:
                category = "moderada-rápida"
            else:
                category = "rápida"
            
            return {
                "percentile": percentile,
                "z_score": z_score,
                "category": category
            }
    

    def _calculate_fluency_score(self, speech_rate: Dict, segment_stats: Dict, pause_stats: Dict) -> float:
        """
        Calcula uma pontuação de fluência baseada em características de fala.
        
        Returns:
            Pontuação de fluência (0-100)
        """
        # Base para a pontuação
        base_score = 50.0
        
        # Fator de taxa de fala - penaliza fala muito lenta ou muito rápida
        speech_rate_factor = 0.0
        spm = speech_rate["syllables_per_minute"]
        if 200 <= spm <= 300:  # Faixa ideal
            speech_rate_factor = 20.0
        elif 150 <= spm < 200 or 300 < spm <= 350:  # Faixa aceitável
            speech_rate_factor = 15.0
        elif 100 <= spm < 150 or 350 < spm <= 400:  # Faixa menos ideal
            speech_rate_factor = 10.0
        else:  # Faixa problemática
            speech_rate_factor = 5.0
        
        # Fator de consistência nos segmentos
        consistency_factor = 0.0
        if segment_stats["segment_count"] > 0:
            # Menos variação na duração dos segmentos = mais consistência
            cv = segment_stats["segment_duration_std"] / segment_stats["avg_segment_duration"] \
                if segment_stats["avg_segment_duration"] > 0 else float('inf')
            
            if cv < 0.3:  # Muito consistente
                consistency_factor = 15.0
            elif cv < 0.5:  # Consistente
                consistency_factor = 12.0
            elif cv < 0.7:  # Moderadamente consistente
                consistency_factor = 8.0
            else:  # Pouco consistente
                consistency_factor = 5.0
        
        # Fator de pausas
        pause_factor = 0.0
        if pause_stats["pause_count"] > 0:
            avg_pause = pause_stats["avg_pause_duration"]
            
            if avg_pause < 0.3:  # Pausas curtas, natural
                pause_factor = 15.0
            elif avg_pause < 0.6:  # Pausas moderadas
                pause_factor = 10.0
            elif avg_pause < 1.0:  # Pausas longas
                pause_factor = 5.0
            else:  # Pausas muito longas
                pause_factor = 0.0
        
        # Calcular pontuação final
        fluency_score = base_score + speech_rate_factor + consistency_factor + pause_factor
        
        # Limitar a 100
        return min(fluency_score, 100.0)