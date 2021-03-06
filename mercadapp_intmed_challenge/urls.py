from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from core import views

router = routers.DefaultRouter()
router.register(r'markets', views.MarketViewSet, base_name='markets')
router.register(r'carts', views.CartViewSet, base_name='carts')
router.register(r'orders', views.OrderViewSet, base_name='orders')

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]
