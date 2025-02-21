from typing import Dict, List
import numpy as np
from ..comparator.text_comparator import TextComparator
from ..utils.web_handler import fetch_webpage_text
from ..utils.file_handler import read_file
from collections import Counter

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
        try:
            self.curriculo = read_file(curriculo_path)
            if not self.curriculo:
                raise ValueError("O currículo está vazio ou não pode ser lido.")
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo não encontrado: {curriculo_path}")
        except Exception as e:
            raise RuntimeError(f"Erro ao carregar o currículo: {e}")

        self.comparator = TextComparator()

    def analisar_vaga(self, job_url: str) -> Dict:
        """
        Compara o currículo do candidato com a descrição de uma vaga.

        Args:
            job_url (str): URL da vaga de emprego.
            
        Returns:
            dict: Dicionário contendo a análise de compatibilidade, habilidades correspondentes e recomendações.
        """
        try:
            vaga = fetch_webpage_text(job_url)
            if not vaga:
                raise ValueError(f"Não foi possível obter a descrição da vaga em {job_url}")

            resultado_base = self.comparator.compare_texts(self.curriculo, vaga)
            if not resultado_base:
                raise RuntimeError("Erro na comparação de textos. Nenhum resultado gerado.")

            resultado = {
                'compatibilidade_geral': resultado_base.get('cosine_similarity', 0.0),
                'nivel_match': resultado_base.get('match_level', 'Desconhecido'),
                'habilidades_correspondentes': resultado_base.get('common_terms', []),
                'requisitos_faltantes': resultado_base.get('unique_terms_doc1', []),
                'diferenciais_candidato': resultado_base.get('unique_terms_doc2', []),
                'recomendacoes': self._gerar_recomendacoes(resultado_base),
            }

            return resultado

        except Exception as e:
            return {'erro': f"Erro ao analisar a vaga: {str(e)}"}

    def _gerar_recomendacoes(self, resultado: Dict) -> List[str]:
        """
        Gera recomendações para o candidato com base na análise da vaga.

        Args:
            resultado (dict): Dicionário contendo os resultados da análise.
        
        Returns:
            list: Lista de recomendações personalizadas para o candidato.
        """
        try:
            recomendacoes = []

            nivel_match = resultado.get('nivel_match', 'Baixo')
            habilidades_correspondentes = resultado.get('habilidades_correspondentes', [])
            requisitos_faltantes = resultado.get('requisitos_faltantes', [])
            diferenciais_candidato = resultado.get('diferenciais_candidato', [])

            if nivel_match == 'Alto':
                recomendacoes.append(
                    f"Seu perfil é altamente compatível. Destaque suas experiências com: {', '.join(habilidades_correspondentes[:5])}"
                )
            elif nivel_match == 'Médio':
                recomendacoes.append(
                    f"Compatibilidade moderada. Para aumentar suas chances, enfatize: {', '.join(habilidades_correspondentes[:3])}"
                )
                if requisitos_faltantes:
                    recomendacoes.append(
                        f"Considere desenvolver conhecimentos em: {', '.join(requisitos_faltantes[:3])}"
                    )
            else:
                if habilidades_correspondentes:
                    recomendacoes.append(
                        f"Destaque suas habilidades compatíveis: {', '.join(habilidades_correspondentes[:3])}"
                    )
                recomendacoes.append(
                    f"Para melhorar seu currículo, aprimore-se em: {', '.join(requisitos_faltantes[:5])}"
                )

            if diferenciais_candidato and len(diferenciais_candidato) > 2:
                recomendacoes.append(
                    f"Seus diferenciais incluem: {', '.join(diferenciais_candidato[:3])}"
                )

            return recomendacoes

        except Exception as e:
            return [f"Erro ao gerar recomendações: {str(e)}"]

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
            try:
                analise = self.analisar_vaga(vaga['url'])

                resultados.append({
                    'id_vaga': vaga['id'],
                    'titulo': vaga['titulo'],
                    'compatibilidade': analise.get('compatibilidade_geral', 0.0),
                    'nivel_match': analise.get('nivel_match', 'Desconhecido'),
                    'analise_detalhada': analise
                })
            except Exception as e:
                resultados.append({
                    'id_vaga': vaga['id'],
                    'titulo': vaga['titulo'],
                    'erro': f"Erro ao analisar vaga {vaga['id']}: {str(e)}"
                })

        return sorted(resultados, key=lambda x: x['compatibilidade'], reverse=True)

    def recomendar_melhorias_curriculo(self, vagas_alvo: List[str]) -> Dict:
        """
        Analisa múltiplas vagas e sugere melhorias no currículo do candidato.

        Args:
            vagas_alvo (list): Lista de URLs das vagas de interesse.

        Returns:
            dict: Dicionário contendo sugestões de aprimoramento do currículo.
        """
        try:
            todos_requisitos = []
            habilidades_candidato = set(self.comparator.preprocess_texts(self.curriculo, "")[0])

            for job_url in vagas_alvo:
                analise = self.analisar_vaga(job_url)
                requisitos_faltantes = [req for req in analise.get('requisitos_faltantes', []) if req not in habilidades_candidato]
                todos_requisitos.extend(requisitos_faltantes)

            contador_requisitos = Counter(todos_requisitos)
            top_requisitos = contador_requisitos.most_common(10)

            return {
                'habilidades_prioritarias': [req for req, _ in top_requisitos],
                'sugestao_melhoria': f"Considere desenvolver estas habilidades: {', '.join([req for req, _ in top_requisitos[:5]])}."
            }
        except Exception as e:
            return {'erro': f"Erro ao gerar recomendações de melhoria: {str(e)}"}
