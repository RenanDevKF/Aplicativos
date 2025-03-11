import matplotlib.pyplot as plt
import numpy as np
import io
import base64
from typing import Dict, Any, List, Optional, Tuple

class AudioVisualizer:
    """Classe para criar visualizações de características de áudio e análises linguísticas."""
    
    def __init__(self, dpi: int = 100, fig_size: Tuple[int, int] = (10, 6)):
        """
        Inicializa o visualizador de áudio.
        
        :param dpi: Resolução da figura em pontos por polegada.
        :param fig_size: Tamanho da figura em polegadas (largura, altura).
        """
        self.dpi = dpi
        self.fig_size = fig_size
        plt.style.use('ggplot')
    
    def plot_speech_rate(self, speech_analysis: Dict[str, Any]) -> str:
        """
        Cria um gráfico visual da taxa de fala e sua classificação.
        
        :param speech_analysis: Dicionário contendo os dados de análise da taxa de fala.
        :return: String da imagem codificada em base64.
        :raises ValueError: Se os dados de entrada não forem um dicionário.
        :raises KeyError: Se a chave 'speech_rate' estiver ausente nos dados de análise.
        """
        try:
            if not isinstance(speech_analysis, dict):
                raise ValueError("Os dados de análise devem ser um dicionário válido.")
            if "speech_rate" not in speech_analysis:
                raise KeyError("Chave 'speech_rate' ausente nos dados de análise.")

            speech_rate = speech_analysis["speech_rate"]
            spm = speech_rate.get("syllables_per_minute", 0)

            # Criar figura
            fig, ax = plt.subplots(figsize=self.fig_size)

            rate_ranges = [
                (0, 150, "Lenta", "lightblue"),
                (150, 220, "Moderada-Lenta", "lightgreen"),
                (220, 280, "Moderada", "green"),
                (280, 350, "Moderada-Rápida", "orange"),
                (350, 450, "Rápida", "red")
            ]

            for start, end, label, color in rate_ranges:
                ax.barh(0, end-start, left=start, height=0.5, color=color, alpha=0.6)
                ax.text((start+end)/2, 0, label, ha='center', va='center', color='black')

            ax.plot(spm, 0, 'ro', ms=10, color='navy')
            ax.annotate(f"{spm:.1f} sílabas/min", xy=(spm, 0), xytext=(spm, 0.2),
                        arrowprops=dict(arrowstyle='->'), ha='center')

            ax.set_yticks([])
            ax.set_xlabel("Sílabas por Minuto")
            ax.set_title("Taxa de Fala")
            ax.set_xlim(0, 450)

            return self._fig_to_base64(fig)
        
        except (KeyError, ValueError) as e:
            print(f"Erro ao gerar gráfico de taxa de fala: {e}")
            return ""

    def plot_pronunciation_comparison(self, pronunciation_analysis: Dict[str, Any]) -> str:
        """
        Cria um gráfico visual comparando a pronúncia do usuário com a referência.
        
        :param pronunciation_analysis: Dicionário contendo os dados de análise da pronúncia.
        :return: String da imagem codificada em base64.
        :raises ValueError: Se os dados de entrada não forem um dicionário.
        :raises KeyError: Se a chave 'similarity_percentage' estiver ausente.
        """
        try:
            if not isinstance(pronunciation_analysis, dict):
                raise ValueError("Os dados de análise devem ser um dicionário válido.")
            if "similarity_percentage" not in pronunciation_analysis:
                raise KeyError("Chave 'similarity_percentage' ausente nos dados de análise.")

            similarity = pronunciation_analysis.get("similarity_percentage", 0)
            correlation = pronunciation_analysis.get("correlation", 0)
            score = pronunciation_analysis.get("pronunciation_score", 0)

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=self.fig_size)

            self._create_gauge(ax1, similarity, "Similaridade", "%")
            
            return self._fig_to_base64(fig)
        
        except (KeyError, ValueError) as e:
            print(f"Erro ao gerar gráfico de comparação de pronúncia: {e}")
            return ""
    
    def _fig_to_base64(self, fig) -> str:
        """
        Converte uma figura matplotlib para string base64.
        
        :param fig: Objeto da figura do matplotlib.
        :return: String base64 representando a imagem.
        """
        try:
            buffer = io.BytesIO()
            fig.savefig(buffer, format='png', dpi=self.dpi)
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()
            plt.close(fig)
            return base64.b64encode(image_png).decode('utf-8')
        
        except Exception as e:
            print(f"Erro ao converter gráfico para base64: {e}")
            return ""
