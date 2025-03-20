# lotofacil_analyzer/analyzers/base.py
from abc import ABC, abstractmethod
import pandas as pd
from ..models import SorteioLotofacil, AnaliseEstatistica

class AnalisadorBase(ABC):
    """Classe base para todos os analisadores de Lotofácil"""
    
    def __init__(self, sorteios=None, ultimos_n=None):
        """
        Inicializa o analisador
        
        Args:
            sorteios (list): Lista de objetos SorteioLotofacil ou None para buscar todos
            ultimos_n (int): Analisar apenas os últimos N sorteios ou None para todos
        """
        self.nome = self.__class__.__name__
        
        # Se não recebeu sorteios, busca do banco de dados
        if sorteios is None:
            query = SorteioLotofacil.objects.all().order_by('-concurso')
            if ultimos_n:
                query = query[:ultimos_n]
            self.sorteios = list(query)
        else:
            self.sorteios = sorteios
        
        self.resultados = {}
        self.df = self._criar_dataframe()
    
    def _criar_dataframe(self):
        """Converte os sorteios em um DataFrame para facilitar a análise"""
        dados = []
        for sorteio in self.sorteios:
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