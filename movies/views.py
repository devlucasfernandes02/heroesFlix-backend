import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.cache import cache
import time

TMDB_BASE = 'https://api.themoviedb.org/3'
LOCK_TIMEOUT = 10 

def tmdb_get(path, params=None):
    if params is None:
        params = {}
    params.update({
        'api_key': settings.TMDB_API_KEY,
        'language': 'pt-BR'
    })
    url = f"{TMDB_BASE}{path}"
    resp = requests.get(url, params=params, timeout=15) 
    resp.raise_for_status()
    return resp.json()


def fetch_and_cache(cache_key, lock_key, fetch_function, timeout_seconds=60*60):
    data = cache.get(cache_key)
    if not data:
        if cache.add(lock_key, True, LOCK_TIMEOUT):
            try:
                data = fetch_function()
                cache.set(cache_key, data, timeout=timeout_seconds)
            finally:
                cache.delete(lock_key)
        else:
            time.sleep(1) 
            data = cache.get(cache_key) 
            if not data:
                return Response({"message": "Cache em reconstrução, tente novamente em breve."}, status=503)
    return Response(data)


@api_view(['GET'])
def filmes_herois(request):
    page = request.GET.get('page', 1)
    cache_key = f"tmdb_hero_movies_page_{page}"
    lock_key = f"{cache_key}_lock"
    
    def fetch():
        data_marvel = tmdb_get('/discover/movie', params={
            'with_genres': '28,12,878',
            'with_keywords': 15695,      
            'sort_by': 'popularity.desc',
            'page': page
        })
        data_dc = tmdb_get('/discover/movie', params={
            'with_genres': '28,12,878',
            'with_keywords': 9717,        
            'sort_by': 'popularity.desc',
            'page': page
        })
        data_hero = tmdb_get('/discover/movie', params={
            'with_genres': '28,12,878',
            'with_keywords': 9715,        
            'sort_by': 'popularity.desc',
            'page': page
        })

        results = {f['id']: f for f in (data_marvel.get('results', []) +
                                        data_dc.get('results', []) +
                                        data_hero.get('results', []))}
        return {'results': list(results.values())}

    return fetch_and_cache(cache_key, lock_key, fetch)


@api_view(['GET'])
def series_herois(request):
    page = request.GET.get('page', 1)
    cache_key = f"tmdb_hero_series_page_{page}"
    lock_key = f"{cache_key}_lock"
    
    def fetch():
        data_marvel = tmdb_get('/discover/tv', params={
            'with_genres': '10759,10765',
            'with_keywords': 15695,       
            'sort_by': 'popularity.desc',
            'page': page
        })
        data_dc = tmdb_get('/discover/tv', params={
            'with_genres': '10759,10765',
            'with_keywords': 9717,        
            'sort_by': 'popularity.desc',
            'page': page
        })
        data_hero = tmdb_get('/discover/tv', params={
            'with_genres': '10759,10765',
            'with_keywords': 9715,        
            'sort_by': 'popularity.desc',
            'page': page
        })

        results = {f['id']: f for f in (data_marvel.get('results', []) +
                                        data_dc.get('results', []) +
                                        data_hero.get('results', []))}
        return {'results': list(results.values())}

    return fetch_and_cache(cache_key, lock_key, fetch)


@api_view(['GET'])
def filmes_marvel(request):
    page = request.GET.get('page', 1)
    cache_key = "tmdb_marvel_movies"
    lock_key = f"{cache_key}_lock"
    
    def fetch():
        return tmdb_get('/discover/movie', params={
            'with_companies': '420',
            'sort_by': 'popularity.desc',
            'page': page
        })
        
    return fetch_and_cache(cache_key, lock_key, fetch)


@api_view(['GET'])
def filmes_dc(request):
    page = request.GET.get('page', 1)
    cache_key = "tmdb_dc_movies"
    lock_key = f"{cache_key}_lock"
    
    def fetch():
        return tmdb_get('/discover/movie', params={
            'with_keywords': '9717',
            'sort_by': 'popularity.desc',
            'page': page
        })

    return fetch_and_cache(cache_key, lock_key, fetch)


@api_view(['GET'])
def herois_alternativos(request):
    page = request.GET.get('page', 1)
    cache_key = "tmdb_alt_heroes"
    lock_key = f"{cache_key}_lock"
    
    def fetch():
        return tmdb_get('/discover/movie', params={
            'with_keywords': '9715',
            'sort_by': 'popularity.desc',
            'page': page
        })

    return fetch_and_cache(cache_key, lock_key, fetch)


@api_view(['GET'])
def detalhe_item(request, tipo, id):
    if tipo == 'filmes':
        tmdb_path = f'/movie/{id}'
    elif tipo == 'series':
        tmdb_path = f'/tv/{id}'
    else:
        return Response({"error": "Tipo de conteúdo inválido."}, status=400)

    cache_key = f"tmdb_detail_{tipo}_{id}"
    lock_key = f"{cache_key}_lock"
    
    def fetch():
        data = tmdb_get(tmdb_path)
        data['link_detalhes'] = f"/item/{tipo}/{id}"
        data['link_assistir'] = f"/assistir/{tipo}/{id}"
        return data

    return fetch_and_cache(cache_key, lock_key, fetch, timeout_seconds=60*60*24)