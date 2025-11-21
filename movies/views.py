import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

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


# ----------------- Lista de Filmes e Séries -----------------

@api_view(['GET'])
def filmes_herois(request):
    page = request.GET.get('page', 1)
    data = tmdb_get('/discover/movie', params={
        'with_genres': '28,12,878',  # Ação, Aventura, Ficção Científica
        'with_keywords': 9715,       # Super-Hero
        'sort_by': 'popularity.desc',
        'page': page
    })
    return Response(data)


@api_view(['GET'])
def series_herois(request):
    page = request.GET.get('page', 1)
    data = tmdb_get('/discover/tv', params={
        'with_genres': '10759,10765',  # Ação + Ficção/Fantasia
        'with_keywords': 9715,
        'sort_by': 'popularity.desc',
        'page': page
    })
    return Response(data)


@api_view(['GET'])
def filmes_marvel(request):
    page = request.GET.get('page', 1)
    data = tmdb_get('/discover/movie', params={
        'with_companies': '420',
        'sort_by': 'popularity.desc',
        'page': page
    })
    return Response(data)


@api_view(['GET'])
def filmes_dc(request):
    page = request.GET.get('page', 1)
    data = tmdb_get('/discover/movie', params={
        'with_keywords': 9717,
        'sort_by': 'popularity.desc',
        'page': page
    })
    return Response(data)


@api_view(['GET'])
def herois_alternativos(request):
    page = request.GET.get('page', 1)
    data = tmdb_get('/discover/movie', params={
        'with_keywords': 9715,
        'sort_by': 'popularity.desc',
        'page': page
    })
    return Response(data)


# ----------------- Detalhes do Item -----------------

@api_view(['GET'])
def detalhe_item(request, tipo, id):
    """
    Retorna detalhes de um item pelo tipo (filmes ou series) e ID.
    """
    try:
        if tipo == "filmes":
            data = tmdb_get(f"/movie/{id}")
        elif tipo == "series":
            data = tmdb_get(f"/tv/{id}")
        else:
            return Response({"error": "Tipo inválido"}, status=400)

        # Mapeia os campos para o frontend
        item = {
            "id": data["id"],
            "titulo": data.get("title") or data.get("name"),
            "descricao": data.get("overview"),
            "capa": f"https://image.tmdb.org/t/p/w500{data.get('poster_path')}" if data.get('poster_path') else None,
            "banner": f"https://image.tmdb.org/t/p/original{data.get('backdrop_path')}" if data.get('backdrop_path') else None,
            "genero": ", ".join([g["name"] for g in data.get("genres", [])]),
            "ano": (data.get("release_date") or data.get("first_air_date") or "")[:4]
        }

        return Response(item)
    except Exception as e:
        return Response({"error": str(e)}, status=404)