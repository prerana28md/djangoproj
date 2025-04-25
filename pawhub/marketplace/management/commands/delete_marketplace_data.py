from django.core.management.base import BaseCommand
from marketplace.models import MarketplaceItem

class Command(BaseCommand):
    help = 'Deletes all marketplace items'

    def handle(self, *args, **options):
        count = MarketplaceItem.objects.count()
        MarketplaceItem.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} marketplace items')) 