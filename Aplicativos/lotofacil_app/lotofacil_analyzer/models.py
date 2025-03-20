from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import json

class SorteioLotofacil(models.Model):
    """Armazena resultados dos sorteios da Lotofácil."""
    concurso = models.IntegerField(unique=True)  # Número do concurso
    data = models.DateField()  # Data do sorteio
    numeros = models.CharField(max_length=50)  # Números sorteados (ex: "1,2,3,4,...")
    ganhadores_15_acertos = models.IntegerField(default=0)  # Ganhadores com 15 acertos

    def get_numeros_list(self):
        """Retorna os números como lista de inteiros."""
        return [int(n) for n in self.numeros.split(',')]

    def clean(self):
        """Valida os números sorteados."""
        numeros = self.get_numeros_list()
        if len(numeros) != 15:
            raise ValidationError("O concurso deve ter exatamente 15 números.")
        if any(n < 1 or n > 25 for n in numeros):
            raise ValidationError("Os números devem estar entre 1 e 25.")

    def __str__(self):
        return f"Concurso {self.concurso} - {self.data}"

    class Meta:
        ordering = ['-concurso']
        verbose_name = 'Sorteio Lotofácil'
        verbose_name_plural = 'Sorteios Lotofácil'
        
        
from django.db import models
import json

class AnaliseEstatistica(models.Model):
    """Armazena os resultados das análises estatísticas."""
    TIPO_ANALISE_CHOICES = [
        ('frequencia', 'Frequência de Números'),
        ('atraso', 'Atraso de Números'),
        ('combinacoes', 'Combinações Mais Comuns'),
        ('distribuicao', 'Distribuição de Números'),
        ('outro', 'Outro'),
    ]

    tipo = models.CharField(max_length=50, choices=TIPO_ANALISE_CHOICES)  # Tipo de análise
    data_analise = models.DateTimeField(auto_now_add=True)  # Data da análise
    parametros = models.JSONField(null=True, blank=True)  # Parâmetros usados na análise
    resultados = models.JSONField()  # Resultados da análise

    def get_resultados_formatados(self):
        """Retorna os resultados formatados para exibição."""
        return json.dumps(self.resultados, indent=4)

    def __str__(self):
        return f"Análise de {self.get_tipo_display()} - {self.data_analise}"

    class Meta:
        ordering = ['-data_analise']
        verbose_name = 'Análise Estatística'
        verbose_name_plural = 'Análises Estatísticas'

class ApostaGerada(models.Model):
    """Armazena apostas geradas para os usuários."""
    METODO_GERACAO_CHOICES = [
        ('frequencia', 'Frequência de Números'),
        ('combinado', 'Combinação Estatística'),
        ('aleatorio', 'Aleatório'),
        ('outro', 'Outro'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='apostas_geradas')
    data_geracao = models.DateTimeField(auto_now_add=True)
    numeros = models.CharField(max_length=50)  # "1,2,3,4,..."
    metodo_geracao = models.CharField(max_length=50, choices=METODO_GERACAO_CHOICES)
    parametros = models.JSONField(null=True, blank=True)  # Parâmetros usados para gerar

    def get_numeros_list(self):
        """Retorna os números como lista de inteiros."""
        return [int(n) for n in self.numeros.split(',')]

    def clean(self):
        """Valida os números da aposta."""
        numeros = self.get_numeros_list()
        if len(numeros) != 15:
            raise ValidationError("A aposta deve ter exatamente 15 números.")
        if any(n < 1 or n > 25 for n in numeros):
            raise ValidationError("Os números devem estar entre 1 e 25.")

    def __str__(self):
        return f"Aposta para {self.usuario.username} - {self.data_geracao}"

    class Meta:
        ordering = ['-data_geracao']
        verbose_name = 'Aposta Gerada'
        verbose_name_plural = 'Apostas Geradas'

