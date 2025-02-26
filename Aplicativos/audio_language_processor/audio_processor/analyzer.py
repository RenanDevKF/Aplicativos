# Analisa carcteristicas de um audio

import numpy as np
import scipy.stats
from typing import Dict, List, Any

class AudioAnalyzer:
    """Classe para analisar características extraídas de áudio para estudo de idiomas."""
    
    def __init__(self, extractor):
        """
        Inicializa o analisador com um extrator de áudio.
        
        Args:
            extractor: Instância de AudioExtractor
        """
        self.extractor = extractor