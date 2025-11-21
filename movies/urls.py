from django.urls import path
from . import views

urlpatterns = [
    path('filmes/herois', views.filmes_herois, name='filmes_herois'),
    path('series/herois', views.series_herois, name='series_herois'),
    path('filmes/marvel', views.filmes_marvel, name='filmes_marvel'),
    path('filmes/dc', views.filmes_dc, name='filmes_dc'),
    path('filmes/herois-alternativos', views.herois_alternativos, name='herois_alternativos'),
    path('item/<str:tipo>/<int:id>/', views.detalhe_item, name='detalhe_item'),
   
]
