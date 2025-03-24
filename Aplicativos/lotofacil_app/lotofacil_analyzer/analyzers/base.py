# lotofacil_analyzer/analyzers/base.py
from abc import ABC, abstractmethod
import pandas as pd
from ..models import AnaliseEstatistica  # Remova SorteioLotofacil se não for usado

class AnalisadorBase(ABC):
    """Classe base para todos os analisadores de Lotofácil"""
    
    def __init__(self, df=None, arquivo_excel=None, ultimos_n=None):
        """
        Inicializa o analisador.
        
        Args:
            df (pd.DataFrame, optional): DataFrame com os dados dos sorteios.
            arquivo_excel (str, optional): Caminho para o arquivo Excel com os dados.
            ultimos_n (int, optional): Analisar apenas os últimos N sorteios.
        """
        self.nome = self.__class__.__name__
        
        if df is None:
            if arquivo_excel:
                # Carrega os dados do arquivo Excel
                self.df = self._carregar_excel(arquivo_excel)
            else:
                raise ValueError("Nenhum DataFrame ou arquivo Excel fornecido.")
        else:
            # Usa o DataFrame fornecido
            self.df = df
        
        # Filtra os últimos N sorteios, se necessário
        if ultimos_n:
            self.df = self.df.head(ultimos_n)
        
        self.resultados = {}
        
        # Garantir que a coluna 'numeros' exista
        if 'numeros' not in self.df.columns:
            numeros_colunas = [f'Bola{i}' for i in range(1, 16)]
            self.df['numeros'] = self.df[numeros_colunas].values.tolist()
        
    def _carregar_excel(self, arquivo_excel):
        """
        Carrega os dados do arquivo Excel e prepara o DataFrame.
        
        Args:
            arquivo_excel (str): Caminho para o arquivo Excel.
        
        Returns:
            pd.DataFrame: DataFrame com os dados dos sorteios.
        """
        # Carrega o arquivo Excel
        df = pd.read_excel(arquivo_excel)
        
        # Verifica se as colunas necessárias existem
        colunas_necessarias = ['Concurso', 'Data Sorteio'] + [f'Bola{i}' for i in range(1, 16)]
        for coluna in colunas_necessarias:
            if coluna not in df.columns:
                raise ValueError(f"Coluna '{coluna}' não encontrada no arquivo Excel.")
        
        # Converte as colunas de números em uma lista na coluna 'numeros'
        df['numeros'] = df[[f'Bola{i}' for i in range(1, 16)]].values.tolist()
        
        return df
    
    @abstractmethod
    def analisar(self):
        """
        Método principal para executar a análise
        Deve ser implementado por cada classe filha
        
        Returns:
            dict: Resultados da análise
        """
        pass
    
    def salvar_resultados(self):
        """Salva os resultados da análise no banco de dados"""
        if not self.resultados:
            self.analisar()
        
        analise = AnaliseEstatistica(
            tipo=self.nome,
            resultados=self.resultados
        )
        analise.save()
        return analise
    
    def obter_resultados(self, force_new=False):
        """
        Obtém os resultados da análise
        
        Args:
            force_new (bool): Se True, força recalcular mesmo se já existir
            
        Returns:
            dict: Resultados da análise
        """
        if not self.resultados or force_new:
            self.analisar()
        return self.resultados