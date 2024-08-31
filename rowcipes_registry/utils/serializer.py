from rest_framework import serializers
from ..models.user_model import Usuario
from ..models.receita_model import Receita

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['username', 'name','password', 'telefone', 'estado', 'imagem_perfil_url', 'email']
    
    def create(self, validated_data):
        user = Usuario.objects.create_user(
            username=validated_data.get('email'),
            name=validated_data.get('name'),
            password=validated_data.get('password'),
            telefone=validated_data.get('telefone', ''),
            endereco=validated_data.get('endereco', ''),
            imagem_perfil_url=validated_data.get('imagem_perfil_url', ''),
            email=validated_data.get('email','')
        )
        return user

class ReceitaSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True) 

    class Meta:
        model = Receita
        fields = '__all__'
