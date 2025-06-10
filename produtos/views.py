from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProdutoForm
from .models import Categoria
from .models import Produto
from django.db.models import Avg
from .models import Avaliacao
from .forms import AvaliacaoForm
from django.contrib import messages

@login_required
def anunciar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            produto = form.save(commit=False)
            produto.vendedor = request.user
            produto.save()
            return redirect('home')
    else:
        form = ProdutoForm()

    categorias = Categoria.objects.all()  # 🔹 Isso que envia as categorias
    return render(request, 'produtos/anunciar.html', {
        'form': form,
        'categorias': categorias
    })

def produto_detalhe(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    relacionados = Produto.objects.filter(categoria=produto.categoria).exclude(id=produto.id)[:4]
    avaliacoes = produto.avaliacoes.select_related('usuario').order_by('-criado_em')
    media_nota = avaliacoes.aggregate(media=Avg('nota'))['media'] or 0
    outros_produtos = Produto.objects.exclude(categoria=produto.categoria).exclude(id=produto.id)[:4]


    # Processamento do formulário
    if request.method == 'POST' and 'avaliar' in request.POST:
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.produto = produto
            avaliacao.usuario = request.user
            avaliacao.save()
            messages.success(request, "Avaliação enviada com sucesso!")
            return redirect('produto_detalhe', produto_id=produto.id)
    else:
        form = AvaliacaoForm()

    return render(request, 'produtos/produto_detalhe.html', {
        'produto': produto,
        'relacionados': relacionados,
        'form_avaliacao': form,
        'avaliacoes': avaliacoes,
        'media_nota': media_nota,
        'outros_produtos': outros_produtos,
    })

