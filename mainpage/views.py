from django.shortcuts import render
from produtos.models import Produto

def home(request):
    return render(request, 'mainpage/home.html')

def buscar(request):
    return render(request, 'mainpage/buscar_resultados.html', {})

def home(request):
    produtos = Produto.objects.select_related('categoria', 'vendedor').order_by('-criado_em')
    return render(request, 'mainpage/home.html', {'produtos': produtos})