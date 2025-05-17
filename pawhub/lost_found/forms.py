from django import forms
from .models import LostFound
from pets.models import Pet

class LostPetForm(forms.ModelForm):
    class Meta:
        model = LostFound
        fields = [
            'title', 'description', 'location', 'date', 'image',
            'pet_name', 'pet_type', 'breed', 'age', 'gender', 'color',
            'owner_name', 'contact_info', 'additional_contact', 'status'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a descriptive title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your pet and any identifying features'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Where was your pet last seen?'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'pet_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your pet\'s name'}),
            'pet_type': forms.Select(attrs={'class': 'form-control'}),
            'breed': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your pet\'s breed'}),
            'age': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your pet\'s age'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your pet\'s color and markings'}),
            'owner_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'contact_info': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your phone number and/or email'}),
            'additional_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Additional contact information (optional)'}),
            'status': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].initial = 'lost'

class FoundPetForm(forms.ModelForm):
    class Meta:
        model = LostFound
        fields = [
            'title', 'description', 'location', 'date', 'image',
            'pet_type', 'breed', 'age', 'gender', 'color', 'health_condition',
            'finder_name', 'contact_info', 'additional_contact', 'status'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a descriptive title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the pet and any identifying features'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Where did you find the pet?'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'pet_type': forms.Select(attrs={'class': 'form-control'}),
            'breed': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pet\'s breed (if known)'}),
            'age': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Approximate age'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pet\'s color and markings'}),
            'health_condition': forms.Select(attrs={'class': 'form-control'}),
            'finder_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'contact_info': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your phone number and/or email'}),
            'additional_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Additional contact information (optional)'}),
            'status': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].initial = 'found' 