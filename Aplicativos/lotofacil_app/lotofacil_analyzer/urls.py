from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Rota para a view home
    path('criar_jogo/', views.criar_jogo, name='criar_jogo'),
    path('gerar-jogo-rapido/', views.gerar_jogo_rapido, name='gerar_jogo_rapido'),
    path('resultados/', views.resultados, name='resultados'),
    path('estatisticas/', views.estatisticas, name='estatisticas'),
    path('planos/', views.planos, name='planos'),
    path('newsletter/', views.newsletter_signup, name='newsletter_signup'),
]

