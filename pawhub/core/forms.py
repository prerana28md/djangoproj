from django import forms
from .models import Pet, Listing, HealthRecord, MarketplaceItem

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'type', 'breed', 'age', 'gender', 'health_status', 'vaccination_status', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter pet name'}),
            'type': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'breed': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter breed'}),
            'age': forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'min': '0', 'max': '100'}),
            'gender': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'health_status': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'vaccination_status': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'image': forms.FileInput(attrs={'class': 'form-control form-control-lg'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].choices = Pet.PET_TYPES
        self.fields['gender'].choices = Pet.GENDER_CHOICES
        self.fields['health_status'].choices = Pet.HEALTH_STATUS_CHOICES
        self.fields['vaccination_status'].choices = Pet.VACCINATION_STATUS_CHOICES

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['pet', 'listing_type', 'status']
        widgets = {
            'listing_type': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'status': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'pet': forms.Select(attrs={'class': 'form-select form-select-lg'}),
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
