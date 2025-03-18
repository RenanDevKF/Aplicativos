from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Concurso(models.Model):
    numero = models.IntegerField(unique=True)  # Número do concurso
    data = models.DateField()
    numeros_sorteados = models.JSONField()  # Lista de números sorteados

    def __str__(self):
        return f"Concurso {self.numero} - {self.data}"
    
    def save(self, *args, **kwargs):
        if len(self.numeros_sorteados) != 15:
            raise ValidationError("O concurso deve ter exatamente 15 números sorteados.")
        super().save(*args, **kwargs)

class JogoGerado(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    numeros = models.JSONField()  # Lista de números sugeridos
    data_geracao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Jogo de {self.usuario.username if self.usuario else 'Anônimo'} - {self.data_geracao}"

