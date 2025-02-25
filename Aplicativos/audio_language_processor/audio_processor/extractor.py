# Extrai dados de áudio

import librosa
import numpy as np
from typing import Dict, Tuple, List, Any

class AudioExtractor:
    """Classe para extrair características de arquivos de áudio para estudo de idiomas."""
    
    def __init__(self, audio_path: str):
        """
        Inicializa o extrator com o caminho para o arquivo de áudio.
        
        Args:
            audio_path: Caminho para o arquivo de áudio a ser analisado
        """
        self.audio_path = audio_path
        self.y = None
        self.sr = None
        self.duration = None
        self._load_audio()
    
    def _load_audio(self) -> None:
        """Carrega o áudio usando librosa e configura parâmetros básicos."""
        try:
            self.y, self.sr = librosa.load(self.audio_path, sr=None)
            self.duration = librosa.get_duration(y=self.y, sr=self.sr)
            print(f"Áudio carregado: duração de {self.duration:.2f} segundos, taxa de amostragem {self.sr}Hz")
        except Exception as e:
            print(f"Erro ao carregar o áudio: {e}")
            raise
        
def get_speech_rate(self) -> Dict[str, float]:
        """
        Calcula a taxa aproximada de fala usando os picos de energia.
        
        Returns:
            Dicionário com estatísticas de taxa de fala
        """
        # Dividir o áudio em janelas e contar picos de energia
        hop_length = int(self.sr * 0.01)  # Janela de 10ms
        onset_env = librosa.onset.onset_strength(y=self.y, sr=self.sr, hop_length=hop_length)
        onsets = librosa.onset.onset_detect(onset_envelope=onset_env, sr=self.sr, 
                                           hop_length=hop_length)
        
        # Estimar sílabas a partir dos onsets
        estimated_syllables = len(onsets)
        syllables_per_second = estimated_syllables / self.duration
        syllables_per_minute = syllables_per_second * 60
        
        return {
            "syllables_detected": estimated_syllables,
            "syllables_per_second": syllables_per_second,
            "syllables_per_minute": syllables_per_minute
        }
        
def get_pitch_stats(self) -> Dict[str, float]:
        """
        Extrai estatísticas de pitch (tom) do áudio.
        
        Returns:
            Dicionário com estatísticas de pitch
        """
        pitches, magnitudes = librosa.piptrack(y=self.y, sr=self.sr)
        
        # Filtrar pitches com magnitude significativa
        pitches_filtered = []
        for i in range(pitches.shape[1]):
            index = magnitudes[:, i].argmax()
            pitch = pitches[index, i]
            if pitch > 0:  # Ignorar silêncio
                pitches_filtered.append(pitch)
        
        if pitches_filtered:
            pitch_array = np.array(pitches_filtered)
            return {
                "pitch_min": float(np.min(pitch_array)),
                "pitch_max": float(np.max(pitch_array)),
                "pitch_mean": float(np.mean(pitch_array)),
                "pitch_std": float(np.std(pitch_array)),
                "pitch_range": float(np.max(pitch_array) - np.min(pitch_array))
            }
        else:
            return {
                "pitch_min": 0.0,
                "pitch_max": 0.0,
                "pitch_mean": 0.0,
                "pitch_std": 0.0,
                "pitch_range": 0.0
            }