import speech_recognition as sr
from pydub import AudioSegment
import os
import tempfile
from typing import Dict, Any, Optional
import logging

# Configuração de log
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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
                logging.error(f"Erro na conversão de áudio: {str(e)}")
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                return {"error": f"Erro na conversão: {str(e)}", "transcription": ""}
            
    def _process_wav_file(self, wav_path: str) -> Dict[str, Any]:
        """
        Processa um arquivo WAV com a biblioteca speech_recognition.
        
        Args:
            wav_path: Caminho para o arquivo WAV
            
        Returns:
            Dicionário com texto transcrito e informações de confiança
        """
        try:
            with sr.AudioFile(wav_path) as source:
                # Ajustar para ruído ambiente
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Obter áudio
                audio_data = self.recognizer.record(source)
                
                # Tentar reconhecer com Google (mais preciso)
                try:
                    result = self.recognizer.recognize_google(
                        audio_data, 
                        language=self.language,
                        show_all=True
                    )
                    
                    if result and isinstance(result, dict) and "alternative" in result:
                        # Obter a alternativa mais confiável
                        best_result = result["alternative"][0]
                        return {
                            "transcription": best_result["transcript"],
                            "confidence": best_result.get("confidence", 0.0),
                            "alternatives": [alt["transcript"] for alt in result["alternative"][1:]]
                        }
                    elif result and isinstance(result, list) and len(result) > 0:
                        return {
                            "transcription": result[0]["transcript"],
                            "confidence": result[0].get("confidence", 0.0),
                            "alternatives": [alt["transcript"] for alt in result[1:]]
                        }
                    else:
                        return {"transcription": "", "confidence": 0.0, "alternatives": []}
                        
                except sr.UnknownValueError:
                    # Fallback para Sphinx (offline, menos preciso)
                    try:
                        text = self.recognizer.recognize_sphinx(audio_data, language=self.language)
                        return {"transcription": text, "confidence": 0.3, "engine": "sphinx"}
                    except Exception as e:
                        logging.error(f"Erro ao tentar usar Sphinx: {str(e)}")
                        return {"transcription": "", "confidence": 0.0, "error": "Fala não reconhecida"}
                
                except Exception as e:
                    logging.error(f"Erro ao reconhecer áudio com Google: {str(e)}")
                    return {"transcription": "", "confidence": 0.0, "error": str(e)}
        
        except Exception as e:
            logging.error(f"Erro ao processar arquivo WAV: {str(e)}")
            return {"transcription": "", "confidence": 0.0, "error": f"Erro ao processar arquivo: {str(e)}"}
        
    
    def _get_audio_format(self) -> str:
        """
        Determina o formato do arquivo de áudio pela extensão.
        
        Returns:
            Formato do arquivo (mp3, wav, etc.)
        """
        extension = os.path.splitext(self.audio_path)[1].lower()
        if extension.startswith('.'):
            extension = extension[1:]
            
        if extension in ["mp3", "wav", "flac", "ogg", "m4a"]:
            return extension
        else:
            # Tentar inferir formato
            try:
                AudioSegment.from_file(self.audio_path)
                return "wav"  # Formato padrão se não for possível determinar
            except Exception as e:
                logging.error(f"Erro ao tentar determinar formato: {str(e)}")
                raise ValueError(f"Formato de arquivo não suportado: {extension}")
