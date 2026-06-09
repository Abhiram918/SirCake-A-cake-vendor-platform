from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Sum, Count, Avg
from accounts.models import SellerProfile
from products.models import Cake
from orders.models import OrderItem, Order
from .forms import SellerProfileForm, SellerCakeForm
from django.contrib import messages

# Permissions
class ApprovedSellerMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'seller' and hasattr(self.request.user, 'seller_profile') and self.request.user.seller_profile.is_approved

    def handle_no_permission(self):
        if self.request.user.is_authenticated and self.request.user.role == 'seller':
            return render(self.request, 'dashboard/not_approved.html')
        return super().handle_no_permission()

# Public Views
class ShopListView(ListView):
    model = SellerProfile
    template_name = 'sellers/shop_list.html'
    context_object_name = 'shops'
    queryset = SellerProfile.objects.filter(is_approved=True)

class ShopDetailView(DetailView):
    model = SellerProfile
    template_name = 'sellers/shop_detail.html'
    context_object_name = 'shop'
    slug_field = 'shop_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cakes'] = self.object.cakes.filter(is_available=True)
        # Calculate analytics for public view
        avg_rating = self.object.cakes.aggregate(Avg('reviews__rating'))['reviews__rating__avg'] or 0
        total_reviews = self.object.cakes.aggregate(Count('reviews'))['reviews__count'] or 0
        context['avg_rating'] = round(avg_rating, 1)
        context['total_reviews'] = total_reviews
        return context

# Dashboard & Analytics
class SellerDashboardView(ApprovedSellerMixin, TemplateView):
    template_name = 'sellers/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seller = self.request.user.seller_profile
        my_cakes = seller.cakes.all()
        my_items = OrderItem.objects.filter(cake__seller=seller)
        
        # Analytics
        revenue = my_items.aggregate(total=Sum('price'))['total'] or 0 # Simplification: sum of price * quantity
        # Fix revenue calculation:
        revenue = sum(item.price * item.quantity for item in my_items)
        
        avg_rating = my_cakes.aggregate(Avg('reviews__rating'))['reviews__rating__avg'] or 0
        
        context.update({
            'total_revenue': revenue,
            'avg_rating': round(avg_rating, 1),
            'cake_count': my_cakes.count(),
            'order_count': my_items.values('order').distinct().count(),
            'recent_orders': my_items.select_related('order', 'order__customer').order_by('-order__created_at')[:5],
            'status_summary': list(my_items.values('status').annotate(count=Count('id'))),
        })
        return context

# Profile Management
class SellerProfileUpdateView(ApprovedSellerMixin, UpdateView):
    model = SellerProfile
    form_class = SellerProfileForm
    template_name = 'sellers/profile_edit.html'
    success_url = reverse_lazy('sellers:dashboard')

    def get_object(self, queryset=None):
        return self.request.user.seller_profile

# Cake Management
class SellerCakeListView(ApprovedSellerMixin, ListView):
    model = Cake
    template_name = 'sellers/cake_list.html'
    context_object_name = 'cakes'

    def get_queryset(self):
        return Cake.objects.filter(seller=self.request.user.seller_profile)

class SellerCakeCreateView(ApprovedSellerMixin, CreateView):
    model = Cake
    form_class = SellerCakeForm
    template_name = 'sellers/cake_form.html'
    success_url = reverse_lazy('sellers:cake_list')

    def form_valid(self, form):
        form.instance.seller = self.request.user.seller_profile
        messages.success(self.request, "Cake listing created successfully!")
        return super().form_valid(form)

class SellerCakeUpdateView(ApprovedSellerMixin, UpdateView):
    model = Cake
    form_class = SellerCakeForm
    template_name = 'sellers/cake_form.html'
    success_url = reverse_lazy('sellers:cake_list')

    def get_queryset(self):
        return Cake.objects.filter(seller=self.request.user.seller_profile)

class SellerCakeDeleteView(ApprovedSellerMixin, DeleteView):
    model = Cake
    template_name = 'sellers/cake_confirm_delete.html'
    success_url = reverse_lazy('sellers:cake_list')

    def get_queryset(self):
        return Cake.objects.filter(seller=self.request.user.seller_profile)

# Order & Sub-order Management
class SellerOrderListView(ApprovedSellerMixin, ListView):
    template_name = 'sellers/order_list.html'
    context_object_name = 'order_items'

    def get_queryset(self):
        return OrderItem.objects.filter(cake__seller=self.request.user.seller_profile).select_related('order', 'cake', 'order__customer').order_by('-order__created_at')

class SellerOrderItemUpdateView(ApprovedSellerMixin, UpdateView):
    model = OrderItem
    fields = ['status']
    template_name = 'sellers/order_item_form.html'
    success_url = reverse_lazy('sellers:order_list')

    def get_queryset(self):
        return OrderItem.objects.filter(cake__seller=self.request.user.seller_profile)
        
    def dispatch(self, request, *args, **kwargs):
        # We need to catch the object to check its order status before displaying the form or processing POST
        try:
            item = self.get_object()
            if item.order.status == 'delivered' or getattr(item.order, 'delivery_assignment', None) and item.order.delivery_assignment.status == 'delivered':
                messages.error(request, "This order has been delivered. Status cannot be updated anymore.")
                return redirect('sellers:order_list')
        except Exception:
            pass # Let the standard dispatch handle 404s
            
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Sync parent order status
        order = self.object.order
        items = order.items.all()
        statuses = [item.status for item in items]
        
        # We don't want to override statuses managed by delivery (like out_for_delivery, delivered)
        # unless all items are somehow delivered.
        if order.status not in ['picked_up', 'out_for_delivery', 'delivered']:
            if all(s == 'delivered' for s in statuses):
                order.status = 'delivered'
            elif all(s in ['ready', 'delivered'] for s in statuses):
                order.status = 'ready'
            elif any(s == 'baking' for s in statuses):
                order.status = 'baking'
            elif any(s in ['accepted', 'baking', 'ready'] for s in statuses):
                order.status = 'accepted'
            
            order.save()
            
        messages.success(self.request, f"Status updated to {self.object.get_status_display()}")
        return response
