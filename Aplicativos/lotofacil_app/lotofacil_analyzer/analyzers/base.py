# lotofacil_analyzer/analyzers/base.py
from abc import ABC, abstractmethod
import pandas as pd
from ..models import SorteioLotofacil, AnaliseEstatistica

class AnalisadorBase(ABC):
    """Classe base para todos os analisadores de Lotofácil"""
    
    def __init__(self, df=None, ultimos_n=None):
        """
        Inicializa o analisador.
        
        Args:
            df (pd.DataFrame, optional): DataFrame com os dados dos sorteios.
            ultimos_n (int, optional): Analisar apenas os últimos N sorteios.
        """
        self.nome = self.__class__.__name__
        
        if df is None:
            # Se nenhum DataFrame for fornecido, busca os dados do banco de dados
            query = SorteioLotofacil.objects.all().order_by('-concurso')
            if ultimos_n:
                query = query[:ultimos_n]
            self.df = self._criar_dataframe(query)
        else:
            # Usa o DataFrame fornecido
            self.df = df
        
        self.resultados = {}
    
    def _criar_dataframe(self, sorteios):
        """
        Converte uma lista de objetos SorteioLotofacil em um DataFrame.
        
        Args:
            sorteios (list): Lista de objetos SorteioLotofacil.
        
        Returns:
            pd.DataFrame: DataFrame com os dados dos sorteios.
        """
        dados = []
        for sorteio in sorteios:
            row = {
                'concurso': sorteio.concurso,
                'data': sorteio.data,
                'numeros': sorteio.get_numeros_list()
            }
            dados.append(row)
        return pd.DataFrame(dados)
    
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