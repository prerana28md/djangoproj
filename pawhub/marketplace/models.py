from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class MarketplaceItem(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'Pet Food'),
        ('toys', 'Toys'),
        ('accessories', 'Accessories'),
        ('supplies', 'Supplies'),
        ('other', 'Other')
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='marketplace/', blank=True, null=True)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='marketplace_items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
