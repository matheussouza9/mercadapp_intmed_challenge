from django.contrib import admin
from .models import Market, Item, Cart, Order


class MarketAdmin(admin.ModelAdmin):
    pass


class ItemAdmin(admin.ModelAdmin):
    pass


class CartAdmin(admin.ModelAdmin):
    pass


class OrderAdmin(admin.ModelAdmin):
    pass


admin.site.register(Market, MarketAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
