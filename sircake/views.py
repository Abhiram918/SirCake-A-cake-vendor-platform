from django.shortcuts import render
from orders.models import Order
from products.models import Cake
from accounts.models import SellerProfile

def home(request):
    query = request.GET.get('q')
    if query:
        from django.urls import reverse
        from django.http import HttpResponseRedirect
        return HttpResponseRedirect(f"{reverse('products:cake_list')}?q={query}")
    
    # If no search, show the beautiful landing page
    return render(request, 'home.html')

def debug_db(request):
    orders = Order.objects.all()
    cakes = Cake.objects.all()
    sellers = SellerProfile.objects.all()
    return render(request, 'debug_db.html', {
        'orders': orders,
        'cakes': cakes,
        'sellers': sellers,
    })
