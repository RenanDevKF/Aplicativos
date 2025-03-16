from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Rota para a view home
    path('criar_jogo/', views.criar_jogo, name='criar_jogo'),
    path('gerar-jogo-rapido/', views.gerar_jogo_rapido, name='gerar_jogo_rapido'),
    path('resultados/', views.resultados, name='resultados'),
]

