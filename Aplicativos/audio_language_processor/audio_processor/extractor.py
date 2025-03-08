import librosa
import numpy as np
from typing import Dict, Tuple, List, Any

class AudioExtractor:
    """Classe para extrair características de arquivos de áudio para estudo de idiomas."""
    
    def __init__(self, audio_path: str):
        """
        Inicializa o extrator com o caminho para o arquivo de áudio.
        
        Args:
            audio_path (str): Caminho para o arquivo de áudio a ser analisado.
        """
        self.audio_path = audio_path
        self.y = None
        self.sr = None
        self.duration = None
        try:
            self._load_audio()
        except Exception as e:
            print(f"Erro ao inicializar o extrator de áudio: {e}")
            raise

    def _load_audio(self) -> None:
        """
        Carrega o áudio usando librosa e configura parâmetros básicos.
        
        Levanta exceções caso ocorra algum erro no carregamento do áudio.
        """
        try:
            self.y, self.sr = librosa.load(self.audio_path, sr=None)
            self.duration = librosa.get_duration(y=self.y, sr=self.sr)
            print(f"Áudio carregado: duração de {self.duration:.2f} segundos, taxa de amostragem {self.sr}Hz")
        except librosa.util.exceptions.ParameterError as e:
            print(f"Erro de parâmetro ao carregar o áudio: {e}")
            raise
        except FileNotFoundError as e:
            print(f"Arquivo de áudio não encontrado: {e}")
            raise
        except Exception as e:
            print(f"Erro desconhecido ao carregar o áudio: {e}")
            raise

    def get_speech_rate(self) -> Dict[str, float]:
        """
        Calcula a taxa aproximada de fala usando os picos de energia.
        
        Returns:
            dict: Dicionário com estatísticas de taxa de fala, incluindo:
                - syllables_detected: Número estimado de sílabas detectadas
                - syllables_per_second: Média de sílabas por segundo
                - syllables_per_minute: Média de sílabas por minuto
        """
        try:
            hop_length = int(self.sr * 0.01)  # Janela de 10ms
            onset_env = librosa.onset.onset_strength(y=self.y, sr=self.sr, hop_length=hop_length)
            onsets = librosa.onset.onset_detect(onset_envelope=onset_env, sr=self.sr, hop_length=hop_length)
            
            estimated_syllables = len(onsets)
            syllables_per_second = estimated_syllables / self.duration
            syllables_per_minute = syllables_per_second * 60
            
            return {
                "syllables_detected": estimated_syllables,
                "syllables_per_second": syllables_per_second,
                "syllables_per_minute": syllables_per_minute
            }
        except Exception as e:
            print(f"Erro ao calcular a taxa de fala: {e}")
            return {"error": f"Erro ao calcular a taxa de fala: {str(e)}"}

    def get_pitch_stats(self) -> Dict[str, float]:
        """
        Extrai estatísticas de pitch (tom) do áudio.
        
        Returns:
            dict: Dicionário contendo:
                - pitch_min: Tom mínimo detectado
                - pitch_max: Tom máximo detectado
                - pitch_mean: Média do tom
                - pitch_std: Desvio padrão do tom
                - pitch_range: Variação entre tom máximo e mínimo
        """
        try:
            pitches, magnitudes = librosa.piptrack(y=self.y, sr=self.sr)
            
            pitches_filtered = []
            for i in range(pitches.shape[1]):
                index = magnitudes[:, i].argmax()
                pitch = pitches[index, i]
                if pitch > 0:
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
        except Exception as e:
            print(f"Erro ao extrair estatísticas de pitch: {e}")
            return {"error": f"Erro ao extrair estatísticas de pitch: {str(e)}"}

    def segment_audio(self, min_silence_len: int = 500, silence_thresh: int = -40) -> List[Dict[str, Any]]:
        """
        Segmenta o áudio em trechos separados por silêncio.
        
        Args:
            min_silence_len (int): Duração mínima do silêncio em ms.
            silence_thresh (int): Limiar de dB para considerar silêncio.
            
        Returns:
            list: Lista de segmentos contendo:
                - start: Início do segmento (segundos)
                - end: Fim do segmento (segundos)
                - duration: Duração do segmento (segundos)
        """
        try:
            db = librosa.amplitude_to_db(np.abs(librosa.stft(self.y)), ref=np.max)
            silence_mask = db.mean(axis=0) < silence_thresh
            
            hop_length = 512  # Padrão do STFT
            frame_time = hop_length / self.sr
            
            segments = []
            is_silence = True
            current_start = 0
            
            for i, silent in enumerate(silence_mask):
                if is_silence and not silent:
                    current_start = i * frame_time
                    is_silence = False
                elif not is_silence and silent:
                    silence_start = i
                    long_silence = True
                    
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
            
            if not is_silence:
                end_time = len(silence_mask) * frame_time
                segments.append({
                    "start": current_start,
                    "end": end_time,
                    "duration": end_time - current_start
                })
            
            return segments
        except Exception as e:
            print(f"Erro ao segmentar o áudio: {e}")
            return {"error": f"Erro ao segmentar o áudio: {str(e)}"}
