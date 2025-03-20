# lotofacil_analyzer/generators/base.py
from abc import ABC, abstractmethod
from ..models import ApostaGerada

class GeradorBase(ABC):
    """Classe base para geradores de apostas"""
    
    def __init__(self, analisadores=None, usuario=None):
        """
        Inicializa o gerador
        
        Args:
            analisadores (dict): Dicionário com resultados de analisadores
            usuario (User): Usuário para quem gerar as apostas
        """
        self.analisadores = analisadores or {}
        self.usuario = usuario
        self.nome = self.__class__.__name__
    
    @abstractmethod
    def gerar(self, quantidade=1, salvar=True):
        """
        Gera apostas baseadas nas análises
        
        Args:
            quantidade (int): Número de jogos a gerar
            salvar (bool): Se True, salva as apostas no banco de dados
            
        Returns:
            list: Lista de apostas geradas (cada aposta é uma lista de 15 números)
        """
        pass
    
    def salvar_aposta(self, numeros):
        """
        Salva uma aposta gerada no banco de dados
        
        Args:
            numeros (list): Lista de 15 números da aposta
            
        Returns:
            ApostaGerada: Objeto da aposta salva
        """
        if not self.usuario:
            raise ValueError("É necessário um usuário para salvar apostas")
        
        numeros_str = ','.join(map(str, sorted(numeros)))
        
        aposta = ApostaGerada(
            usuario=self.usuario,
            numeros=numeros_str,
            metodo_geracao=self.nome
        )
        aposta.save()
        return aposta