from django import forms
from .models import MarketplaceItem

class MarketplaceItemForm(forms.ModelForm):
    class Meta:
        model = MarketplaceItem
        fields = ['name', 'description', 'price', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False
        self.fields['image'].help_text = 'Upload an image for your item (optional)'
        self.fields['image'].widget.attrs.update({
            'class': 'form-control',
            'accept': 'image/*'
        })

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.shop_owner = self.user  # fixed field name
        if commit:
            instance.save()
        return instance
