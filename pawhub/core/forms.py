from django import forms
from .models import Pet, Listing, HealthRecord, MarketplaceItem

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'type', 'breed', 'age', 'health_status', 'vaccination_status', 'image']
        widgets = {
            'health_status': forms.Textarea(attrs={'rows': 3}),
            'vaccination_status': forms.TextInput(attrs={'placeholder': 'e.g. Fully vaccinated'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['pet', 'listing_type', 'status']
        widgets = {
            'listing_type': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'pet': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['pet'].queryset = Pet.objects.filter(owner=user)
            self.fields['pet'].empty_label = "Select a pet"
            self.fields['pet'].label = "Pet"

class HealthRecordForm(forms.ModelForm):
    class Meta:
        model = HealthRecord
        fields = ['record_date', 'description']
        widgets = {
            'record_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class MarketplaceItemForm(forms.ModelForm):
    class Meta:
        model = MarketplaceItem
        fields = ['name', 'category', 'price', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'price': forms.NumberInput(attrs={'min': '0', 'step': '0.01'}),
            'image': forms.FileInput(attrs={'class': 'form-control'})
        }
