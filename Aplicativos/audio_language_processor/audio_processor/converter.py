import speech_recognition as sr
from pydub import AudioSegment
import os
import tempfile
from typing import Dict, Any, Optional
import logging

# Configuração de log
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class AudioToTextConverter:
    """
    Classe para converter arquivos de áudio em texto usando reconhecimento de fala.
    
    Attributes:
        audio_path (str): Caminho do arquivo de áudio a ser processado.
        language (str): Código do idioma para reconhecimento de fala.
        recognizer (sr.Recognizer): Instância do reconhecedor de fala do SpeechRecognition.
    """
    
    def __init__(self, audio_path: str, language: str = "en-US"):
        """
        Inicializa a classe de conversão de áudio para texto.
        
        Args:
            audio_path (str): Caminho do arquivo de áudio.
            language (str, opcional): Código do idioma para reconhecimento. Padrão: "en-US".
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
        Converte o arquivo de áudio completo para texto.
        
        Returns:
            dict: Dicionário contendo a transcrição e informações de confiança.
            Exemplo:
                {
                    "transcription": "Texto reconhecido",
                    "confidence": 0.95,
                    "alternatives": ["Alternativa1", "Alternativa2"]
                }
        """
        audio_format = self._get_audio_format()
        
        if audio_format == "wav":
            return self._process_wav_file(self.audio_path)
        else:
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
        Processa um arquivo de áudio no formato WAV e realiza o reconhecimento de fala.
        
        Args:
            wav_path (str): Caminho do arquivo WAV a ser processado.
        
        Returns:
            dict: Dicionário contendo a transcrição, confiança e alternativas.
        """
        try:
            with sr.AudioFile(wav_path) as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio_data = self.recognizer.record(source)
                
                try:
                    result = self.recognizer.recognize_google(audio_data, language=self.language, show_all=True)
                    
                    if result and isinstance(result, dict) and "alternative" in result:
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
        Obtém o formato do arquivo de áudio com base na extensão do nome do arquivo.
        
        Returns:
            str: O formato do arquivo de áudio (exemplo: "mp3", "wav", etc.).
        
        Raises:
            ValueError: Se o formato do arquivo não for suportado.
        """
        extension = os.path.splitext(self.audio_path)[1].lower()
        if extension.startswith('.'):
            extension = extension[1:]
            
        if extension in ["mp3", "wav", "flac", "ogg", "m4a"]:
            return extension
        else:
            try:
                AudioSegment.from_file(self.audio_path)
                return "wav"  # Formato padrão se não for possível determinar
            except Exception as e:
                logging.error(f"Erro ao tentar determinar formato: {str(e)}")
                raise ValueError(f"Formato de arquivo não suportado: {extension}")
