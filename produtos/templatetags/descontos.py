from django import template

register = template.Library()

@register.filter
def percentual_desconto(preco_original, preco_final):
    try:
        if preco_original == 0:
            return 0
        return round((preco_original - preco_final) / preco_original * 100, 2)
    except:
        return 0
