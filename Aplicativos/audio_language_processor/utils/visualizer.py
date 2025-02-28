# Cria visualizações

import matplotlib.pyplot as plt
import numpy as np
import io
import base64
from typing import Dict, Any, List, Optional, Tuple

class AudioVisualizer:
    """Classe para criar visualizações de características de áudio e análises linguísticas."""
    
    def __init__(self, dpi: int = 100, fig_size: Tuple[int, int] = (10, 6)):
        """
        Inicializa o visualizador.
        
        Args:
            dpi: Resolução das imagens geradas
            fig_size: Tamanho da figura em polegadas (largura, altura)
        """
        self.dpi = dpi
        self.fig_size = fig_size
        
        # Configuração de estilo
        plt.style.use('ggplot')
    
    def plot_speech_rate(self, speech_analysis: Dict[str, Any]) -> str:
        """
        Cria um gráfico visual da taxa de fala e classificação.
        
        Args:
            speech_analysis: Dicionário com análise de padrões de fala
            
        Returns:
            String com imagem codificada em base64
        """
        if not speech_analysis or "speech_rate" not in speech_analysis:
            return ""
        
        # Extrair dados
        speech_rate = speech_analysis["speech_rate"]
        spm = speech_rate.get("syllables_per_minute", 0)
        
        # Criar figura
        fig, ax = plt.subplots(figsize=self.fig_size)
        
        # Definir faixas de taxa de fala
        rate_ranges = [
            (0, 150, "Lenta", "lightblue"),
            (150, 220, "Moderada-Lenta", "lightgreen"),
            (220, 280, "Moderada", "green"),
            (280, 350, "Moderada-Rápida", "orange"),
            (350, 450, "Rápida", "red")
        ]
        
        # Criar gráfico de barras para faixas
        for i, (start, end, label, color) in enumerate(rate_ranges):
            ax.barh(0, end-start, left=start, height=0.5, color=color, alpha=0.6)
            ax.text((start+end)/2, 0, label, ha='center', va='center', color='black')
        
        # Marcar a taxa de fala do usuário
        ax.plot(spm, 0, 'ro', ms=10, color='navy')
        ax.annotate(f"{spm:.1f} sílabas/min", 
                   xy=(spm, 0), xytext=(spm, 0.2),
                   arrowprops=dict(arrowstyle='->'), ha='center')
        
        # Configurar eixos
        ax.set_yticks([])
        ax.set_xlabel("Sílabas por Minuto")
        ax.set_title("Taxa de Fala")
        ax.set_xlim(0, 450)
        
        # Converter para base64
        return self._fig_to_base64(fig)
    
    
    def plot_pronunciation_comparison(self, pronunciation_analysis: Dict[str, Any]) -> str:
        """
        Cria um gráfico visual comparando pronúncia do usuário com referência.
        
        Args:
            pronunciation_analysis: Dicionário com análise de pronúncia
            
        Returns:
            String com imagem codificada em base64
        """
        if not pronunciation_analysis or "similarity_percentage" not in pronunciation_analysis:
            return ""
        
        # Extrair dados
        similarity = pronunciation_analysis.get("similarity_percentage", 0)
        correlation = pronunciation_analysis.get("correlation", 0)
        score = pronunciation_analysis.get("pronunciation_score", 0)
        
        # Criar figura
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=self.fig_size)
        
        # Gráfico 1: Medidor de similaridade
        self._create_gauge(ax1, similarity, "Similaridade", "%")
        
        # Gráfico 2: Pontuação geral
        categories = ['Pronúncia', 'Entonação', 'Ritmo', 'Fluência']
        
        # Valores de exemplo (ajustar conforme necessário)
        values = [
            score, 
            min(max(correlation * 100, 0), 100),
            min(max((similarity - 20), 0), 100),  # Valor derivado da similaridade
            min(max((score - 10), 0), 100)      # Valor derivado da pontuação
        ]
        
        # Normalizar valores para 0-1
        values = [v / 100 for v in values]
        
        # Configurar radar chart
        angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
        angles += angles[:1]  # Fechar o polígono
        values += values[:1]  # Fechar o polígono
        
        ax2.polar(angles, values, marker='o')
        ax2.fill(angles, values, alpha=0.3)
        ax2.set_xticks(angles[:-1])
        ax2.set_xticklabels(categories)
        ax2.set_yticks([0.25, 0.5, 0.75, 1.0])
        ax2.set_yticklabels(['25', '50', '75', '100'])
        ax2.set_title("Pontuação por Categoria")
        
        plt.tight_layout()
        
        # Converter para base64
        return self._fig_to_base64(fig)