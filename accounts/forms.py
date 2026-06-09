from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, CustomerProfile, Address

class CustomerRegistrationForm(UserCreationForm):
    address = forms.CharField(widget=forms.Textarea, required=False)
    phone_number = forms.CharField(max_length=15, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

class SellerRegistrationForm(UserCreationForm):
    shop_name = forms.CharField(max_length=100, required=True)
    shop_description = forms.CharField(widget=forms.Textarea, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)
    phone_number = forms.CharField(max_length=15, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

class DeliveryRegistrationForm(UserCreationForm):
    vehicle_details = forms.CharField(max_length=100, required=True)
    phone_number = forms.CharField(max_length=15, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

class UserProfileForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=15, required=False)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        self.profile_instance = kwargs.pop('profile_instance', None)
        super(UserProfileForm, self).__init__(*args, **kwargs)
        
        # Add form-control for consistent styling
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        
        # Populate initial values for profile fields if not bound
        if not self.is_bound:
            if self.profile_instance:
                self.fields['phone_number'].initial = getattr(self.profile_instance, 'phone_number', '')
                self.fields['address'].initial = getattr(self.profile_instance, 'address', '')
            
            # Form might not auto-populate if we redefined fields or used initials
            if self.instance:
                self.fields['first_name'].initial = self.instance.first_name
                self.fields['last_name'].initial = self.instance.last_name
                self.fields['email'].initial = self.instance.email

    def save(self, commit=True):
        user = super(UserProfileForm, self).save(commit=False)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        
        if commit:
            user.save()
            
        if self.profile_instance:
            self.profile_instance.phone_number = self.cleaned_data.get('phone_number')
            self.profile_instance.address = self.cleaned_data.get('address')
            if commit:
                self.profile_instance.save()
        return user

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['full_name', 'address_line1', 'address_line2', 'city', 'state', 'pincode', 'is_default']
    
    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'is_default':
                self.fields[field].widget.attrs.update({'class': 'form-control'})
