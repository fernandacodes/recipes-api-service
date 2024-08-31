from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core.files.storage import default_storage
import json
from ..models.receita_model import Receita
from ..models.user_model import Usuario
from ..utils.serializer import ReceitaSerializer
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer

@api_view(['POST'])
def create_receita(request):
    if request.method == 'POST':
        try:
            # Verifica se o usuário está autenticado
            if not request.user.is_authenticated:
                return Response({"error": "Usuário não autenticado."}, status=status.HTTP_403_FORBIDDEN)

            if 'imagem' not in request.FILES:
                return Response({"error": "Imagem não fornecida."}, status=status.HTTP_400_BAD_REQUEST)
            
            imagem = request.FILES['imagem']
            nome = request.POST.get('nome')
            ingredientes = request.POST.get('ingredientes')
            instrucoes = request.POST.get('instrucoes')
            tempo_preparo = request.POST.get('tempo_preparo')
            porcoes = request.POST.get('porcoes')

            imagem_path = default_storage.save('imagens_receitas/' + imagem.name, imagem)
            imagem_url = default_storage.url(imagem_path)

            receita = Receita.objects.create(
                nome=nome,
                ingredientes=ingredientes,
                instrucoes=instrucoes,
                tempo_preparo=tempo_preparo,
                porcoes=porcoes,
                imagem=imagem_url,
                usuario=request.user  # Associa a receita ao usuário atual
            )

            return Response({"message": "Receita criada com sucesso."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "Método não permitido."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['GET'])
def get_all_receitas(request):
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({'error': 'Authorization header not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        token_str = auth_header.split()[1]
        
        # Decodifica o token
        data = {'token': token_str}
        valid_data = VerifyJSONWebTokenSerializer().validate(data)
        user = valid_data['user']

        receitas = Receita.objects.all()
        receitas_list = [ReceitaSerializer(receita).data for receita in receitas]
        return Response({"receitas": receitas_list}, status=status.HTTP_200_OK)

    except Exception as e:
        # Retorna erro se o token não for válido ou se houver qualquer outro erro
        return Response({'error': 'Invalid token or other error'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def get_receita_by_id(request, receita_id):
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({'error': 'Authorization header not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        token_str = auth_header.split()[1]
        
        data = {'token': token_str}
        valid_data = VerifyJSONWebTokenSerializer().validate(data)
        user = valid_data['user']

        receita = Receita.objects.get(id=receita_id)
        return Response(ReceitaSerializer(receita).data, status=status.HTTP_200_OK)
    
    except Receita.DoesNotExist:
        return Response({"error": f"Receita com ID {receita_id} não encontrada."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def update_receita(request, receita_id):
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({'error': 'Authorization header not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        token_str = auth_header.split()[1]
        
        data = {'token': token_str}
        valid_data = VerifyJSONWebTokenSerializer().validate(data)
        user = valid_data['user']

        receita = Receita.objects.get(id=receita_id)
        
        if receita.usuario != user:
            return Response({"error": "Você não tem permissão para atualizar esta receita."}, status=status.HTTP_403_FORBIDDEN)
        
        data = json.loads(request.body.decode('utf-8'))
        
        for key, value in data.items():
            if key == 'imagem' and isinstance(value, str):  # Se for uma URL, não atualize o campo da imagem
                continue
            setattr(receita, key, value)
        
        receita.save()
        return Response({"message": f"Receita com ID {receita_id} atualizada com sucesso."})
    
    except Receita.DoesNotExist:
        return Response({"error": f"Receita com ID {receita_id} não encontrada."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def search_receitas_by_name(request):
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({'error': 'Authorization header not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        token_str = auth_header.split()[1]
        
        data = {'token': token_str}
        valid_data = VerifyJSONWebTokenSerializer().validate(data)
        user = valid_data['user']

        nome = request.GET.get('nome', None)
        if not nome:
            return Response({"error": "Nenhum nome fornecido."}, status=status.HTTP_400_BAD_REQUEST)

        receitas = Receita.objects.filter(nome__icontains=nome)
        receitas_list = [ReceitaSerializer(receita).data for receita in receitas]
        return Response({"receitas": receitas_list}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_receitas_by_user(request, user_id):
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({'error': 'Authorization header not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        token_str = auth_header.split()[1]
        
        data = {'token': token_str}
        valid_data = VerifyJSONWebTokenSerializer().validate(data)
        user = valid_data['user']

        receitas = Receita.objects.filter(usuario_id=user_id)
        receitas_list = [ReceitaSerializer(receita).data for receita in receitas]
        return Response({"receitas": receitas_list}, status=status.HTTP_200_OK)
    
    except Usuario.DoesNotExist:
        return Response({"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

