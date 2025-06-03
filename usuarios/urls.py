from django.urls import path
from usuarios import views as usuarios_views
from . import views
from .views import logout_view

urlpatterns = [
    # Autenticação
    path('login/', usuarios_views.login_view, name='login'),
    path('logout/', usuarios_views.logout_view, name='logout'),
    path('register/', usuarios_views.register_view, name='register'),
    path('cadastrar-produtor/', usuarios_views.register_produtor_view, name='register_produtor'),

    # Perfil e Endereços
    path('perfil/', views.perfil_view, name='perfil'),
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
    path('endereco/<int:endereco_id>/editar/', views.editar_endereco, name='editar_endereco'),
    path('endereco/novo/', views.adicionar_endereco, name='adicionar_endereco'),
    path('endereco/<int:endereco_id>/principal/', views.tornar_endereco_principal, name='tornar_endereco_principal'),
]
