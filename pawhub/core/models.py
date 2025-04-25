from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Pet(models.Model):
    PET_TYPES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('fish', 'Fish'),
        ('reptile', 'Reptile'),
        ('other', 'Other'),
    ]
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=PET_TYPES)
    breed = models.CharField(max_length=100)
    age = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    health_status = models.TextField()
    vaccination_status = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='pets/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Listing(models.Model):
    LISTING_TYPES = [
        ('adoption', 'Adoption'),
        ('sale', 'Sale'),
        ('exchange', 'Exchange'),
    ]
    STATUS = [
        ('available', 'Available'),
        ('adopted', 'Adopted'),
        ('removed', 'Removed'),
    ]
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    listing_type = models.CharField(max_length=20, choices=LISTING_TYPES)
    status = models.CharField(max_length=20, choices=STATUS, default='available')
    date_posted = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.listing_type} - {self.pet.name}"

class Hospital(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    contact = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class HealthRecord(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    record_date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return f"Record for {self.pet.name} on {self.record_date}"

class MarketplaceItem(models.Model):
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Toys', 'Toys'),
        ('Bedding', 'Bedding'),
        ('Grooming', 'Grooming'),
        ('Other', 'Other'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.name
