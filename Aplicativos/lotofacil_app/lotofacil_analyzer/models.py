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

class JogoGerado(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    numeros = models.JSONField()  # Lista de números sugeridos
    data_geracao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Jogo de {self.usuario.username if self.usuario else 'Anônimo'} - {self.data_geracao}"

