from django.core.management.base import BaseCommand
from django.core.files import File
from core.models import MarketplaceItem
from django.contrib.auth import get_user_model
import os
from django.conf import settings

User = get_user_model()

class Command(BaseCommand):
    help = 'Adds sample marketplace items with images'

    def handle(self, *args, **kwargs):
        # Get or create a default user
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            user.set_password('admin')
            user.save()

        # Sample items
        items = [
            {
                'name': 'Premium Dog Food',
                'description': 'High-quality dog food with balanced nutrition for adult dogs.',
                'price': 49.99,
                'stock': 50,
                'category': 'food',
            },
            {
                'name': 'Interactive Cat Toy',
                'description': 'Engaging toy that keeps your cat active and entertained.',
                'price': 19.99,
                'stock': 30,
                'category': 'toys',
            },
            {
                'name': 'Designer Pet Collar',
                'description': 'Stylish and comfortable collar for your furry friend.',
                'price': 24.99,
                'stock': 25,
                'category': 'accessories',
            },
            {
                'name': 'Pet Vitamins',
                'description': 'Essential vitamins for your pet\'s health and wellbeing.',
                'price': 29.99,
                'stock': 40,
                'category': 'health',
            },
            {
                'name': 'Professional Grooming Kit',
                'description': 'Complete grooming kit for maintaining your pet\'s coat.',
                'price': 39.99,
                'stock': 20,
                'category': 'grooming',
            }
        ]

        # Create items
        for item_data in items:
            item = MarketplaceItem.objects.create(
                name=item_data['name'],
                description=item_data['description'],
                price=item_data['price'],
                stock=item_data['stock'],
                category=item_data['category'],
                shop_owner=user
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created item: {item.name}')) 