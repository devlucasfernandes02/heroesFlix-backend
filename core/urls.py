from django.contrib import admin
from django.urls import path, include
from users import views
from django.http import JsonResponse

def home(request):
    return JsonResponse({"status": "OK", "service": "HeroesFlix API running"})

urlpatterns = [
    path("", home),  # <--- adicionada
    path('admin/', admin.site.urls),
    path('api/', include('movies.urls')), 
    path('users/', views.user, name='list_users'),       
    path('login/', views.login_user, name='login_user'),
    path('login/create/', views.login_create, name='login_create'),
]
