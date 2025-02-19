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
    
    def analisar_vaga(self, vaga: str) -> Dict:
        """
        Analisa uma vaga específica em relação ao currículo do candidato
        
        Args:
            vaga: Texto da vaga de emprego
            
        Returns:
            Dicionário com análise de compatibilidade e recomendações
        """
        # Obtendo métricas de comparação básicas
        resultado_base = self.comparator.compare_documents(vaga, self.curriculo)
        
        # Adaptando o resultado para perspectiva do candidato
        resultado = {
            'compatibilidade_geral': resultado_base['cosine_similarity'],
            'nivel_match': resultado_base['match_level'],
            'habilidades_correspondentes': resultado_base['common_terms'],
            'requisitos_faltantes': resultado_base['unique_terms_doc1'],
            'diferenciais_candidato': resultado_base['unique_terms_doc2'],
        }
        
        # Adicionando recomendações específicas
        resultado['recomendacoes'] = self._gerar_recomendacoes(resultado)
        
        return resultado    