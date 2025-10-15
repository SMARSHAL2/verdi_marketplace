from django.urls import path
from . import views

urlpatterns = [
    path('finalizar-compra/', views.finalizar_compra, name='finalizar_compra'),
    path('pedido/<int:pedido_id>/', views.tela_pedido_usuario, name='tela_pedido_usuario'),
    path('historico/', views.historico_pedidos, name='historico_pedidos'),
    path('<int:pedido_id>/', views.tela_pedido_usuario, name='tela_pedido_usuario'),
]
