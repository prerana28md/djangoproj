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

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('unknown', 'Unknown'),
    ]

    HEALTH_STATUS_CHOICES = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('critical', 'Critical'),
    ]

    VACCINATION_STATUS_CHOICES = [
        ('fully_vaccinated', 'Fully Vaccinated'),
        ('partially_vaccinated', 'Partially Vaccinated'),
        ('not_vaccinated', 'Not Vaccinated'),
        ('unknown', 'Unknown'),
    ]

    ADOPTION_STATUS_CHOICES = [
        ('available', 'Available for Adoption'),
        ('requested', 'Adoption Requested'),
        ('adopted', 'Adopted'),
        ('pending', 'Adoption Pending'),
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=PET_TYPES)
    breed = models.CharField(max_length=100)
    age = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='unknown')
    health_status = models.CharField(max_length=20, choices=HEALTH_STATUS_CHOICES, default='good')
    vaccination_status = models.CharField(max_length=20, choices=VACCINATION_STATUS_CHOICES, default='unknown')
    adoption_status = models.CharField(max_length=20, choices=ADOPTION_STATUS_CHOICES, default='available')
    description = models.TextField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_pets')
    image = models.ImageField(upload_to='pets/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class AdoptionRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='adoption_requests')
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='adoption_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    request_date = models.DateTimeField(auto_now_add=True)
    response_date = models.DateTimeField(null=True, blank=True)
    admin_notes = models.TextField(blank=True)
    requester_notes = models.TextField(blank=True)

    def __str__(self):
        return f"Adoption request for {self.pet.name} by {self.requester.username}"

    class Meta:
        ordering = ['-request_date']

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

class HealthRecord(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    record_date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return f"Record for {self.pet.name} on {self.record_date}"

class MarketplaceItem(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'Pet Food'),
        ('toys', 'Toys'),
        ('accessories', 'Accessories'),
        ('health', 'Health & Wellness'),
        ('grooming', 'Grooming'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='marketplace/', blank=True, null=True)
    shop_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='marketplace_items', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    marketplace_item = models.ForeignKey(MarketplaceItem, on_delete=models.CASCADE, null=True, blank=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.marketplace_item:
            return f"{self.quantity} x {self.marketplace_item.name}"
        elif self.listing:
            return f"{self.quantity} x {self.listing.pet.name}"
        return "Invalid cart item"

    @property
    def total_price(self):
        if self.marketplace_item:
            return self.quantity * self.marketplace_item.price
        elif self.listing and self.listing.listing_type == 'sale':
            return self.quantity * self.listing.pet.price
        return 0

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(marketplace_item__isnull=False, listing__isnull=True) | 
                      models.Q(marketplace_item__isnull=True, listing__isnull=False),
                name='cart_item_must_have_one_item'
            )
        ]

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    items = models.ManyToManyField(MarketplaceItem, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    shipping_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

    class Meta:
        ordering = ['-created_at']

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(MarketplaceItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_time = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"

    @property
    def total_price(self):
        return self.quantity * self.price_at_time
