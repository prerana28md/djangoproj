from django.core.management.base import BaseCommand
from pets.models import Pet

class Command(BaseCommand):
    help = 'Check pets in the database'

    def handle(self, *args, **options):
        self.stdout.write('Checking pets in database...')
        
        # Get all pets
        pets = Pet.objects.all()
        
        if not pets.exists():
            self.stdout.write(self.style.WARNING('No pets found in database!'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'Found {pets.count()} pets:'))
        
        for pet in pets:
            self.stdout.write(f'- {pet.name} (ID: {pet.id})')
            self.stdout.write(f'  Owner: {pet.owner}')
            self.stdout.write(f'  Species: {pet.species}')
            self.stdout.write(f'  Breed: {pet.breed}')
            self.stdout.write(f'  Age: {pet.age}')
            self.stdout.write(f'  Listing Type: {pet.listing_type}')
            self.stdout.write(f'  Status: {pet.status}')
            self.stdout.write(f'  Created: {pet.created_at}')
            self.stdout.write('---') 