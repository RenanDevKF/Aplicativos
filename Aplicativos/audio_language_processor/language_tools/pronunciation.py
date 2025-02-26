# Avalia pronunciação

import numpy as np
import librosa
from typing import Dict, Any, List, Tuple

class PronunciationAnalyzer:
    """Classe para analisar pronúncia em áudios para estudo de idiomas."""
    
    def __init__(self, user_audio_path: str, reference_audio_path: str = None):
        """
        Inicializa o analisador de pronúncia.
        
        Args:
            user_audio_path: Caminho para o áudio do usuário
            reference_audio_path: Caminho para o áudio de referência (opcional)
        """
        self.user_audio_path = user_audio_path
        self.reference_audio_path = reference_audio_path
        
        # Carregar o áudio do usuário
        self.user_y, self.user_sr = librosa.load(user_audio_path, sr=None)
        
        # Carregar o áudio de referência se fornecido
        self.ref_y = None
        self.ref_sr = None
        if reference_audio_path:
            self.ref_y, self.ref_sr = librosa.load(reference_audio_path, sr=None)
            
            # Resampling para mesma taxa se diferentes
            if self.user_sr != self.ref_sr:
                self.ref_y = librosa.resample(self.ref_y, orig_sr=self.ref_sr, target_sr=self.user_sr)
                self.ref_sr = self.user_sr
    
    def compare_mfcc(self, n_mfcc: int = 13) -> Dict[str, Any]:
        """
        Compara MFCCs (Mel-frequency cepstral coefficients) entre áudios
        para avaliar similaridade fonética.
        
        Args:
            n_mfcc: Número de coeficientes MFCC a usar
            
        Returns:
            Dicionário com métricas de similaridade de pronúncia
        """
        if self.ref_y is None:
            return {"error": "Áudio de referência não fornecido"}
        
        # Extrair MFCC
        user_mfcc = librosa.feature.mfcc(y=self.user_y, sr=self.user_sr, n_mfcc=n_mfcc)
        ref_mfcc = librosa.feature.mfcc(y=self.ref_y, sr=self.ref_sr, n_mfcc=n_mfcc)
        
        # Normalizar comprimentos (Dynamic Time Warping seria melhor, mas é mais complexo)
        min_length = min(user_mfcc.shape[1], ref_mfcc.shape[1])
        user_mfcc = user_mfcc[:, :min_length]
        ref_mfcc = ref_mfcc[:, :min_length]
        
        # Calcular distância euclidiana
        distance = np.mean(np.sqrt(np.sum((user_mfcc - ref_mfcc)**2, axis=0)))
        
        # Calcular correlação
        correlation = np.mean([np.corrcoef(user_mfcc[i, :], ref_mfcc[i, :])[0, 1] 
                              for i in range(n_mfcc)])
        
        # Calcular similaridade em porcentagem (inversamente proporcional à distância)
        max_distance = np.sqrt(n_mfcc * 100)  # Valor aproximado para normalização
        similarity = max(0, 100 - (distance / max_distance * 100))
        
        return {
            "distance": float(distance),
            "correlation": float(correlation),
            "similarity_percentage": float(similarity),
            "pronunciation_score": self._calculate_pronunciation_score(similarity, correlation)
        }
        
    def detect_stress_patterns(self) -> List[Dict[str, Any]]:
        """
        Detecta padrões de acentuação e ênfase no áudio.
        
        Returns:
            Lista de segmentos com informações de acentuação
        """
        # Extrair envelope de energia
        hop_length = 512
        onset_env = librosa.onset.onset_strength(y=self.user_y, sr=self.user_sr, 
                                               hop_length=hop_length)
        
        # Detectar onsets (inícios de som/sílaba)
        onsets = librosa.onset.onset_detect(onset_envelope=onset_env, sr=self.user_sr,
                                          hop_length=hop_length)
        onset_times = librosa.frames_to_time(onsets, sr=self.user_sr, hop_length=hop_length)
        
        # Extrair energia em cada onset
        onset_strengths = onset_env[onsets] if len(onsets) > 0 else []
        
        # Identificar acentuações (picos de energia relativamente altos)
        if len(onset_strengths) > 0:
            mean_strength = np.mean(onset_strengths)
            std_strength = np.std(onset_strengths)
            
            stress_segments = []
            for i, (time, strength) in enumerate(zip(onset_times, onset_strengths)):
                # Classificar nível de ênfase
                if strength > mean_strength + 1.5 * std_strength:
                    emphasis = "forte"
                elif strength > mean_strength + 0.5 * std_strength:
                    emphasis = "moderada"
                else:
                    emphasis = "fraca"
                
                # Calcular duração aproximada até próximo onset
                if i < len(onset_times) - 1:
                    duration = onset_times[i+1] - time
                else:
                    duration = 0.25  # Valor padrão para o último segmento
                
                stress_segments.append({
                    "time": float(time),
                    "strength": float(strength),
                    "emphasis": emphasis,
                    "duration": float(duration)
                })
            
            return stress_segments
        else:
            return []
        
    def _calculate_pronunciation_score(self, similarity: float, correlation: float) -> float:
        """
        Calcula uma pontuação de pronúncia baseada em métricas de similaridade.
        
        Args:
            similarity: Percentual de similaridade
            correlation: Correlação entre os MFCCs
            
        Returns:
            Pontuação de pronúncia (0-100)
        """
        # Pesos para cada componente
        similarity_weight = 0.7
        correlation_weight = 0.3
        
        # Ajustar correlação para escala 0-100
        correlation_score = max(0, (correlation + 1) * 50)
        
        # Calcular pontuação ponderada
        score = similarity_weight * similarity + correlation_weight * correlation_score
        
        return float(score)