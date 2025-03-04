import numpy as np
import librosa
import librosa.display
import os
from typing import Dict, Any, List

class PronunciationAnalyzer:
    """
    Classe para analisar a pronúncia em arquivos de áudio.

    Permite a comparação de um áudio do usuário com um áudio de referência, 
    analisando características fonéticas por meio de MFCCs (Mel-Frequency Cepstral Coefficients) 
    e padrões de acentuação.
    """

    def __init__(self, user_audio_path: str, reference_audio_path: str = None):
        """
        Inicializa o analisador de pronúncia.

        Args:
            user_audio_path (str): Caminho do arquivo de áudio do usuário.
            reference_audio_path (str, opcional): Caminho do arquivo de áudio de referência.
        
        Raises:
            FileNotFoundError: Se o arquivo de áudio do usuário ou referência não for encontrado.
            ValueError: Se houver erro ao carregar os arquivos de áudio.
        """
        self.user_audio_path = user_audio_path
        self.reference_audio_path = reference_audio_path
        self.user_y, self.user_sr = None, None
        self.ref_y, self.ref_sr = None, None

        if not os.path.isfile(user_audio_path):
            raise FileNotFoundError(f"O arquivo de áudio do usuário '{user_audio_path}' não foi encontrado.")

        try:
            self.user_y, self.user_sr = librosa.load(user_audio_path, sr=None)
        except Exception as e:
            raise ValueError(f"Erro ao carregar o áudio do usuário '{user_audio_path}': {str(e)}")

        if reference_audio_path:
            if not os.path.isfile(reference_audio_path):
                raise FileNotFoundError(f"O arquivo de áudio de referência '{reference_audio_path}' não foi encontrado.")
            
            try:
                self.ref_y, self.ref_sr = librosa.load(reference_audio_path, sr=None)
                if self.user_sr and self.ref_sr and self.user_sr != self.ref_sr:
                    self.ref_y = librosa.resample(self.ref_y, orig_sr=self.ref_sr, target_sr=self.user_sr)
                    self.ref_sr = self.user_sr
            except Exception as e:
                raise ValueError(f"Erro ao carregar o áudio de referência '{reference_audio_path}': {str(e)}")

    def compare_mfcc(self, n_mfcc: int = 13) -> Dict[str, Any]:
        """
        Compara os coeficientes MFCC entre os áudios do usuário e de referência para avaliar a similaridade fonética.

        Args:
            n_mfcc (int, opcional): Número de coeficientes MFCC a serem extraídos. Padrão: 13.

        Returns:
            dict: Contém as métricas de similaridade, incluindo distância euclidiana, correlação e uma pontuação geral.
        """
        if self.ref_y is None:
            return {"error": "Áudio de referência não fornecido ou não carregado corretamente."}

        try:
            user_mfcc = librosa.feature.mfcc(y=self.user_y, sr=self.user_sr, n_mfcc=n_mfcc)
            ref_mfcc = librosa.feature.mfcc(y=self.ref_y, sr=self.ref_sr, n_mfcc=n_mfcc)

            if user_mfcc.shape[1] == 0 or ref_mfcc.shape[1] == 0:
                return {"error": "Erro ao calcular MFCCs. Verifique a qualidade dos áudios."}

            min_length = min(user_mfcc.shape[1], ref_mfcc.shape[1])
            user_mfcc = user_mfcc[:, :min_length]
            ref_mfcc = ref_mfcc[:, :min_length]

            distance = np.mean(np.sqrt(np.sum((user_mfcc - ref_mfcc) ** 2, axis=0)))
            
            correlation_values = [
                np.corrcoef(user_mfcc[i, :], ref_mfcc[i, :])[0, 1] 
                for i in range(n_mfcc) if np.std(user_mfcc[i, :]) > 0 and np.std(ref_mfcc[i, :]) > 0
            ]
            correlation = np.mean(correlation_values) if correlation_values else 0.0
            
            max_distance = np.sqrt(n_mfcc * 100)
            similarity = max(0, 100 - (distance / max_distance * 100)) if max_distance > 0 else 0.0

            return {
                "distance": float(distance),
                "correlation": float(correlation),
                "similarity_percentage": float(similarity),
                "pronunciation_score": self._calculate_pronunciation_score(similarity, correlation)
            }
        except Exception as e:
            return {"error": f"Erro na comparação de MFCCs: {str(e)}"}

    def detect_stress_patterns(self) -> List[Dict[str, Any]]:
        """
        Detecta padrões de acentuação e ênfase na fala do usuário.

        Returns:
            list: Lista de dicionários contendo informações sobre os padrões de acentuação detectados.
        """
        try:
            hop_length = 512
            onset_env = librosa.onset.onset_strength(y=self.user_y, sr=self.user_sr, hop_length=hop_length)
            onsets = librosa.onset.onset_detect(onset_envelope=onset_env, sr=self.user_sr, hop_length=hop_length)
            onset_times = librosa.frames_to_time(onsets, sr=self.user_sr, hop_length=hop_length)
            onset_strengths = onset_env[onsets] if len(onsets) > 0 else []

            if len(onset_strengths) > 0:
                mean_strength = np.mean(onset_strengths)
                std_strength = np.std(onset_strengths)

                stress_segments = []
                for i, (time, strength) in enumerate(zip(onset_times, onset_strengths)):
                    if strength > mean_strength + 1.5 * std_strength:
                        emphasis = "forte"
                    elif strength > mean_strength + 0.5 * std_strength:
                        emphasis = "moderada"
                    else:
                        emphasis = "fraca"

                    duration = onset_times[i + 1] - time if i < len(onset_times) - 1 else 0.25

                    stress_segments.append({
                        "time": float(time),
                        "strength": float(strength),
                        "emphasis": emphasis,
                        "duration": float(duration)
                    })
                return stress_segments
            else:
                return []
        except Exception as e:
            return {"error": f"Erro na detecção de padrões de acentuação: {str(e)}"}

    def _calculate_pronunciation_score(self, similarity: float, correlation: float) -> float:
        """
        Calcula uma pontuação geral de pronúncia com base na similaridade e correlação dos MFCCs.

        Args:
            similarity (float): Porcentagem de similaridade dos MFCCs.
            correlation (float): Correlação entre os MFCCs do usuário e do áudio de referência.

        Returns:
            float: Pontuação de pronúncia em uma escala de 0 a 100.
        """
        try:
            similarity_weight = 0.7
            correlation_weight = 0.3
            correlation_score = max(0, (correlation + 1) * 50)
            score = similarity_weight * similarity + correlation_weight * correlation_score
            return float(score)
        except Exception:
            return 0.0
