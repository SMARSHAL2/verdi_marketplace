from django.urls import path
from . import views

urlpatterns = [
    path('anunciar/', views.anunciar_produto, name='anunciar_produto'),
    path('produto/<int:produto_id>/', views.produto_detalhe, name='produto_detalhe'),
]
