from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProdutoForm
from .models import Categoria

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

