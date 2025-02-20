from typing import Dict, List, Tuple, Union
import numpy as np
from ..comparator.text_comparator import TextComparator
from ..utils.web_handler import fetch_web_text
from ..utils.file_handler import read_file

class CandidateMatcher:
    """
    Classe responsável por analisar vagas de emprego e compará-las com o currículo do candidato.
    """
    def __init__(self, curriculo_path: str):
        """
        Inicializa o CandidateMatcher com o currículo do candidato.
        
        Args:
            curriculo_path (str): Caminho do arquivo contendo o currículo do candidato.
        """
        self.curriculo = read_file(curriculo_path)
        self.comparator = TextComparator()
    
    def analisar_vaga(self, job_url: str) -> Dict:
        """
        Compara o currículo do candidato com a descrição de uma vaga.
        
        Args:
            job_url (str): URL da vaga de emprego.
            
        Returns:
            dict: Dicionário contendo a análise de compatibilidade, habilidades correspondentes e recomendações.
        """
        vaga = fetch_web_text(job_url)
        
        # Obtendo métricas de comparação
        resultado_base = self.comparator.compare_texts(self.curriculo, vaga)
        
        # Estruturando o resultado da análise
        resultado = {
            'compatibilidade_geral': resultado_base['cosine_similarity'],
            'nivel_match': resultado_base['match_level'],
            'habilidades_correspondentes': resultado_base.get('common_terms', []),
            'requisitos_faltantes': resultado_base.get('unique_terms_doc1', []),
            'diferenciais_candidato': resultado_base.get('unique_terms_doc2', []),
        }
        
        # Gerando recomendações
        resultado['recomendacoes'] = self._gerar_recomendacoes(resultado)
        
        return resultado
    
    def _gerar_recomendacoes(self, resultado: Dict) -> List[str]:
        """
        Gera recomendações para o candidato com base na análise da vaga.
        
        Args:
            resultado (dict): Dicionário contendo os resultados da análise.
        
        Returns:
            list: Lista de recomendações personalizadas para o candidato.
        """
        recomendacoes = []
        
        if resultado['nivel_match'] == 'Alto':
            recomendacoes.append(
                "Seu perfil é altamente compatível com esta vaga. Destaque suas experiências com: " + 
                ", ".join(resultado['habilidades_correspondentes'][:5])
            )
        elif resultado['nivel_match'] == 'Médio':
            recomendacoes.append(
                "Compatibilidade moderada. Para aumentar suas chances, enfatize suas experiências com: " + 
                ", ".join(resultado['habilidades_correspondentes'][:3])
            )
            if resultado['requisitos_faltantes']:
                recomendacoes.append(
                    "Considere desenvolver conhecimentos em: " + 
                    ", ".join(resultado['requisitos_faltantes'][:3])
                )
        else:
            if resultado['habilidades_correspondentes']:
                recomendacoes.append(
                    "Destaque suas habilidades compatíveis: " + 
                    ", ".join(resultado['habilidades_correspondentes'][:3])
                )
            recomendacoes.append(
                "Para aumentar sua compatibilidade, busque desenvolver conhecimentos em: " + 
                ", ".join(resultado['requisitos_faltantes'][:5])
            )
        
        if resultado['diferenciais_candidato'] and len(resultado['diferenciais_candidato']) > 2:
            recomendacoes.append(
                "Seus diferenciais que podem ser destacados: " + 
                ", ".join(resultado['diferenciais_candidato'][:3])
            )
        
        return recomendacoes
    
    def classificar_vagas(self, lista_vagas: List[Dict]) -> List[Dict]:
        """
        Classifica uma lista de vagas de emprego com base na compatibilidade com o currículo do candidato.
        
        Args:
            lista_vagas (list): Lista de dicionários contendo informações sobre as vagas (id, título, URL).
        
        Returns:
            list: Lista de vagas ordenadas por nível de compatibilidade.
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
        
        # Ordena as vagas por compatibilidade em ordem decrescente
        resultados_ordenados = sorted(resultados, key=lambda x: x['compatibilidade'], reverse=True)
        
        return resultados_ordenados
    
    def recomendar_melhorias_curriculo(self, vagas_alvo: List[str]) -> Dict:
        """
        Analisa múltiplas vagas e sugere melhorias no currículo do candidato.
        
        Args:
            vagas_alvo (list): Lista de URLs das vagas de interesse.
        
        Returns:
            dict: Dicionário contendo sugestões de aprimoramento do currículo.
        """
        todos_requisitos = []
        habilidades_candidato = set(self.comparator.preprocess_texts(self.curriculo, "")[0])

        for job_url in vagas_alvo:
            analise = self.analisar_vaga(job_url)
            requisitos_faltantes = [req for req in analise['requisitos_faltantes'] if req not in habilidades_candidato]
            todos_requisitos.extend(requisitos_faltantes)
        
        # Contabiliza a frequência dos requisitos mais comuns
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
