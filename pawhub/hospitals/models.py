from django.db import models
from django.conf import settings
from django.core.validators import URLValidator
from django.utils import timezone

class Hospital(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    contact = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(validators=[URLValidator()], blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='hospitals/', blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

class Doctor(models.Model):
    SPECIALIZATIONS = [
        ('general', 'General Veterinarian'),
        ('surgery', 'Veterinary Surgeon'),
        ('dermatology', 'Veterinary Dermatologist'),
        ('cardiology', 'Veterinary Cardiologist'),
        ('dentistry', 'Veterinary Dentist'),
        ('other', 'Other Specialization'),
    ]
    
    name = models.CharField(max_length=200)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='doctors')
    specialization = models.CharField(max_length=50, choices=SPECIALIZATIONS)
    qualification = models.CharField(max_length=200)
    experience_years = models.PositiveIntegerField()
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='doctors/', blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dr. {self.name} - {self.get_specialization_display()}"

    class Meta:
        ordering = ['name']
