from django import forms
from .models import Cake

class CakeForm(forms.ModelForm):
    class Meta:
        model = Cake
        fields = [
            'category', 'name', 'description', 'price', 
            'discount_price', 'weight', 'image', 
            'is_eggless', 'is_available', 'customization_options'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Signature Chocolate Cake'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your cake...'}),
            'weight': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1kg / 500g'}),
            'customization_options': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Special messages, toppings etc.'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'discount_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_eggless': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
