"""mercadapp_intmed_challenge URL Configuration"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from core import views

router = routers.DefaultRouter()
router.register(r'market', views.MarketViewSet)
router.register(r'cart', views.CartViewSet, base_name='cart')

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]
