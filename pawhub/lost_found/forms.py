from django import forms
from .models import LostFound

class LostPetForm(forms.ModelForm):
    class Meta:
        model = LostFound
        exclude = ['status', 'user', 'created_at', 'updated_at']

class FoundPetForm(forms.ModelForm):
    class Meta:
        model = LostFound
        exclude = ['status', 'user', 'created_at', 'updated_at'] 