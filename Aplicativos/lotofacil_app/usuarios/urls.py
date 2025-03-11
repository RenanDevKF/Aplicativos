from django.urls import path
from .views import registrar_usuario, login_usuario, logout_usuario, historico_jogos

urlpatterns = [
    path("registro/", registrar_usuario, name="registro"),
    path("login/", login_usuario, name="login"),
    path("logout/", logout_usuario, name="logout"),
    path("historico/", historico_jogos, name="historico"),
]
