from django.db import models
from django.conf import settings

class Receita(models.Model):
    nome = models.CharField(max_length=255)
    ingredientes = models.TextField()
    instrucoes = models.TextField()
    tempo_preparo = models.IntegerField()
    porcoes = models.IntegerField()
    imagem = models.URLField(max_length=200)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receitas')

    def __str__(self):
        return self.nome

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "ingredientes": self.ingredientes,
            "instrucoes": self.instrucoes,
            "tempo_preparo": self.tempo_preparo,
            "porcoes": self.porcoes,
            "imagem": self.imagem,
            "usuario": self.usuario.name
        }
