from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from ..models.user_model import Usuario
from ..utils.serializer import UsuarioSerializer
from rest_framework.permissions import AllowAny
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    user_data = request.data.get('user', {})
    user_serializer = UsuarioSerializer(data=user_data)
    if user_serializer.is_valid():
        if Usuario.objects.filter(email=user_data.get('email')).exists():
            return Response({'error': 'Um usuário com esse e-mail já existe.'}, status=status.HTTP_400_BAD_REQUEST)
        user = user_serializer.save()
        return Response(user_serializer.data, status=status.HTTP_201_CREATED)

    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_user(request):
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({'error': 'Authorization header not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        token_str = auth_header.split()[1]
        
        data = {'token': token_str}
        valid_data = VerifyJSONWebTokenSerializer().validate(data)
        user = valid_data['user']
        
        serializer = UsuarioSerializer(user)
        user_data = serializer.data
        
        return Response(user_data, status=status.HTTP_200_OK)
    
    except Usuario.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
