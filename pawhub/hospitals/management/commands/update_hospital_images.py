import os
import requests
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from hospitals.models import Hospital
from tempfile import NamedTemporaryFile
import random

class Command(BaseCommand):
    help = 'Updates hospital images based on their name and type'

    def handle(self, *args, **kwargs):
        # Pexels API key
        PEXELS_API_KEY = 'gByRVaXEt2jwPnffUdWrKMuJkY7KAKvIJnBAb1m6H4HZioredAGJaWx8'
        
        # Dictionary mapping hospital names to search terms with multiple options
        hospital_terms = {
            'Loving Paws Veterinary Clinic': [
                'modern veterinary clinic exterior',
                'veterinary hospital front desk',
                'pet hospital waiting room'
            ],
            'Happy Hearts Animal Hospital': [
                'veterinary clinic reception',
                'animal hospital building',
                'pet care center exterior'
            ],
            'The Pet Doctor': [
                'veterinary examination room',
                'pet clinic interior',
                'animal hospital modern'
            ],
            'Tail Waggers Vet Clinic': [
                'veterinary clinic modern',
                'pet hospital building',
                'animal care center exterior'
            ],
            'Animal Care Veterinary Hospital': [
                'veterinary hospital building',
                'pet clinic waiting area',
                'animal hospital reception'
            ],
            'Pet Wellness Clinic': [
                'modern veterinary clinic',
                'pet hospital interior',
                'animal care center modern'
            ],
            'Cuddle Care Animal Hospital': [
                'veterinary clinic cozy',
                'pet hospital warm',
                'animal care center comfortable'
            ],
            'Four Paws Veterinary Center': [
                'veterinary center modern',
                'pet hospital facility',
                'animal care center building'
            ],
            'Happy Pets Vet Hospital': [
                'veterinary hospital cheerful',
                'pet clinic bright',
                'animal hospital welcoming'
            ],
            'Gentle Touch Animal Clinic': [
                'veterinary clinic gentle',
                'pet hospital caring',
                'animal care center peaceful'
            ],
            'Happy Paws Veterinary Care': [
                'veterinary care modern',
                'pet hospital facility',
                'animal care center building'
            ],
            'Whiskers & Paws Hospital': [
                'veterinary hospital cozy',
                'pet clinic warm',
                'animal hospital welcoming'
            ],
            'Four Legs Vet Center': [
                'veterinary center modern',
                'pet hospital facility',
                'animal care center building'
            ],
            'Happy Tails Veterinary Clinic': [
                'veterinary clinic cheerful',
                'pet hospital bright',
                'animal care center welcoming'
            ],
            'Paws & Claws Animal Hospital': [
                'veterinary hospital modern',
                'pet clinic facility',
                'animal care center building'
            ]
        }

        # Create media directory if it doesn't exist
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'hospitals'), exist_ok=True)

        headers = {
            'Authorization': PEXELS_API_KEY
        }

        for hospital in Hospital.objects.all():
            # Get search terms for the hospital
            search_terms = hospital_terms.get(hospital.name, [f"veterinary hospital {hospital.name}"])
            search_term = random.choice(search_terms)
            
            try:
                # Use Pexels API to search for images with more results
                search_url = f"https://api.pexels.com/v1/search?query={search_term}&per_page=5"
                response = requests.get(search_url, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    if data['photos']:
                        # Randomly select one of the photos
                        photo = random.choice(data['photos'])
                        photo_url = photo['src']['medium']
                        
                        # Download the image
                        img_response = requests.get(photo_url)
                        if img_response.status_code == 200:
                            # Create a temporary file to save the image
                            img_temp = NamedTemporaryFile(delete=True)
                            img_temp.write(img_response.content)
                            img_temp.flush()

                            # Delete old image if it exists
                            if hospital.image:
                                try:
                                    os.remove(hospital.image.path)
                                except:
                                    pass

                            # Save the image to the hospital
                            hospital.image.save(
                                f"{hospital.name.lower().replace(' ', '_')}.jpg",
                                File(img_temp),
                                save=True
                            )
                            
                            self.stdout.write(
                                self.style.SUCCESS(f"Successfully updated image for {hospital.name}")
                            )
                        else:
                            self.stdout.write(
                                self.style.WARNING(f"Failed to download image for {hospital.name}")
                            )
                    else:
                        self.stdout.write(
                            self.style.WARNING(f"No images found for {hospital.name}")
                        )
                else:
                    self.stdout.write(
                        self.style.WARNING(f"Failed to search for image for {hospital.name}")
                    )
            
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Error processing {hospital.name}: {str(e)}")
                ) 