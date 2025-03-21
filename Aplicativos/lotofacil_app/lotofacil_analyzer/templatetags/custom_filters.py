from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Retorna o valor de um dicionário para uma chave específica."""
    return dictionary.get(key, '')  # Retorna '' se a chave não existir

@register.filter
def range_filter(value):
    return range(1, value + 1)