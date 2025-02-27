# Converte áudio para texto

import speech_recognition as sr
from pydub import AudioSegment
import os
import tempfile
from typing import Dict, Any, Optional

class AudioToTextConverter:
    """Classe para converter áudio em texto usando reconhecimento de fala."""
    
    def __init__(self, audio_path: str, language: str = "en-US"):
        """
        Inicializa o conversor de áudio para texto.
        
        Args:
            audio_path: Caminho para o arquivo de áudio
            language: Código do idioma para reconhecimento (padrão: inglês)
        """
        self.audio_path = audio_path
        self.language = language
        self.recognizer = sr.Recognizer()
        
        # Ajustar parâmetros de reconhecimento
        self.recognizer.energy_threshold = 300  # Aumentar para ambientes barulhentos
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8  # Tempo de pausa entre frases
    
    def convert_full_audio(self) -> Dict[str, Any]:
        """
        Converte o arquivo de áudio completo em texto.
        
        Returns:
            Dicionário com texto transcrito e informações de confiança
        """
        # Verificar formato do arquivo
        audio_format = self._get_audio_format()
        
        if audio_format == "wav":
            # Processar WAV diretamente
            return self._process_wav_file(self.audio_path)
            
        else:
            # Converter para WAV temporário e processar
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
                temp_path = temp_wav.name
            
            try:
                audio = AudioSegment.from_file(self.audio_path, format=audio_format)
                audio.export(temp_path, format="wav")
                result = self._process_wav_file(temp_path)
                os.remove(temp_path)
                return result
            except Exception as e:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                return {"error": f"Erro na conversão: {str(e)}", "transcription": ""}
            
    