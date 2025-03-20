from django.contrib import admin
from .models import SorteioLotofacil, ApostaGerada

@admin.register(SorteioLotofacil)
class SorteioLotofacilAdmin(admin.ModelAdmin):
    list_display = ('numeros', 'data')
    search_fields = ('numeros', 'data')
    

@admin.register(ApostaGerada)
class ApostaGeradaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'data_geracao')
    search_fields = ('usuario__username', 'data_geracao')
    list_filter = ('data_geracao', 'usuario')
    ordering = ('-data_geracao',)  # Ordena por data de geração (mais recente primeiro)
