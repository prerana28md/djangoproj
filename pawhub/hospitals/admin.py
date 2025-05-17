from django.contrib import admin
from .models import Hospital, Doctor

@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'contact', 'email', 'owner', 'created_at')
    search_fields = ('name', 'address', 'contact', 'email')
    list_filter = ('created_at', 'owner')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'hospital', 'specialization', 'qualification', 'experience_years')
    search_fields = ('name', 'specialization', 'qualification')
    list_filter = ('specialization', 'hospital')
