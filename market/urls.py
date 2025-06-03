from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from mainpage import views as mainpage_views
from produtos import views
from market import views as market_views


from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', mainpage_views.home, name='home'),
    path('accounts/', include('usuarios.urls')),
    path('suporte/', include('suporte.urls')),
    path('produtos/', include('produtos.urls')),
    path('carrinho/', include('carrinho.urls')),
    path('buscar/', mainpage_views.buscar, name='buscar'),
    path('carrinho/', market_views.carrinho_view, name='carrinho'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
