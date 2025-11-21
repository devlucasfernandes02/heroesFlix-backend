from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from .models import User

def home(request):
    return render(request, 'users/home.html')

def user(request):
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        # validações mínimas
        if not email or not password:
            messages.error(request, "Email e senha são obrigatórios.")
            return redirect('login_user')

        # verifica duplicação antes de criar
        if User.objects.filter(email=email).exists():
            messages.error(request, "Usuário já cadastrado. Faça login.")
            return redirect('login_user')

        # cria usuário (simples, sem hashing)
        User.objects.create(name=name, email=email, password=password)
        messages.success(request, "Usuário cadastrado com sucesso! Faça login.")
        return redirect('login_user')

    # GET -> listar
    users = User.objects.all()
    return render(request, 'users/users.html', {'users': users})


# Login: valida email+senha e redireciona
def login_create(request):
    if request.method != "POST":
        raise Http404()

    email = request.POST.get('email', '').strip()
    password = request.POST.get('password', '')

    if not email or not password:
        messages.error(request, "Preencha email e senha.")
        return redirect('login_user')

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        messages.error(request, "Usuário ou senha incorreta.")
        return redirect('login_user')

    if user.password != password:
        messages.error(request, "Usuário ou senha incorreta.")
        return redirect('login_user')

    request.session['user_email'] = user.email
    messages.success(request, "Login realizado com sucesso!")
    return redirect('list_users')


# Template de login
def login_user(request):
    return render(request, 'users/login.html')
