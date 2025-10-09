# movies/urls.py (Corrigido)
from django.urls import path
from . import views

urlpatterns = [
    # REMOVA o '/api/' daqui. Comece o path com 'filmes/...'.
    # O path completo será agora: 'api/' + 'filmes/populares'
    path('filmes/populares', views.filmes_populares, name='filmes_populares'),
    path('filmes/top10', views.filmes_top10, name='filmes_top10'),
    path('filmes/acao', views.filmes_acao, name='filmes_acao'),
    
    # Adicione a rota 'continue-watching' (view não implementada, mas corrigida a URL)
    # path('filmes/continue-watching', views.filmes_continue_watching, name='filmes_continue_watching'),
    
    # Detalhes
    path('filmes/<int:tmdb_id>/', views.filme_detalhes, name='filme_detalhes'),
]