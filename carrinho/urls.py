# carrinho/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.resumo_carrinho, name='resumo_carrinho'),
    path('resumo-menu/', views.carrinho_resumo_menu, name='carrinho_resumo_menu'),
]
