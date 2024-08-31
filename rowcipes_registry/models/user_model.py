# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    telefone = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    imagem_perfil_url = models.URLField(max_length=255, blank=True, null=True)  # Link para a imagem do perfil

    def to_dict(self):
        return {
            "username": self.email,
            "name":self.name,
            "email": self.email,
            "telefone": self.telefone,
            "estado": self.estado,
            "password": self.password,  
            'email': self.email,
            "imagem_perfil_url":self.imagem_perfil_url          
        }
