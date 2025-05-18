from django.contrib import admin
from .models import Listing, MarketplaceItem

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('pet', 'status', 'date_posted')
    list_filter = ('status', 'date_posted')
    search_fields = ('pet__name', 'pet__species', 'pet__breed')
    date_hierarchy = 'date_posted'
    ordering = ('-date_posted',)

@admin.register(MarketplaceItem)
class MarketplaceItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'shop_owner', 'created_at')
    list_filter = ('category',)
    search_fields = ('name', 'description', 'shop_owner__username')
    date_hierarchy = 'created_at'
