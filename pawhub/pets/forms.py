from django import forms
from .models import Pet, HealthRecord

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'species', 'breed', 'age', 'gender', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter pet name'}),
            'species': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'breed': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter breed'}),
            'age': forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'min': '0'}),
            'gender': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-lg', 'rows': 4, 'placeholder': 'Enter pet description'}),
            'image': forms.FileInput(attrs={'class': 'form-control form-control-lg'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['species'].choices = Pet.SPECIES_CHOICES
        self.fields['gender'].choices = Pet.GENDER_CHOICES

class HealthRecordForm(forms.ModelForm):
    class Meta:
        model = HealthRecord
        fields = ['date', 'type', 'description', 'notes', 'document']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-lg'}),
            'type': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'description': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'notes': forms.Textarea(attrs={'class': 'form-control form-control-lg', 'rows': 4}),
            'document': forms.FileInput(attrs={'class': 'form-control form-control-lg'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].choices = HealthRecord.RECORD_TYPES 