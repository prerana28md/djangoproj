from django import forms
from .models import LostFound
from pets.models import Pet

class LostPetForm(forms.ModelForm):
    class Meta:
        model = LostFound
        fields = ['pet', 'title', 'description', 'location', 'date', 'image', 'contact_info']
        widgets = {
            'pet': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'title': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter title'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-lg', 'rows': 4, 'placeholder': 'Enter description'}),
            'location': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter location'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-lg'}),
            'image': forms.FileInput(attrs={'class': 'form-control form-control-lg'}),
            'contact_info': forms.Textarea(attrs={'class': 'form-control form-control-lg', 'rows': 3, 'placeholder': 'Enter contact information'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['pet'].queryset = Pet.objects.filter(owner=user)
            self.fields['pet'].empty_label = "Select a pet (optional)"
            self.fields['pet'].label = "Pet"

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.status = 'lost'
        if commit:
            instance.save()
        return instance

class FoundPetForm(forms.ModelForm):
    class Meta:
        model = LostFound
        fields = ['pet', 'title', 'description', 'location', 'date', 'image', 'contact_info']
        widgets = {
            'pet': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'title': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter title'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-lg', 'rows': 4, 'placeholder': 'Enter description'}),
            'location': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter location'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-lg'}),
            'image': forms.FileInput(attrs={'class': 'form-control form-control-lg'}),
            'contact_info': forms.Textarea(attrs={'class': 'form-control form-control-lg', 'rows': 3, 'placeholder': 'Enter contact information'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['pet'].queryset = Pet.objects.filter(owner=user)
            self.fields['pet'].empty_label = "Select a pet (optional)"
            self.fields['pet'].label = "Pet"

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.status = 'found'
        if commit:
            instance.save()
        return instance 