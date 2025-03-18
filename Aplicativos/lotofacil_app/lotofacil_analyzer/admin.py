from django.contrib import admin
from .models import Concurso, JogoGerado

@admin.register(Concurso)
class ConcursoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'data')
    search_fields = ('numero', 'data')

@admin.register(JogoGerado)
class JogoGeradoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'data_geracao')
    search_fields = ('usuario__username', 'data_geracao')
