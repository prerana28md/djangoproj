from django.contrib import admin
from .models import LostFound

@admin.register(LostFound)
class LostFoundAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'location', 'date', 'user', 'created_at')
    list_filter = ('status', 'date', 'created_at')
    search_fields = ('title', 'description', 'location', 'user__username')
    date_hierarchy = 'created_at'
