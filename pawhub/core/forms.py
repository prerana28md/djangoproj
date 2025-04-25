from django import forms
from .models import Pet, Listing, MarketplaceItem
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
            'listing_type': forms.Select(),
            'status': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['pet'].queryset = Pet.objects.filter(owner=user)

class MarketplaceItemForm(forms.ModelForm):
    class Meta:
        model = MarketplaceItem
        fields = ['name', 'category', 'price', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'price': forms.NumberInput(attrs={'min': '0', 'step': '0.01'})
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user
