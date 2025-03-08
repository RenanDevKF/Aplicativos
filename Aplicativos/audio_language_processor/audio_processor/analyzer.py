import numpy as np  # Usado para cálculos estatísticos
from typing import Dict, List, Any

class AudioAnalyzer:
    """Classe para analisar características extraídas de áudio para estudo de idiomas."""
    
    def __init__(self, extractor):
        """
        Inicializa o analisador com um extrator de áudio.
        
        Args:
            extractor: Instância de AudioExtractor, responsável por extrair informações do áudio.
        
        Raises:
            AttributeError: Se o extractor não possuir os métodos necessários.
        """
        self.extractor = extractor
        
        # Verificação da existência dos métodos necessários no extractor
        required_methods = ["get_speech_rate", "get_pitch_stats", "segment_audio"]
        for method in required_methods:
            if not hasattr(extractor, method):
                raise AttributeError(f"O extractor precisa ter o método {method}.")
        
    def analyze_speech_patterns(self) -> Dict[str, Any]:
        """
        Analisa padrões de fala como ritmo, entonação e pausas.
        
        Returns:
            dict: Dicionário contendo as métricas analisadas:
                - speech_rate (dict): Taxa de fala.
                - pitch_stats (dict): Estatísticas de entonação.
                - segment_stats (dict): Estatísticas dos segmentos de áudio.
                - pause_stats (dict): Estatísticas das pausas.
                - speech_rate_percentile (dict): Classificação da taxa de fala.
                - fluency_score (float): Pontuação de fluência calculada.
        
        Raises:
            RuntimeError: Se ocorrer um erro ao extrair os dados do áudio.
        """
        try:
            speech_rate = self.extractor.get_speech_rate()
            pitch_stats = self.extractor.get_pitch_stats()
            segments = self.extractor.segment_audio()
        except Exception as e:
            raise RuntimeError(f"Erro ao extrair dados de áudio: {e}")
        
        segment_durations = [seg.get("duration", 0) for seg in segments if "duration" in seg]
        
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
        
        pauses = []
        for i in range(len(segments) - 1):
            try:
                pause_duration = segments[i+1]["start"] - segments[i]["end"]
                pauses.append(pause_duration)
            except KeyError:
                continue
        
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
        
        speech_rate_percentile = self._classify_speech_rate(speech_rate.get("syllables_per_minute", 0))
        
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
        Classifica a taxa de fala com base na média e no desvio padrão esperado.
        
        Args:
            syllables_per_minute (float): Número de sílabas faladas por minuto.
        
        Returns:
            dict: Classificação da taxa de fala contendo:
                - z_score (float): Pontuação padronizada.
                - category (str): Classificação textual da taxa de fala.
        """
        mean_spm = 250.0
        std_spm = 50.0
        
        if std_spm == 0:
            z_score = 0.0
        else:
            z_score = (syllables_per_minute - mean_spm) / std_spm
        
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
            "z_score": z_score,
            "category": category
        }
    
    def _calculate_fluency_score(self, speech_rate: Dict, segment_stats: Dict, pause_stats: Dict) -> float:
        """
        Calcula uma pontuação de fluência baseada em características de fala.
        
        Args:
            speech_rate (dict): Dados da taxa de fala.
            segment_stats (dict): Estatísticas dos segmentos de áudio.
            pause_stats (dict): Estatísticas das pausas.
        
        Returns:
            float: Pontuação de fluência entre 0 e 100.
        """
        base_score = 50.0
        
        try:
            spm = speech_rate["syllables_per_minute"]
        except KeyError:
            spm = 0
        
        speech_rate_factor = 5.0
        if 200 <= spm <= 300:
            speech_rate_factor = 20.0
        elif 150 <= spm < 200 or 300 < spm <= 350:
            speech_rate_factor = 15.0
        elif 100 <= spm < 150 or 350 < spm <= 400:
            speech_rate_factor = 10.0
        
        try:
            consistency_factor = 5.0
            cv = segment_stats["segment_duration_std"] / segment_stats["avg_segment_duration"] if segment_stats["avg_segment_duration"] > 0 else float('inf')
            if cv < 0.3:
                consistency_factor = 15.0
            elif cv < 0.5:
                consistency_factor = 12.0
            elif cv < 0.7:
                consistency_factor = 8.0
        except ZeroDivisionError:
            consistency_factor = 5.0
        
        pause_factor = 0.0
        if pause_stats["pause_count"] > 0:
            avg_pause = pause_stats["avg_pause_duration"]
            if avg_pause < 0.3:
                pause_factor = 15.0
            elif avg_pause < 0.6:
                pause_factor = 10.0
            elif avg_pause < 1.0:
                pause_factor = 5.0
        
        fluency_score = base_score + speech_rate_factor + consistency_factor + pause_factor
        return min(fluency_score, 100.0)
