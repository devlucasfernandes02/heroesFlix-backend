from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt  # só para desenvolvimento rápido; veja observações abaixo
def login_view(request):
    """
    POST { "email": "...", "password": "..." }
    """
    data = request.data
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return Response({'detail': 'Email e senha são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        return Response({'detail': 'Credenciais inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)

    # o authenticate espera username, então usamos username do user
    user_auth = authenticate(request, username=user.username, password=password)
    if user_auth is None:
        return Response({'detail': 'Credenciais inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)

    # cria a sessão
    login(request, user_auth)

    # retorna dados do usuário (sem senha)
    user_data = {
        'id': user_auth.id,
        'username': user_auth.username,
        'email': user_auth.email,
        'first_name': user_auth.first_name,
        'last_name': user_auth.last_name,
    }
    return Response({'access': True, 'user': user_data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({'detail': 'Logout ok'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def whoami(request):
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    })
