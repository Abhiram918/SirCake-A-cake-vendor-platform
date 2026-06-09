from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Count, Avg
from orders.models import Order
from products.models import Cake
from accounts.models import User, SellerProfile, DeliveryProfile
from delivery.models import DeliveryAssignment

def is_customer(user): return user.role == 'customer'
def is_seller(user): return user.role == 'seller'
def is_delivery(user): return user.role == 'delivery'
def is_admin(user): return user.role == 'admin'

@login_required
@user_passes_test(is_customer)
def customer_dashboard(request):
    orders = Order.objects.filter(customer=request.user).exclude(status='cart').order_by('-created_at')
    return render(request, 'dashboard/customer.html', {'orders': orders})


@login_required
@user_passes_test(is_admin)
def admin_approvals(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve_seller':
            SellerProfile.objects.filter(id=request.POST.get('id')).update(is_approved=True)
        elif action == 'approve_delivery':
            DeliveryProfile.objects.filter(id=request.POST.get('id')).update(is_approved=True)
        return redirect('dashboard:admin_approvals')

    context = {
        'pending_sellers': SellerProfile.objects.filter(is_approved=False),
        'pending_delivery': DeliveryProfile.objects.filter(is_approved=False),
        'active_tab': 'approvals'
    }
    return render(request, 'dashboard/admin_approvals.html', context)

@login_required
@user_passes_test(is_admin)
def admin_orders(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'assign_delivery':
            order = get_object_or_404(Order, id=request.POST.get('order_id'))
            agent = get_object_or_404(DeliveryProfile, id=request.POST.get('agent_id'))
            DeliveryAssignment.objects.update_or_create(
                order=order,
                defaults={'agent': agent, 'status': 'assigned'}
            )
        return redirect('dashboard:admin_orders')

    context = {
        'all_orders': Order.objects.exclude(status='cart').order_by('-created_at'),
        'delivery_agents': DeliveryProfile.objects.filter(is_approved=True),
        'active_tab': 'orders'
    }
    return render(request, 'dashboard/admin_orders.html', context)

@login_required
@user_passes_test(is_admin)
def admin_users(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        user_id = request.POST.get('id')
        user_obj = get_object_or_404(User, id=user_id)
        
        if action == 'delete_user':
            user_obj.delete()
            messages.success(request, f"User {user_obj.username} has been successfully deleted.")
        elif action == 'block_user':
            user_obj.is_active = False
            user_obj.save()
            messages.warning(request, f"User {user_obj.username} has been temporarily blocked.")
        elif action == 'unblock_user':
            user_obj.is_active = True
            user_obj.save()
            messages.success(request, f"User {user_obj.username} has been unblocked.")
            
        return redirect('dashboard:admin_users')

    context = {
        'all_users': User.objects.all(),
        'active_tab': 'users'
    }
    return render(request, 'dashboard/admin_users.html', context)

@login_required
@user_passes_test(is_admin)
def admin_sellers(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'revoke_seller':
            seller_id = request.POST.get('id')
            seller = get_object_or_404(SellerProfile, id=seller_id)
            seller.is_approved = False
            seller.save()
            messages.warning(request, f"Approval revoked for {seller.shop_name}.")
        return redirect('dashboard:admin_sellers')

    context = {
        'approved_sellers': SellerProfile.objects.filter(is_approved=True),
        'active_tab': 'sellers'
    }
    return render(request, 'dashboard/admin_sellers.html', context)
