from django.contrib import admin
from .models import Pet, HealthRecord

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'species', 'breed', 'age', 'gender', 'type', 'status', 'price', 'created_at')
    list_filter = ('species', 'gender', 'type', 'status')
    search_fields = ('name', 'breed', 'owner__username', 'location')
    date_hierarchy = 'created_at'
    list_editable = ('status', 'type', 'price')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'owner', 'species', 'breed', 'age', 'gender'),
            'description': 'Owner is required. This is the user who owns the pet.'
        }),
        ('Listing Details', {
            'fields': ('type', 'status', 'price', 'location'),
            'description': 'Type and status are required. Price is required for sale/exchange listings.'
        }),
        ('Additional Information', {
            'fields': ('description', 'image')
        }),
    )
    actions = ['delete_selected']

    def save_model(self, request, obj, form, change):
        # Validate price for sale/exchange listings
        if obj.type in ['sale', 'exchange'] and not obj.price:
            self.message_user(request, "Price is required for sale or exchange listings.", level='error')
            return
        
        # Save the pet
        super().save_model(request, obj, form, change)
        self.message_user(request, f"Pet {'created' if not change else 'updated'} successfully.", level='success')

@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ('pet', 'date', 'type', 'description')
    list_filter = ('type', 'date')
    search_fields = ('pet__name', 'description', 'notes')
    date_hierarchy = 'date'
