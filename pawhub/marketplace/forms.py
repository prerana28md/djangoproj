from django import forms
from .models import MarketplaceItem

class MarketplaceItemForm(forms.ModelForm):
    class Meta:
        model = MarketplaceItem
        fields = ['name', 'category', 'price', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['category'].choices = MarketplaceItem.CATEGORY_CHOICES
        self.fields['image'].required = False
        self.fields['image'].help_text = 'Upload an image for your item (optional)'
        self.fields['image'].widget.attrs.update({
            'class': 'form-control',
            'accept': 'image/*'
        })

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.seller = self.user
        if commit:
            instance.save()
        return instance 