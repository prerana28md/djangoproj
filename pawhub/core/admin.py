from django.contrib import admin
from .models import Listing, MarketplaceItem

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('pet', 'listing_type', 'status', 'date_posted')
    list_filter = ('listing_type', 'status')
    search_fields = ('pet__name', 'pet__owner__username')
    date_hierarchy = 'date_posted'

@admin.register(MarketplaceItem)
class MarketplaceItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'seller', 'created_at')
    list_filter = ('category',)
    search_fields = ('name', 'description', 'seller__username')
    date_hierarchy = 'created_at'
