import json
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from .models import User


def home(request):
    return JsonResponse({
        "status": "OK",
        "service": "HeroesFlix API running",
        "endpoints": {
            "/users/": "GET lista usuários | POST cria usuário",
            "/login/": "Info da rota de login",
            "/login/create/": "POST valida login"
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

        # validações
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
    return JsonResponse({
        "message": "Use POST em /login/create/",
        # "example": {
        #     "email": "email@exemplo.com",
        #     "password": "123"
        # }
    })


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
