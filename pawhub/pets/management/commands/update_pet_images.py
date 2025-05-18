import os
import requests
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from pets.models import Pet
from tempfile import NamedTemporaryFile

class Command(BaseCommand):
    help = 'Updates pet images based on their breed and species'

    def handle(self, *args, **kwargs):
        # Pexels API key
        PEXELS_API_KEY = 'gByRVaXEt2jwPnffUdWrKMuJkY7KAKvIJnBAb1m6H4HZioredAGJaWx8'
        
        # Dictionary mapping species to search terms
        species_terms = {
            'dog': 'dog',
            'cat': 'cat',
            'bird': 'bird',
            'fish': 'fish',
            'reptile': 'reptile'
        }

        # Dictionary mapping breeds to specific search terms
        breed_terms = {
            'Pomeranian': 'pomeranian dog',
            'Pug': 'pug dog',
            'Himalayan': 'himalayan cat',
            'Gecko': 'gecko reptile',
            'Cockatiel': 'cockatiel bird',
            'Chameleon': 'chameleon reptile',
            'Betta': 'betta fish',
            'British Shorthair': 'british shorthair cat',
            'Doberman': 'doberman dog',
            'Parrot': 'parrot bird',
            'Beagle': 'beagle dog',
            'Maine Coon': 'maine coon cat',
            'Husky': 'husky dog',
            'Iguana': 'iguana reptile',
            'Siamese': 'siamese cat',
            'German Shepherd': 'german shepherd dog',
            'Clownfish': 'clownfish',
            'Canary': 'canary bird',
            'Persian': 'persian cat',
            'Labrador': 'labrador dog'
        }

        # Create media directory if it doesn't exist
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'pets'), exist_ok=True)

        headers = {
            'Authorization': PEXELS_API_KEY
        }

        for pet in Pet.objects.all():
            if pet.image:
                self.stdout.write(f"Pet {pet.name} already has an image, skipping...")
                continue

            # Get search term for the pet
            search_term = breed_terms.get(pet.breed, f"{pet.breed} {species_terms.get(pet.species, '')}")
            
            try:
                # Use Pexels API to search for images
                search_url = f"https://api.pexels.com/v1/search?query={search_term}&per_page=1"
                response = requests.get(search_url, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    if data['photos']:
                        # Get the first photo URL
                        photo_url = data['photos'][0]['src']['medium']
                        
                        # Download the image
                        img_response = requests.get(photo_url)
                        if img_response.status_code == 200:
                            # Create a temporary file to save the image
                            img_temp = NamedTemporaryFile(delete=True)
                            img_temp.write(img_response.content)
                            img_temp.flush()

                            # Save the image to the pet
                            pet.image.save(
                                f"{pet.name.lower()}_{pet.breed.lower()}.jpg",
                                File(img_temp),
                                save=True
                            )
                            
                            self.stdout.write(
                                self.style.SUCCESS(f"Successfully added image for {pet.name} ({pet.breed})")
                            )
                        else:
                            self.stdout.write(
                                self.style.WARNING(f"Failed to download image for {pet.name} ({pet.breed})")
                            )
                    else:
                        self.stdout.write(
                            self.style.WARNING(f"No images found for {pet.name} ({pet.breed})")
                        )
                else:
                    self.stdout.write(
                        self.style.WARNING(f"Failed to search for image for {pet.name} ({pet.breed})")
                    )
            
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Error processing {pet.name}: {str(e)}")
                ) 