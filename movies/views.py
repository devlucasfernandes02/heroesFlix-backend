import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.cache import cache

TMDB_BASE = 'https://api.themoviedb.org/3'

def tmdb_get(path, params=None):
    if params is None:
        params = {}
    params.update({
        'api_key': settings.TMDB_API_KEY,
        'language': 'pt-BR'
    })
    url = f"{TMDB_BASE}{path}"
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


# --------------------------
# Filmes e séries de heróis
# --------------------------

@api_view(['GET'])
def filmes_herois(request):
    """Lista de filmes de Heróis"""
    page = request.GET.get('page', 1)
    cache_key = f"tmdb_hero_movies_page_{page}"
    data = cache.get(cache_key)
    if not data:
        # Palavras-chave usadas separadamente para garantir que o TMDB encontre
        data_marvel = tmdb_get('/discover/movie', params={
            'with_genres': '28,12,878',  # Ação, Aventura, Ficção Científica
            'with_keywords': 15695,       # Marvel
            'sort_by': 'popularity.desc',
            'page': page
        })
        data_dc = tmdb_get('/discover/movie', params={
            'with_genres': '28,12,878',
            'with_keywords': 9717,        # DC
            'sort_by': 'popularity.desc',
            'page': page
        })
        data_hero = tmdb_get('/discover/movie', params={
            'with_genres': '28,12,878',
            'with_keywords': 9715,        # Super-Hero
            'sort_by': 'popularity.desc',
            'page': page
        })

        # Combina os resultados e remove duplicados
        results = {f['id']: f for f in (data_marvel.get('results', []) +
                                        data_dc.get('results', []) +
                                        data_hero.get('results', []))}
        data = {'results': list(results.values())}
        cache.set(cache_key, data, timeout=60*60)
    return Response(data)


@api_view(['GET'])
def series_herois(request):
    """Lista de séries de Heróis"""
    page = request.GET.get('page', 1)
    cache_key = f"tmdb_hero_series_page_{page}"
    data = cache.get(cache_key)
    if not data:
        data_marvel = tmdb_get('/discover/tv', params={
            'with_genres': '10759,10765',  # Ação + Ficção/Fantasia
            'with_keywords': 15695,        # Marvel
            'sort_by': 'popularity.desc',
            'page': page
        })
        data_dc = tmdb_get('/discover/tv', params={
            'with_genres': '10759,10765',
            'with_keywords': 9717,         # DC
            'sort_by': 'popularity.desc',
            'page': page
        })
        data_hero = tmdb_get('/discover/tv', params={
            'with_genres': '10759,10765',
            'with_keywords': 9715,         # Super-Hero
            'sort_by': 'popularity.desc',
            'page': page
        })

        # Combina resultados e remove duplicados
        results = {f['id']: f for f in (data_marvel.get('results', []) +
                                        data_dc.get('results', []) +
                                        data_hero.get('results', []))}
        data = {'results': list(results.values())}
        cache.set(cache_key, data, timeout=60*60)
    return Response(data)


@api_view(['GET'])
def filmes_marvel(request):
    """Filmes da Marvel Studios"""
    cache_key = "tmdb_marvel_movies"
    data = cache.get(cache_key)
    if not data:
        data = tmdb_get('/discover/movie', params={
            'with_companies': '420',  # Marvel Studios
            'sort_by': 'popularity.desc',
            'page': request.GET.get('page', 1)
        })
        cache.set(cache_key, data, timeout=60*60)
    return Response(data)


@api_view(['GET'])
def filmes_dc(request):
    cache_key = "tmdb_dc_movies"
    data = cache.get(cache_key)
    if not data:
        data = tmdb_get('/discover/movie', params={
            'with_keywords': '9717',  # DC Comics
            'sort_by': 'popularity.desc',
            'page': request.GET.get('page', 1)
        })
        cache.set(cache_key, data, timeout=60*60)
    return Response(data)


@api_view(['GET'])
def herois_alternativos(request):
    cache_key = "tmdb_alt_heroes"
    data = cache.get(cache_key)
    if not data:
        data = tmdb_get('/discover/movie', params={
            'with_keywords': '9715',  # Super-heróis alternativos
            'sort_by': 'popularity.desc',
            'page': request.GET.get('page', 1)
        })
        cache.set(cache_key, data, timeout=60*60)
    return Response(data)
