# All marketplace models have been merged into core.models
# Please use core.models.MarketplaceItem instead
# The seller field is implemented as 'shop_owner' in the core model 

from django.db import models

class MarketplaceItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='marketplace/', blank=True, null=True)

    def __str__(self):
        return self.name 