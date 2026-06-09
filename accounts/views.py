from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomerRegistrationForm, SellerRegistrationForm, DeliveryRegistrationForm, UserProfileForm, AddressForm
from .models import User, Address

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            # Role redirection
            if user.role == 'customer':
                return redirect('dashboard:customer')
            elif user.role == 'seller':
                return redirect('sellers:dashboard')
            elif user.role == 'delivery':
                return redirect('delivery:dashboard')
            elif user.role == 'admin':
                return redirect('dashboard:admin_approvals')
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "Successfully logged out.")
    return redirect('home')

def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'customer'
            user.save()
            # The signal creates the profile. We can update it here.
            profile = user.customer_profile
            profile.address = form.cleaned_data.get('address')
            profile.phone_number = form.cleaned_data.get('phone_number')
            profile.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('dashboard:customer')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'accounts/register_customer.html', {'form': form})

def register_seller(request):
    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'seller'
            user.save()
            profile = user.seller_profile
            profile.shop_name = form.cleaned_data.get('shop_name')
            profile.shop_description = form.cleaned_data.get('shop_description')
            profile.address = form.cleaned_data.get('address')
            profile.phone_number = form.cleaned_data.get('phone_number')
            profile.save()
            # Do not login automatically, requires admin approval
            messages.success(request, "Registration successful! Please wait for admin approval.")
            return redirect('accounts:login')
    else:
        form = SellerRegistrationForm()
    return render(request, 'accounts/register_seller.html', {'form': form})

def register_delivery(request):
    if request.method == 'POST':
        form = DeliveryRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'delivery'
            user.save()
            profile = user.delivery_profile
            profile.vehicle_details = form.cleaned_data.get('vehicle_details')
            profile.phone_number = form.cleaned_data.get('phone_number')
            profile.save()
            # Do not login automatically, requires admin approval
            messages.success(request, "Registration successful! Please wait for admin approval.")
            return redirect('accounts:login')
    else:
        form = DeliveryRegistrationForm()
    return render(request, 'accounts/register_delivery.html', {'form': form})

@login_required
def profile_view(request):
    if request.user.role == 'customer':
        profile = getattr(request.user, 'customer_profile', None)
    elif request.user.role == 'seller':
        profile = getattr(request.user, 'seller_profile', None)
    elif request.user.role == 'delivery':
        profile = getattr(request.user, 'delivery_profile', None)
    else:
        profile = None

    return render(request, 'accounts/profile.html', {
        'view_user': request.user,
        'profile': profile
    })

@login_required
def profile_edit_view(request):
    if request.user.role == 'customer':
        profile = getattr(request.user, 'customer_profile', None)
    elif request.user.role == 'seller':
        profile = getattr(request.user, 'seller_profile', None)
    elif request.user.role == 'delivery':
        profile = getattr(request.user, 'delivery_profile', None)
    else:
        profile = None

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user, profile_instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user, profile_instance=profile)

    return render(request, 'accounts/profile_edit.html', {'form': form})
@login_required
def address_list_view(request):
    if request.user.role != 'customer':
        messages.error(request, "Only customers can manage saved addresses.")
        return redirect('home')
    
    addresses = request.user.customer_profile.addresses.all()
    return render(request, 'accounts/address_list.html', {'addresses': addresses})

@login_required
def address_create_view(request):
    if request.user.role != 'customer':
        messages.error(request, "Only customers can manage saved addresses.")
        return redirect('home')
    
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.customer = request.user.customer_profile
            address.save()
            messages.success(request, "Address added successfully!")
            return redirect('accounts:address_list')
    else:
        form = AddressForm()
    
    return render(request, 'accounts/address_form.html', {'form': form, 'title': 'Add New Address'})

@login_required
def address_delete_view(request, pk):
    if request.user.role != 'customer':
        messages.error(request, "Only customers can manage saved addresses.")
        return redirect('home')
    
    address = Address.objects.get(pk=pk, customer=request.user.customer_profile)
    address.delete()
    messages.success(request, "Address deleted successfully!")
    return redirect('accounts:address_list')
