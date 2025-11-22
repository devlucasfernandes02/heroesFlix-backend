from django.contrib import admin
from django.urls import path, include
from users import views

urlpatterns = [
    path("", views.home),
    path('admin/', admin.site.urls),
    path('api/', include('movies.urls')),
    path('users/', views.users),
    path('login/', views.login_user),
    path('login/create/', views.login_create),
]
