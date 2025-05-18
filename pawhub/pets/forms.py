from django import forms
from .models import Pet, HealthRecord

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'species', 'breed', 'age', 'gender', 'price', 
                 'description', 'image', 'location', 'type', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.1'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'breed': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'species': forms.Select(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['species'].choices = Pet.SPECIES_CHOICES
        self.fields['gender'].choices = Pet.GENDER_CHOICES
        self.fields['type'].choices = Pet.TYPE_CHOICES
        self.fields['status'].choices = Pet.STATUS_CHOICES

    def clean(self):
        cleaned_data = super().clean()
        pet_type = cleaned_data.get('type')
        price = cleaned_data.get('price')

        if pet_type in ['sale', 'exchange'] and not price:
            self.add_error('price', 'Price is required for sale or exchange listings')
        
        return cleaned_data

class HealthRecordForm(forms.ModelForm):
    class Meta:
        model = HealthRecord
        fields = ['date', 'type', 'description', 'notes', 'document']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'document': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].choices = HealthRecord.RECORD_TYPES 