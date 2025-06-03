from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import render
from produtos.models import ItemCarrinho
from django.conf import settings

@login_required
def carrinho_resumo_menu(request):
    desconto_sistema = settings.DESCONTO_GERAL_SISTEMA
    itens = ItemCarrinho.objects.filter(usuario=request.user)
    total_final = sum(item.total_item(desconto_sistema) for item in itens)

    context = {
        'itens': itens,
        'total_final': total_final,
        'desconto_sistema': desconto_sistema,
    }

    html = render_to_string('carrinho/resumo_menu.html', context, request=request)
    return JsonResponse({'html': html})

@login_required
def resumo_carrinho(request):
    desconto_sistema = get_desconto_sistema()
    itens = ItemCarrinho.objects.filter(usuario=request.user)

    total_bruto = sum(item.produto.preco * item.quantidade for item in itens)
    total_com_desconto = sum(item.total_item(desconto_sistema) for item in itens)
    economia = total_bruto - total_com_desconto

    context = {
        'itens': itens,
        'total_bruto': total_bruto,
        'total_com_desconto': total_com_desconto,
        'economia': economia,
        'desconto_sistema': desconto_sistema,
    }
    return render(request, 'carrinho/resumo_carrinho.html', context)