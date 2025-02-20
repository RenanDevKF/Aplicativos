from typing import Dict, List, Tuple, Union
import numpy as np
from ..comparator.text_comparator import TextComparator
from ..utils.web_handler import fetch_web_text
from ..utils.file_handler import read_file

class CandidateMatcher:
    """
    Classe para ajudar candidatos a encontrar e analisar vagas compatíveis com seu perfil
    """
    def __init__(self, curriculo_path: str):
        """
        Inicializa o matcher com o caminho do currículo do candidato
        
        Args:
            curriculo_path: Caminho do arquivo do currículo do candidato
        """
        self.curriculo = read_file(curriculo_path)
        self.comparator = TextComparator()
    
    def analisar_vaga(self, job_url: str) -> Dict:
        """
        Analisa uma vaga específica em relação ao currículo do candidato
        
        Args:
            job_url: URL da vaga de emprego
            
        Returns:
            Dicionário com análise de compatibilidade e recomendações
        """
        vaga = fetch_web_text(job_url)
        
        # Obtendo métricas de comparação básicas
        resultado_base = self.comparator.compare_texts(self.curriculo, vaga)
        
        # Adaptando o resultado para perspectiva do candidato
        resultado = {
            'compatibilidade_geral': resultado_base['cosine_similarity'],
            'nivel_match': resultado_base['match_level'],
            'habilidades_correspondentes': resultado_base.get('common_terms', []),
            'requisitos_faltantes': resultado_base.get('unique_terms_doc1', []),
            'diferenciais_candidato': resultado_base.get('unique_terms_doc2', []),
        }
        
        # Adicionando recomendações específicas
        resultado['recomendacoes'] = self._gerar_recomendacoes(resultado)
        
        return resultado
    
    def _gerar_recomendacoes(self, resultado: Dict) -> List[str]:
        """
        Gera recomendações personalizadas com base na análise
        
        Args:
            resultado: Dicionário com resultados da análise
            
        Returns:
            Lista de recomendações para o candidato
        """
        recomendacoes = []
        
        # Recomendações baseadas no nível de compatibilidade
        if resultado['nivel_match'] == 'Alto':
            recomendacoes.append("Seu perfil é bastante compatível com esta vaga. Considere destacar suas experiências com: " + 
                               ", ".join(resultado['habilidades_correspondentes'][:5]))
        elif resultado['nivel_match'] == 'Médio':
            recomendacoes.append("Você tem compatibilidade moderada. Para aumentar suas chances, enfatize suas experiências com: " + 
                               ", ".join(resultado['habilidades_correspondentes'][:3]))
            if resultado['requisitos_faltantes']:
                recomendacoes.append("Considere adquirir ou destacar conhecimentos em: " + 
                                   ", ".join(resultado['requisitos_faltantes'][:3]))
        else:
            if resultado['habilidades_correspondentes']:
                recomendacoes.append("Destaque estas habilidades compatíveis: " + 
                                   ", ".join(resultado['habilidades_correspondentes'][:3]))
            recomendacoes.append("Para aumentar sua compatibilidade, busque desenvolver conhecimentos em: " + 
                               ", ".join(resultado['requisitos_faltantes'][:5]))
        
        # Destaque de diferenciais
        if resultado['diferenciais_candidato'] and len(resultado['diferenciais_candidato']) > 2:
            recomendacoes.append("Seus diferenciais que podem ser destacados: " + 
                               ", ".join(resultado['diferenciais_candidato'][:3]))
        
        return recomendacoes
    
    def classificar_vagas(self, lista_vagas: List[Dict]) -> List[Dict]:
        """
        Classifica uma lista de vagas por compatibilidade com o currículo
        
        Args:
            lista_vagas: Lista de dicionários contendo vagas (com chaves 'id', 'titulo', 'url')
            
        Returns:
            Lista de vagas ordenadas por compatibilidade, com análise incluída
        """
        resultados = []
        
        for vaga in lista_vagas:
            analise = self.analisar_vaga(vaga['url'])
            
            resultados.append({
                'id_vaga': vaga['id'],
                'titulo': vaga['titulo'],
                'compatibilidade': analise['compatibilidade_geral'],
                'nivel_match': analise['nivel_match'],
                'analise_detalhada': analise
            })
        
        # Ordenando por compatibilidade (maior para menor)
        resultados_ordenados = sorted(resultados, 
                                     key=lambda x: x['compatibilidade'], 
                                     reverse=True)
        
        return resultados_ordenados
    
    def recomendar_melhorias_curriculo(self, vagas_alvo: List[str]) -> Dict:
        """
        Analisa múltiplas vagas de interesse e sugere melhorias no currículo
        
        Args:
            vagas_alvo: Lista de URLs de vagas que interessam ao candidato
            
        Returns:
            Dicionário com recomendações consolidadas
        """
        todos_requisitos = []
        habilidades_candidato = set(self.comparator.preprocess_texts(self.curriculo, "")[0])

        for job_url in vagas_alvo:
            analise = self.analisar_vaga(job_url)
            requisitos_faltantes = [req for req in analise['requisitos_faltantes'] if req not in habilidades_candidato]
            todos_requisitos.extend(requisitos_faltantes)
        
        # Contando frequência dos requisitos
        from collections import Counter
        contador_requisitos = Counter(todos_requisitos)
        top_requisitos = contador_requisitos.most_common(10)
        
        return {
            'habilidades_prioritarias': [req for req, _ in top_requisitos],
            'sugestao_melhoria': (
                "Com base nas vagas analisadas, considere desenvolver ou destacar "
                f"estas habilidades em seu currículo: {', '.join([req for req, _ in top_requisitos[:5]])}."
            )
        }
