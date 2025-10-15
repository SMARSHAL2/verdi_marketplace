from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from collections import defaultdict

from produtos.models import ItemCarrinho, Produto
from .models import Pedido, ItemPedido


# views.py
def tela_pedido_usuario(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id, cliente=request.user)
    total_final = sum(item.produto.preco * item.quantidade for item in pedido.itens.all())
    return render(request, 'pedido_usuario.html', {
        'pedido': pedido,
        'itens': pedido.itens.all(),
        'total_final': total_final
    })

@login_required
def concluir_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.user != pedido.itens.first().produto.vendedor:
        return redirect('home')  # só o vendedor pode concluir
    pedido.status = 'concluido'
    pedido.save()
    return redirect('detalhe_pedido', pedido_id=pedido.id)

@login_required
def historico_pedidos(request):
    pedidos = Pedido.objects.filter(cliente=request.user).order_by('-id')
    return render(request, 'historico.html', {'pedidos': pedidos})

@login_required
def detalhe_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, cliente=request.user)
    return render(request, 'pedidos/detalhe_pedido.html', {'pedido': pedido})

def finalizar_compra(request):
    itens_carrinho = ItemCarrinho.objects.filter(usuario=request.user)
    if not itens_carrinho.exists():
        return redirect('carrinho')  # carrinho vazio

    # Criar pedido
    pedido = Pedido.objects.create(cliente=request.user, finalizado=True)

    # Criar itens do pedido
    for item in itens_carrinho:
        ItemPedido.objects.create(
            pedido=pedido,
            produto=item.produto,
            quantidade=item.quantidade
        )

    # 🔹 Inicializar o defaultdict
    pedidos_por_produtor = defaultdict(list)

    # Separar itens por vendedor
    for item in pedido.itens.all():
        pedidos_por_produtor[item.produto.vendedor].append(item)

    # Enviar alertas por vendedor
    for vendedor, itens in pedidos_por_produtor.items():
        mensagem = "Você recebeu um novo pedido:\n"
        for item in itens:
            mensagem += f"{item.produto.nome} x {item.quantidade}\n"

        send_mail(
            'Novo pedido',
            mensagem,
            'no-reply@marketplace.com',
            [vendedor.email],  # vendedor é um objeto Usuario
            fail_silently=False,
        )

    # Limpar carrinho no banco
    itens_carrinho.delete()

    return redirect('tela_pedido_usuario', pedido_id=pedido.id)
