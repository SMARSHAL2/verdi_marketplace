from django.shortcuts import render

def carrinho_view(request):
    return render(request, 'market/carrinho.html')
