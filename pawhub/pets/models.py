from django.db import models
from django.conf import settings

class Pet(models.Model):
    SPECIES_CHOICES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('fish', 'Fish'),
        ('reptile', 'Reptile'),
        ('other', 'Other'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('unknown', 'Unknown'),
    ]

    TYPE_CHOICES = [
        ('adoption', 'For Adoption'),
        ('sale', 'For Sale'),
        ('exchange', 'For Exchange'),
        ('lost', 'Lost Pet'),
        ('found', 'Found Pet'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('pending', 'Pending'),
        ('adopted', 'Adopted'),
        ('sold', 'Sold'),
        ('exchanged', 'Exchanged'),
        ('returned', 'Returned to Owner'),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pets')
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=20, choices=SPECIES_CHOICES)
    breed = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='pets/', blank=True, null=True)
    location = models.CharField(max_length=200, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='adoption')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

    def get_type_display(self):
        return dict(self.TYPE_CHOICES)[self.type]

    class Meta:
        ordering = ['-created_at']

class HealthRecord(models.Model):
    RECORD_TYPES = [
        ('vaccination', 'Vaccination'),
        ('checkup', 'Checkup'),
        ('surgery', 'Surgery'),
        ('medication', 'Medication'),
        ('other', 'Other'),
    ]

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='health_records')
    date = models.DateField()
    type = models.CharField(max_length=20, choices=RECORD_TYPES)
    description = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    document = models.FileField(upload_to='health_records/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pet.name}'s {self.type} on {self.date}"

    class Meta:
        ordering = ['-date']
