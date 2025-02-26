# Analisa carcteristicas de um audio

import numpy as np
import scipy.stats
from typing import Dict, List, Any

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
            speech_rate = self.extractor.get_speech_rate()
            
            # Obter estatísticas de pitch
            pitch_stats = self.extractor.get_pitch_stats()
            
            # Obter segmentos
            segments = self.extractor.segment_audio()
            
            # Calcular estatísticas de duração dos segmentos
            segment_durations = [seg["duration"] for seg in segments]
            
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
    
    