from django.contrib import admin
from .models import Market, Item


class MarketAdmin(admin.ModelAdmin):
    pass


class ItemAdmin(admin.ModelAdmin):
    pass


admin.site.register(Market, MarketAdmin)
admin.site.register(Item, ItemAdmin)
