import matplotlib.pyplot as plt
import numpy as np
import io
import base64
from typing import Dict, Any, List, Optional, Tuple

class AudioVisualizer:
    """Classe para criar visualizações de características de áudio e análises linguísticas."""
    
    def __init__(self, dpi: int = 100, fig_size: Tuple[int, int] = (10, 6)):
        """Inicializa o visualizador."""
        self.dpi = dpi
        self.fig_size = fig_size
        plt.style.use('ggplot')
    
    def plot_speech_rate(self, speech_analysis: Dict[str, Any]) -> str:
        """Cria um gráfico visual da taxa de fala e classificação."""
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
        """Cria um gráfico visual comparando pronúncia do usuário com referência."""
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

            categories = ['Pronúncia', 'Entonação', 'Ritmo', 'Fluência']
            values = [
                score, 
                min(max(correlation * 100, 0), 100),
                min(max((similarity - 20), 0), 100),
                min(max((score - 10), 0), 100)
            ]
            values = [v / 100 for v in values]

            angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
            angles += angles[:1]
            values += values[:1]

            ax2.polar(angles, values, marker='o')
            ax2.fill(angles, values, alpha=0.3)
            ax2.set_xticks(angles[:-1])
            ax2.set_xticklabels(categories)
            ax2.set_yticks([0.25, 0.5, 0.75, 1.0])
            ax2.set_yticklabels(['25', '50', '75', '100'])
            ax2.set_title("Pontuação por Categoria")

            plt.tight_layout()
            return self._fig_to_base64(fig)

        except (KeyError, ValueError) as e:
            print(f"Erro ao gerar gráfico de comparação de pronúncia: {e}")
            return ""

    def plot_vocabulary_stats(self, vocabulary: List[Dict[str, Any]], limit: int = 10) -> str:
        """Cria um gráfico de frequência de vocabulário."""
        try:
            if not isinstance(vocabulary, list) or not all(isinstance(i, dict) for i in vocabulary):
                raise ValueError("Os dados de vocabulário devem ser uma lista de dicionários.")

            vocab_to_plot = vocabulary[:limit]
            words = [item.get("word", "") for item in vocab_to_plot]
            counts = [item.get("count", 0) for item in vocab_to_plot]

            fig, ax = plt.subplots(figsize=self.fig_size)
            bars = ax.barh(words, counts, color='skyblue')

            for bar in bars:
                width = bar.get_width()
                ax.text(width + 0.3, bar.get_y() + bar.get_height()/2, f"{width:.0f}", ha='left', va='center')

            ax.set_xlabel("Frequência")
            ax.set_title("Palavras Mais Frequentes")
            ax.invert_yaxis()
            plt.tight_layout()

            return self._fig_to_base64(fig)

        except ValueError as e:
            print(f"Erro ao gerar gráfico de vocabulário: {e}")
            return ""

    def _create_gauge(self, ax, value: float, label: str, unit: str) -> None:
        """Cria um gráfico de medidor (gauge)."""
        try:
            value = max(0, min(100, value))
            theta = np.linspace(3*np.pi/4, 9*np.pi/4, 100)
            r = 0.8
            x = r * np.cos(theta)
            y = r * np.sin(theta)

            ax.plot(x, y, color='lightgray', linewidth=15, alpha=0.3)

            idx = max(0, min(int((value/100) * 100), 99))
            ax.plot(x[:idx+1], y[:idx+1], color='green', linewidth=15, alpha=0.8)

            ax.text(0, -0.2, f"{value:.1f}{unit}", ha='center', va='center', fontsize=18)
            ax.text(0, 0.3, label, ha='center', va='center', fontsize=14)

            ax.set_xlim(-1, 1)
            ax.set_ylim(-1, 1)
            ax.axis('equal')
            ax.axis('off')

        except Exception as e:
            print(f"Erro ao criar gauge: {e}")

    def _fig_to_base64(self, fig) -> str:
        """Converte uma figura matplotlib para string base64."""
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
