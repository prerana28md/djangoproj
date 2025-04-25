from django.contrib import admin
from .models import Pet, HealthRecord

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'species', 'breed', 'age', 'gender', 'created_at')
    list_filter = ('species', 'gender')
    search_fields = ('name', 'breed', 'owner__username')
    date_hierarchy = 'created_at'
    actions = ['delete_selected']

@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ('pet', 'date', 'type', 'description')
    list_filter = ('type', 'date')
    search_fields = ('pet__name', 'description', 'notes')
    date_hierarchy = 'date'
