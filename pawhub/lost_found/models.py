from django.db import models
from django.conf import settings
from pets.models import Pet

class LostFound(models.Model):
    STATUS_CHOICES = [
        ('lost', 'Lost'),
        ('found', 'Found'),
    ]
    
    PET_TYPE_CHOICES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('other', 'Other'),
    ]
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('unknown', 'Unknown'),
    ]
    
    HEALTH_CHOICES = [
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('unknown', 'Unknown'),
    ]

    # Basic Information
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    location = models.CharField(max_length=200)
    date = models.DateField()
    image = models.ImageField(upload_to='lost_found/', null=True, blank=True)
    
    # Pet Information
    pet_name = models.CharField(max_length=100, null=True, blank=True)
    pet_type = models.CharField(max_length=10, choices=PET_TYPE_CHOICES)
    breed = models.CharField(max_length=100, null=True, blank=True)
    age = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='unknown')
    color = models.CharField(max_length=100, null=True, blank=True)
    health_condition = models.CharField(max_length=10, choices=HEALTH_CHOICES, default='unknown')
    
    # Contact Information
    owner_name = models.CharField(max_length=100, null=True, blank=True)
    finder_name = models.CharField(max_length=100, null=True, blank=True)
    contact_info = models.CharField(max_length=200)
    additional_contact = models.CharField(max_length=200, null=True, blank=True)
    
    # Relationships
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_status_display()} - {self.title}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Lost/Found Pet'
        verbose_name_plural = 'Lost/Found Pets'
