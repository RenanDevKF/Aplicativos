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