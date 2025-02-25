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
            
def segment_audio(self, min_silence_len: int = 500, silence_thresh: int = -40) -> List[Dict[str, Any]]:
        """
        Segmenta o áudio em trechos separados por silêncio.
        
        Args:
            min_silence_len: Duração mínima do silêncio em ms
            silence_thresh: Limiar de dB para considerar silêncio
            
        Returns:
            Lista de segmentos com início, fim e duração
        """
        # Converter para dB
        db = librosa.amplitude_to_db(np.abs(librosa.stft(self.y)), ref=np.max)
        
        # Máscara de silêncio
        silence_mask = db.mean(axis=0) < silence_thresh
        
        # Converter frames para segundos
        hop_length = 512  # Padrão do STFT
        frame_time = hop_length / self.sr
        
        # Encontrar segmentos
        segments = []
        is_silence = True
        current_start = 0
        
        for i, silent in enumerate(silence_mask):
            # Transição de silêncio para som
            if is_silence and not silent:
                current_start = i * frame_time
                is_silence = False
            # Transição de som para silêncio
            elif not is_silence and silent:
                # Verificar se o silêncio é longo o suficiente
                silence_start = i
                long_silence = True
                
                # Olhar à frente para verificar se o silêncio dura o suficiente
                min_silence_frames = min_silence_len / 1000 / frame_time
                if i + int(min_silence_frames) < len(silence_mask):
                    long_silence = all(silence_mask[i:i+int(min_silence_frames)])
                
                if long_silence:
                    end_time = i * frame_time
                    segments.append({
                        "start": current_start,
                        "end": end_time,
                        "duration": end_time - current_start
                    })
                    is_silence = True
        
        # Adicionar último segmento se terminar com som
        if not is_silence:
            end_time = len(silence_mask) * frame_time
            segments.append({
                "start": current_start,
                "end": end_time,
                "duration": end_time - current_start
            })
        
        return segments