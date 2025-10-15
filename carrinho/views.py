from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from produtos.models import ItemCarrinho, Produto

@login_required
def carrinho_resumo_menu(request):
    itens = ItemCarrinho.objects.filter(usuario=request.user)
    total_final = sum(item.total_com_desconto() for item in itens)  # soma com desconto do produtor

    context = {
        'itens': itens,
        'total_final': total_final,
    }

    html = render_to_string('carrinho/resumo_menu.html', context, request=request)
    return JsonResponse({'html': html})

from decimal import Decimal

@login_required
def resumo_carrinho(request):
    itens = ItemCarrinho.objects.filter(usuario=request.user)

    # total sem desconto (preço original * qtd)
    total_bruto = sum(item.produto.preco * item.quantidade for item in itens)

    # total com desconto — garante que o retorno seja Decimal
    total_com_desconto = sum(
        Decimal(item.produto.preco_com_desconto()) * item.quantidade for item in itens
    )

    # economia
    economia = total_bruto - total_com_desconto

    context = {
        'itens': itens,
        'total_bruto': total_bruto,
        'total_com_desconto': total_com_desconto,
        'economia': economia,
    }
    return render(request, 'carrinho/resumo_menu.html', context)

@login_required
def adicionar_ao_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    quantidade = int(request.POST.get('quantidade', 1))

    item, criado = ItemCarrinho.objects.get_or_create(
        usuario=request.user,
        produto=produto,
        defaults={'quantidade': quantidade}
    )
    if not criado:
        item.quantidade += quantidade
        item.save()

    return redirect('home')
