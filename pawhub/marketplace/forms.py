from django import forms
from .models import MarketplaceItem, PetListing
from core.models import Pet

class MarketplaceItemForm(forms.ModelForm):
    class Meta:
        model = MarketplaceItem
        fields = ['name', 'category', 'price', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['category'].choices = MarketplaceItem.CATEGORY_CHOICES
        self.fields['image'].required = False
        self.fields['image'].help_text = 'Upload an image for your item (optional)'
        self.fields['image'].widget.attrs.update({
            'class': 'form-control',
            'accept': 'image/*'
        })

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.seller = self.user
        if commit:
            instance.save()
        return instance

class PetListingForm(forms.ModelForm):
    class Meta:
        model = PetListing
        fields = ['pet', 'price', 'description']
        widgets = {
            'price': forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'min': '0', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-lg', 'rows': 4}),
            'pet': forms.Select(attrs={'class': 'form-select form-select-lg'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            # Only show pets owned by the current user
            pets = Pet.objects.filter(owner=self.user)
            print(f"Found {pets.count()} pets for user {self.user.username}")
            for pet in pets:
                print(f"Pet: {pet.name} (Type: {pet.type}, Breed: {pet.breed})")
            self.fields['pet'].queryset = pets
            self.fields['pet'].empty_label = "Select a pet"
            self.fields['pet'].label = "Pet"
            self.fields['pet'].help_text = "Choose a pet to list for sale"
            self.fields['price'].label = "Price ($)"
            self.fields['price'].help_text = "Enter the price in dollars"
            self.fields['description'].label = "Description"
            self.fields['description'].help_text = "Provide details about the pet and why you're selling it"

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.seller = self.user
        if commit:
            instance.save()
        return instance 