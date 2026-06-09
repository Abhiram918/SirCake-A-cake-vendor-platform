from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ['cake', 'quantity', 'price', 'custom_message', 'flavor_choice']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'status', 'total_amount', 'delivery_date', 'delivery_slot', 'created_at']
    list_filter = ['status', 'delivery_date', 'delivery_slot', 'created_at']
    search_fields = ['customer__username', 'id']
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'cake', 'quantity', 'price', 'custom_message', 'flavor_choice']
