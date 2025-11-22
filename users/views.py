import json
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, Profile
from .serializers import ProfileSerializer


def home(request):
    return JsonResponse({
        "status": "OK",
        "service": "HeroesFlix API running",
        "endpoints": {
            "/users/": "GET lista usuários | POST cria usuário",
            "/login/": "Info da rota de login",
            "/login/create/": "POST valida login",
            "/users/<id>/profiles": "GET lista | POST cria perfil",
            "/users/<id>/profiles/<pid>": "DELETE exclui perfil",
        }
    })


@csrf_exempt
def users(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except:
            return JsonResponse({"error": "JSON inválido"}, status=400)

        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        password = data.get("password", "")
        confirm = data.get("confirm_password", "")

        if not email:
            return JsonResponse({"error": "Email é obrigatório."}, status=400)
        if not password:
            return JsonResponse({"error": "Senha é obrigatória."}, status=400)
        if len(password) < 6:
            return JsonResponse({"error": "A senha deve ter no mínimo 6 caracteres."}, status=400)
        if password != confirm:
            return JsonResponse({"error": "As senhas não coincidem."}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Usuário já cadastrado."}, status=409)

        user = User.objects.create(name=name, email=email, password=password)

        return JsonResponse({
            "message": "Usuário criado",
            "user": {
                "id": user.id_users,
                "name": user.name,
                "email": user.email
            }
        }, status=201)

    lista = list(User.objects.values("id_users", "name", "email"))
    return JsonResponse(lista, safe=False)


def login_user(request):
    return JsonResponse({"message": "Use POST em /login/create/"})


@csrf_exempt
def login_create(request):
    if request.method != "POST":
        raise Http404()

    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    email = data.get("email", "").strip()
    password = data.get("password", "")

    if not email or not password:
        return JsonResponse({"error": "Preencha email e senha."}, status=400)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({"error": "Usuário ou senha incorreta."}, status=401)

    if user.password != password:
        return JsonResponse({"error": "Usuário ou senha incorreta."}, status=401)

    return JsonResponse({
        "message": "Login OK",
        "user": {
            "id": user.id_users,
            "name": user.name,
            "email": user.email
        }
    })


@api_view(['GET', 'POST'])
def profiles(request, user_id):
    try:
        user = User.objects.get(id_users=user_id)
    except User.DoesNotExist:
        return Response({"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        profiles = Profile.objects.filter(user=user)
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        data = request.data.copy()
        data['user'] = user.id_users 
        
        serializer = ProfileSerializer(data=data)
        if serializer.is_valid():
            profile = serializer.save(user=user)
            return Response(ProfileSerializer(profile).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@csrf_exempt
def profile_detail(request, user_id, profile_id):
    try:
        profile = Profile.objects.get(user__id_users=user_id, id=profile_id)
    except Profile.DoesNotExist:
        return Response({"error": "Perfil não encontrado para este usuário."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)