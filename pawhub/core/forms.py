from django import forms
from .models import Pet, Listing, HealthRecord, MarketplaceItem, AdoptionRequest, CartItem, Order
from lost_found.models import LostFound

class PetForm(forms.ModelForm):
    type = forms.ChoiceField(
        choices=[
            ('adoption', 'Adoption'),
            ('sale', 'Sale'),
            ('exchange', 'Exchange'),
            ('lost', 'Lost'),
            ('found', 'Found'),
        ],
        widget=forms.Select(attrs={'class': 'form-select form-select-lg'})
    )

    class Meta:
        model = Pet
        fields = ['name', 'species', 'breed', 'age', 'gender', 'price', 'description', 'image', 'location', 'type', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter pet name'}),
            'species': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'breed': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter breed'}),
            'age': forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'min': '0'}),
            'gender': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'price': forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'min': '0', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-lg', 'rows': 4, 'placeholder': 'Enter pet description'}),
            'image': forms.FileInput(attrs={'class': 'form-control form-control-lg'}),
            'location': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter location'}),
            'status': forms.Select(attrs={'class': 'form-select form-select-lg'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['species'].choices = Pet.SPECIES_CHOICES
        self.fields['gender'].choices = Pet.GENDER_CHOICES
        self.fields['status'].choices = Pet.STATUS_CHOICES

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['pet', 'status']
        widgets = {
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

class AdoptionRequestForm(forms.ModelForm):
    class Meta:
        model = AdoptionRequest
        fields = ['requester_notes']
        widgets = {
            'requester_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us why you would be a good fit for this pet...'
            })
        }

class AdoptionRequestResponseForm(forms.ModelForm):
    class Meta:
        model = AdoptionRequest
        fields = ['status', 'admin_notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'admin_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Add any notes about this adoption request...'
            })
        }

class MarketplaceItemForm(forms.ModelForm):
    class Meta:
        model = MarketplaceItem
        fields = ['name', 'description', 'price', 'stock', 'category', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter item name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter item description'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.FileInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].choices = MarketplaceItem.CATEGORY_CHOICES

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '99'
            })
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['shipping_address', 'shipping_city', 'shipping_state', 'shipping_zip', 'phone_number', 'notes']
        widgets = {
            'shipping_address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your street address'
            }),
            'shipping_city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your city'
            }),
            'shipping_state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your state'
            }),
            'shipping_zip': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your ZIP code'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add any special instructions or notes for your order (optional)'
            })
        }

class MarketplaceSearchForm(forms.Form):
    category = forms.ChoiceField(
        choices=[('', 'All Categories')] + list(MarketplaceItem.CATEGORY_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    min_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min Price'
        })
    )
    max_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max Price'
        })
    )
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search items...'
        })
    )

class LostPetForm(forms.ModelForm):
    pet_name = forms.CharField(max_length=100, required=True)
    pet_type = forms.ChoiceField(choices=Pet.SPECIES_CHOICES, required=True)
    breed = forms.CharField(max_length=100, required=True)
    age = forms.IntegerField(required=True, min_value=0)
    gender = forms.ChoiceField(choices=Pet.GENDER_CHOICES, required=True)
    color = forms.CharField(max_length=50, required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)
    location = forms.CharField(max_length=200, required=True)
    date_lost = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    image = forms.ImageField(required=True)
    contact_info = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = LostFound
        fields = ['pet_name', 'pet_type', 'breed', 'age', 'gender', 'color', 'description', 
                 'location', 'date_lost', 'image', 'contact_info']

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        instance.user = user
        instance.listing_type = 'lost'
        instance.status = 'active'
        
        if commit:
            instance.save()
        return instance

class FoundPetForm(forms.ModelForm):
    pet_name = forms.CharField(max_length=100, required=True)
    pet_type = forms.ChoiceField(choices=Pet.SPECIES_CHOICES, required=True)
    breed = forms.CharField(max_length=100, required=True)
    age = forms.IntegerField(required=True, min_value=0)
    gender = forms.ChoiceField(choices=Pet.GENDER_CHOICES, required=True)
    color = forms.CharField(max_length=50, required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)
    location = forms.CharField(max_length=200, required=True)
    date_found = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    image = forms.ImageField(required=True)
    contact_info = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = LostFound
        fields = ['pet_name', 'pet_type', 'breed', 'age', 'gender', 'color', 'description', 
                 'location', 'date_found', 'image', 'contact_info']

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        instance.user = user
        instance.listing_type = 'found'
        instance.status = 'active'
        
        if commit:
            instance.save()
        return instance
