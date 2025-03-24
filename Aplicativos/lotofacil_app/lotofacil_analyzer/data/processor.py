# lotofacil_analyzer/data/processor.py

import pandas as pd
import os
from pathlib import Path
from django.conf import settings
import numpy as np
from typing import List, Dict, Tuple, Any

class LotofacilDataImporter:
    """
    Classe responsável por importar e processar os dados da Lotofácil a partir de arquivos CSV.
    """
    
    print("Módulo processor.py sendo carregado...")  # Adicione esta linha no início do arquivo

class LotofacilDataImporter:
    def __init__(self, file_path=None):
        print(f"Inicializando LotofacilDataImporter com file_path: {file_path}")  # Adicione esta linha
        self.file_path = file_path
        if not file_path:
            data_dir = Path(settings.BASE_DIR) / 'lotofacil_analyzer' / 'data' / 'files'
            os.makedirs(data_dir, exist_ok=True)
            self.file_path = data_dir / 'base_dados.csv'
        
        self.resultados = None
    
    def importar_csv(self) -> pd.DataFrame:
        print("Método importar_csv sendo chamado...")  # Adicione esta linha
        try:
            # Verificar se o arquivo existe
            print(f"Tentando ler o arquivo: {self.file_path}")
            if not os.path.exists(self.file_path):
                raise FileNotFoundError(f"Arquivo não encontrado: {self.file_path}")
            
            # Ler o CSV 
            df = pd.read_csv(self.file_path)
            
            # Criar coluna de números
            bolas_colunas = [f'Bola{i}' for i in range(1, 16)]
            df['numeros'] = df[bolas_colunas].apply(
                lambda row: [int(row[col]) for col in bolas_colunas], 
                axis=1
            )
            
            self.resultados = df
            return df
        except Exception as e:
            print(f"Erro detalhado: {e}")  # Adicione esta linha
            raise Exception(f"Erro ao importar o arquivo CSV: {str(e)}")
        
        def _normalizar_colunas(self, df: pd.DataFrame) -> pd.DataFrame:
            """
            Normaliza os nomes das colunas do DataFrame para um formato padrão.
            
            Args:
                df (DataFrame): DataFrame a ser normalizado
            
            Returns:
                DataFrame: DataFrame com colunas normalizadas
            """
            # Renomear colunas para garantir um padrão consistente
            colunas_mapeadas = {
                col: col.lower().replace(' ', '_') for col in df.columns
            }
            df = df.rename(columns=colunas_mapeadas)
            
            # Criar coluna 'numeros'
            bolas_colunas = [f'bola{i}' for i in range(1, 16)]
            
            # Converter bolas para lista de inteiros
            df['numeros'] = df[bolas_colunas].apply(
                lambda row: [int(row[col]) for col in bolas_colunas], 
                axis=1
            )
            
            return df
    
    def processar_dados(self) -> Dict[str, Any]:
        """
        Processa os dados importados e prepara estruturas de dados para análise.
        
        Returns:
            Dict: Dicionário contendo diferentes representações dos dados
        """
        if self.resultados is None:
            self.importar_csv()
        
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