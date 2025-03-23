# lotofacil_analyzer/data/processor.py

import pandas as pd
import os
from pathlib import Path
from django.conf import settings
import numpy as np
from typing import List, Dict, Tuple, Any

class LotofacilDataImporter:
    """
    Classe responsável por importar e processar os dados da Lotofácil a partir de arquivos XLSX.
    """
    
    def __init__(self, file_path=None):
        """
        Inicializa o importador de dados.
        
        Args:
            file_path (str, optional): Caminho para o arquivo XLSX. Se None, usará o arquivo padrão.
        """
        self.file_path = file_path
        if not file_path:
            # Usar caminho padrão dentro da pasta data
            data_dir = Path(settings.BASE_DIR) / 'lotofacil_analyzer' / 'data' / 'files'
            os.makedirs(data_dir, exist_ok=True)
            self.file_path = data_dir / 'base_dados.xlsx'
        
        self.resultados = None
        
    
    def importar_xlsx(self) -> pd.DataFrame:
        """
        Importa os dados do arquivo XLSX.
        
        Returns:
            DataFrame: DataFrame pandas com os resultados da Lotofácil
        """
        try:
            df = pd.read_excel(self.file_path)
            # Renomear colunas para um formato padrão, se necessário
            self._normalizar_colunas(df)
            self.resultados = df
            return df
        except Exception as e:
            raise Exception(f"Erro ao importar o arquivo XLSX: {str(e)}")
    
    def _normalizar_colunas(self, df: pd.DataFrame) -> None:
        """
        Normaliza os nomes das colunas do DataFrame para um formato padrão.
        
        Args:
            df (DataFrame): DataFrame a ser normalizado
        """
        # Mapeamento de possíveis nomes de colunas para nomes padronizados
        mapeamento_colunas = {
            'concurso': 'concurso',
            'Concurso': 'concurso',
            'CONCURSO': 'concurso',
            'numero_concurso': 'concurso',
            
            'data': 'data',
            'Data': 'data',
            'DATA': 'data',
            'data_sorteio': 'data',
            
            # Mapeamento para bolas sorteadas
            'bola_1': 'bola_1',
            'Bola 1': 'bola_1',
            '1ª Dezena': 'bola_1',
            # ... adicione mais mapeamentos conforme necessário
        }
        
        # Identificar padrão de colunas do arquivo
        # Se as colunas forem numeradas de 1 a 15 sem prefixo
        numeros_colunas = [str(i) for i in range(1, 16)]
        if all(col in df.columns for col in numeros_colunas):
            for i in range(1, 16):
                df.rename(columns={str(i): f'bola_{i}'}, inplace=True)
        
        # Se as colunas forem nomeadas com bola_X ou similar
        colunas_renomeadas = {}
        for col in df.columns:
            col_lower = col.lower()
            # Verificar mapeamentos conhecidos
            if col in mapeamento_colunas:
                colunas_renomeadas[col] = mapeamento_colunas[col]
            # Detectar padrões de colunas de bolas
            elif 'bola' in col_lower or 'dezena' in col_lower:
                for i in range(1, 16):
                    if str(i) in col or f'_{i}' in col or f' {i}' in col:
                        colunas_renomeadas[col] = f'bola_{i}'
                        break
        
        # Aplicar renomeações detectadas
        if colunas_renomeadas:
            df.rename(columns=colunas_renomeadas, inplace=True)
    
    def processar_dados(self) -> Dict[str, Any]:
        """
        Processa os dados importados e prepara estruturas de dados para análise.
        
        Returns:
            Dict: Dicionário contendo diferentes representações dos dados
        """
        if self.resultados is None:
            self.importar_xlsx()
        
        dados_processados = {
            'df': self.resultados,
            'matriz_resultados': self._criar_matriz_resultados(),
            'frequencia_numeros': self._calcular_frequencia_numeros(),
            'ultimo_concurso': self._obter_ultimo_concurso(),
            'historico_completo': self._criar_historico_completo()
        }
        
        return dados_processados
    
    
    
    def _calcular_frequencia_numeros(self) -> Dict[int, int]:
        """
        Calcula a frequência de cada número nos sorteios.
        
        Returns:
            Dict: Dicionário com a frequência de cada número
        """
        matriz = self._criar_matriz_resultados()
        frequencias = {}
        
        for num in range(1, 26):
            frequencias[num] = np.sum(matriz[:, num-1])
            
        return frequencias
    
    def _obter_ultimo_concurso(self) -> Dict[str, Any]:
        """
        Obtém os dados do último concurso realizado.
        
        Returns:
            Dict: Dados do último concurso
        """
        if self.resultados is None or len(self.resultados) == 0:
            return {}
            
        ultimo = self.resultados.iloc[-1].to_dict()
        
        # Extrair os números sorteados
        numeros_sorteados = []
        for i in range(1, 16):
            col_name = f'bola_{i}'
            if col_name in ultimo:
                numeros_sorteados.append(int(ultimo[col_name]))
        
        return {
            'concurso': ultimo.get('concurso', None),
            'data': ultimo.get('data', None),
            'numeros_sorteados': sorted(numeros_sorteados)
        }
    
    
    
    def salvar_dados_processados(self, output_path=None):
        """
        Salva os dados processados em formato serializado para uso rápido.
        
        Args:
            output_path (str, optional): Caminho para salvar os dados processados.
        """
        import pickle
        
        if not output_path:
            output_dir = Path(settings.BASE_DIR) / 'lotofacil_analyzer' / 'data' / 'processed'
            os.makedirs(output_dir, exist_ok=True)
            output_path = output_dir / 'dados_processados.pkl'
        
        dados = self.processar_dados()
        
        with open(output_path, 'wb') as f:
            pickle.dump(dados, f)