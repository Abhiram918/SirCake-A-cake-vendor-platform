from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from products.models import Cake
from django.contrib import messages

@login_required
def cart_view(request):
    order, created = Order.objects.get_or_create(customer=request.user, status='cart')
    
    if request.method == 'POST':
        cake_id = request.POST.get('cake_id')
        if cake_id:
            cake = get_object_or_404(Cake, id=cake_id)
            if cake.stock_quantity <= 0:
                messages.error(request, f"Sorry, {cake.name} is currently out of stock.")
                return redirect('products:cake_list')

            order_item, created_item = OrderItem.objects.get_or_create(
                order=order, 
                cake=cake,
                defaults={'price': cake.price}
            )
            if not created_item:
                if order_item.quantity + 1 > cake.stock_quantity:
                    messages.error(request, f"Cannot add more {cake.name}. Only {cake.stock_quantity} left in stock.")
                else:
                    order_item.quantity += 1
                    order_item.save()
            
            # update total_amount
            order.total_amount = sum(item.price * item.quantity for item in order.items.all())
            order.save()
            messages.success(request, f"Added {cake.name} to cart.")
            return redirect('orders:cart')
        
        # Remove item logic
        remove_id = request.POST.get('remove_id')
        if remove_id:
            OrderItem.objects.filter(id=remove_id, order=order).delete()
            order.total_amount = sum(item.price * item.quantity for item in order.items.all())
            order.save()
            messages.info(request, "Item removed from cart.")
            return redirect('orders:cart')

    return render(request, 'orders/cart.html', {'order': order})

@login_required
def checkout_view(request):
    order = get_object_or_404(Order, customer=request.user, status='cart')
    profile = getattr(request.user, 'customer_profile', None)
    addresses = profile.addresses.all() if profile else []
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        address_id = request.POST.get('address_id')
        
        # Inventory Check before finalizing
        for item in order.items.all():
            if item.cake.stock_quantity < item.quantity:
                messages.error(request, f"Sorry, {item.cake.name} just went out of stock or does not have enough quantity.")
                return redirect('orders:cart')

        if address_id:
            from accounts.models import Address
            order.shipping_address = get_object_or_404(Address, id=address_id, customer=request.user.customer_profile)
        
        order.payment_method = payment_method
        order.status = 'pending' # Customer placed order, waiting for seller
        order.save()

        # Reduce Stock and update Item status
        for item in order.items.all():
            item.cake.stock_quantity -= item.quantity
            item.cake.save()
            # Item status is 'pending' by default as per model
        
        from payments.models import Payment
        Payment.objects.create(
            order=order, 
            amount=order.total_amount, 
            method=payment_method, 
            status='completed' if payment_method == 'online' else 'pending'
        )
        messages.success(request, "Order placed successfully! Track it in your dashboard.")
        return redirect('dashboard:customer')

    return render(request, 'orders/checkout.html', {
        'order': order,
        'addresses': addresses
    })
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})
