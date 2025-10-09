import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.cache import cache

# Base da API da TMDB
TMDB_BASE = 'https://api.themoviedb.org/3'

def tmdb_get(path, params=None):
    """Função auxiliar para buscar dados da TMDB"""
    if params is None:
        params = {}
    params.update({
        'api_key': settings.TMDB_API_KEY,
        'language': 'pt-BR'
    })
    url = f"{TMDB_BASE}{path}"
    # O timeout é excelente para evitar que requisições presas congelem seu servidor
    resp = requests.get(url, params=params, timeout=10) 
    resp.raise_for_status() # Lança exceção para 4xx ou 5xx
    return resp.json()

# ------------------------------------------------
# 1. VIEWS JÁ EXISTENTES
# ------------------------------------------------

@api_view(['GET'])
def filmes_populares(request):
    """Lista de filmes populares (Mapeado para /api/filmes/populares)"""
    cache_key = "tmdb_popular_page_1"
    data = cache.get(cache_key)
    if not data:
        data = tmdb_get('/movie/popular', params={'page': 1})
        cache.set(cache_key, data, timeout=60*60)  # 1 hora de cache
    return Response(data)

@api_view(['GET'])
def filme_detalhes(request, tmdb_id: int):
    """Detalhes de um filme específico (Mapeado para /api/filmes/<id>/)"""
    cache_key = f"tmdb_movie_{tmdb_id}"
    data = cache.get(cache_key)
    if not data:
        data = tmdb_get(f'/movie/{tmdb_id}', params={'append_to_response': 'credits,images'})
        cache.set(cache_key, data, timeout=60*60)
    return Response(data)

@api_view(['GET'])
def buscar_filmes(request):
    """Busca de filmes por nome (Mapeado para /api/filmes/search)"""
    q = request.GET.get('query', '')
    if not q:
        return Response({'results': []})
    data = tmdb_get('/search/movie', params={'query': q, 'page': 1, 'include_adult': 'false'})
    return Response(data)

# ------------------------------------------------
# 2. VIEWS IMPLEMENTADAS PARA RESOLVER O ERRO 404 NO FRONTEND
# ------------------------------------------------

@api_view(['GET'])
def filmes_top10(request):
    """Lista de filmes mais bem avaliados (Mapeado para /api/filmes/top10)"""
    cache_key = "tmdb_top_rated_page_1"
    data = cache.get(cache_key)
    if not data:
        # TMDB endpoint para filmes mais bem avaliados
        data = tmdb_get('/movie/top_rated', params={'page': 1}) 
        cache.set(cache_key, data, timeout=60*60)
    return Response(data)

@api_view(['GET'])
def filmes_acao(request):
    """Lista de filmes de Ação (Mapeado para /api/filmes/acao)"""
    cache_key = "tmdb_genre_action"
    data = cache.get(cache_key)
    if not data:
        # Gênero Ação (ID 28 na TMDB)
        data = tmdb_get('/discover/movie', params={
            'with_genres': 28, 
            'sort_by': 'popularity.desc'
        })
        cache.set(cache_key, data, timeout=60*60)
    return Response(data)

# Opcional: Para 'Séries Originais HeroesFlix' se você usou o endpoint /api/series/originais
# @api_view(['GET'])
# def series_originais(request):
#     """Lista de Séries mais populares"""
#     cache_key = "tmdb_series_popular"
#     data = cache.get(cache_key)
#     if not data:
#         # TMDB endpoint para séries populares
#         data = tmdb_get('/tv/popular', params={'page': 1}) 
#         cache.set(cache_key, data, timeout=60*60)
#     return Response(data)