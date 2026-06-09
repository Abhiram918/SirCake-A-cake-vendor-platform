from django import forms
from accounts.models import SellerProfile
from products.models import Cake, Category

class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = ['shop_name', 'shop_description', 'shop_logo', 'shop_banner', 'address', 'phone_number']
        widgets = {
            'shop_description': forms.Textarea(attrs={'rows': 4}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class SellerCakeForm(forms.ModelForm):
    class Meta:
        model = Cake
        fields = ['category', 'name', 'description', 'price', 'discount_price', 'flavor', 'weight', 'image', 'stock_quantity', 'is_eggless', 'is_available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field not in ['is_eggless', 'is_available', 'category']:
                self.fields[field].widget.attrs.update({'class': 'form-control'})
            elif field == 'category':
                self.fields[field].widget.attrs.update({'class': 'form-select'})
        
        # Make category optional in the form if it's causing issues, 
        # but better to have it so let's just make sure it's styled correctly first.
        self.fields['category'].required = False
        self.fields['category'].empty_label = "Select a Category (Optional)"
        
        self.fields['is_eggless'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['is_available'].widget.attrs.update({'class': 'form-check-input'})
