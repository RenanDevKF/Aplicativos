from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Retorna o valor de um dicionário para uma chave específica."""
    if isinstance(dictionary, dict):  # Verifica se é um dicionário
        return dictionary.get(key, '')  # Retorna '' se a chave não existir
    return ''  # Retorna uma string vazia caso não seja um dicionário

@register.filter
def range_filter(value):
    return range(1, value + 1)