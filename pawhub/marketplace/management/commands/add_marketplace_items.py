from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import MarketplaceItem

User = get_user_model()

class Command(BaseCommand):
    help = 'Add sample items to the marketplace'

    def handle(self, *args, **kwargs):
        # Get or create a default seller
        seller, created = User.objects.get_or_create(
            username='default_seller',
            defaults={
                'email': 'seller@example.com',
                'is_staff': True
            }
        )
        if created:
            seller.set_password('defaultpassword')
            seller.save()
            self.stdout.write(self.style.SUCCESS(f'Created default seller: {seller.username}'))

        items = [
            {
                'name': 'Rubber Chew Bone',
                'description': 'Durable chew toy for dogs.',
                'price': 4.99,
                'category': 'toys',
                'stock': 10
            },
            {
                'name': 'Feather Wand',
                'description': 'Interactive toy for cats.',
                'price': 3.49,
                'category': 'toys',
                'stock': 15
            },
            {
                'name': 'Premium Dog Food',
                'description': 'High-quality dog food for all breeds.',
                'price': 29.99,
                'category': 'food',
                'stock': 20
            },
            {
                'name': 'Cat Scratcher',
                'description': 'A scratching post for cats.',
                'price': 14.99,
                'category': 'accessories',
                'stock': 8
            },
            {
                'name': 'Bird Cage',
                'description': 'Spacious cage for small birds.',
                'price': 49.99,
                'category': 'accessories',
                'stock': 5
            },
            {
                'name': 'Cat Litter Box',
                'description': 'Modern and easy-to-clean litter box.',
                'price': 24.99,
                'category': 'accessories',
                'stock': 12
            },
            {
                'name': 'Dog Seat-belt Harness',
                'description': 'Keeps pets safe in car.',
                'price': 10.99,
                'category': 'accessories',
                'stock': 15
            }
        ]
        
        for item in items:
            try:
                MarketplaceItem.objects.create(
                    name=item['name'],
                    description=item['description'],
                    price=item['price'],
                    category=item['category'],
                    stock=item['stock'],
                    shop_owner=seller
                )
                self.stdout.write(self.style.SUCCESS(f"Added item: {item['name']}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error adding item {item['name']}: {str(e)}")) 