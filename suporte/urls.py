from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='painel_suporte'),
    path('cadastrar/', views.cadastro_usuario_form, name='suporte_cadastro_usuario'),
    path('cadastrar/enviar/', views.cadastrar_usuario, name='cadastrar_usuario_suporte'),
    path('desconto-sistema/', views.desconto_sistema, name='desconto_sistema'),
    path('desativar-promocao/<int:promocao_id>/', views.desativar_promocao, name='desativar_promocao'),
    path('editar-promocao/<int:promocao_id>/', views.editar_promocao, name='editar_promocao'),
]
