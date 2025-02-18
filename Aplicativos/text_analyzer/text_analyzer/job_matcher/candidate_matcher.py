from typing import Dict, List, Tuple, Union
import numpy as np
from ..comparator.text_comparator import TextComparator

class CandidateMatcher:
    """
    Classe para ajudar candidatos a encontrar e analisar vagas compatíveis com seu perfil
    """
    def __init__(self, curriculo: str):
        """
        Inicializa o matcher com o currículo do candidato
        
        Args:
            curriculo: Texto do currículo do candidato
        """
        self.curriculo = curriculo
        self.comparator = TextComparator()