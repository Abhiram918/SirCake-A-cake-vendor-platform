from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from .models import Cake, WishlistItem
from .forms import CakeForm
from django.contrib import messages
from django.http import JsonResponse

def is_seller(user):
    return user.is_authenticated and user.role == 'seller'

def cake_list(request):
    query = request.GET.get('q')
    if query:
        cakes = Cake.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    else:
        cakes = Cake.objects.all()
        
    user_wishlist_cake_ids = []
    if request.user.is_authenticated:
        user_wishlist_cake_ids = request.user.wishlist_items.values_list('cake_id', flat=True)
    return render(request, 'products/list.html', {
        'cakes': cakes, 
        'user_wishlist_cake_ids': user_wishlist_cake_ids,
        'search_query': query
    })

def cake_detail(request, pk):
    cake = get_object_or_404(Cake, pk=pk)
    user_wishlist_cake_ids = []
    if request.user.is_authenticated:
        user_wishlist_cake_ids = request.user.wishlist_items.values_list('cake_id', flat=True)
    return render(request, 'products/detail.html', {'cake': cake, 'user_wishlist_cake_ids': user_wishlist_cake_ids})

@login_required
@user_passes_test(is_seller)
def cake_create(request):
    seller_profile = request.user.seller_profile
    if not seller_profile.is_approved:
        return render(request, 'dashboard/not_approved.html')
        
    if request.method == 'POST':
        form = CakeForm(request.POST, request.FILES)
        if form.is_valid():
            cake = form.save(commit=False)
            cake.seller = seller_profile
            cake.save()
            return redirect('sellers:dashboard')
    else:
        form = CakeForm()
    
    return render(request, 'products/cake_form.html', {
        'form': form,
        'title': 'Add New Cake',
        'button_text': 'Launch Cake listing'
    })

@login_required
@user_passes_test(is_seller)
def cake_update(request, pk):
    seller_profile = request.user.seller_profile
    cake = get_object_or_404(Cake, pk=pk, seller=seller_profile)
    
    if request.method == 'POST':
        form = CakeForm(request.POST, request.FILES, instance=cake)
        if form.is_valid():
            form.save()
            return redirect('sellers:dashboard')
    else:
        form = CakeForm(instance=cake)
    
    return render(request, 'products/cake_form.html', {
        'form': form,
        'cake': cake,
        'title': f'Edit {cake.name}',
        'button_text': 'Update listing'
    })

@login_required
def toggle_wishlist(request, cake_id):
    cake = get_object_or_404(Cake, id=cake_id)
    wishlist_item, created = WishlistItem.objects.get_or_create(user=request.user, cake=cake)
    
    if not created:
        wishlist_item.delete()
        action = "removed from"
    else:
        action = "added to"
        
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'action': action})
    
    messages.success(request, f"{cake.name} has been {action} your wishlist.")
    return redirect(request.META.get('HTTP_REFERER', 'products:cake_list'))

@login_required
def wishlist_view(request):
    wishlist_items = WishlistItem.objects.filter(user=request.user).select_related('cake', 'cake__seller')
    return render(request, 'products/wishlist.html', {'wishlist_items': wishlist_items})
