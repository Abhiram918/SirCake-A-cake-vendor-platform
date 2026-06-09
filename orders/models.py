from django.db import models
from accounts.models import User, Address
from products.models import Cake

class Order(models.Model):
    STATUS_CHOICES = (
        ('cart', 'Cart'),
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('baking', 'Baking'),
        ('ready', 'Ready for pickup'),
        ('picked_up', 'Picked up'),
        ('out_for_delivery', 'Out for delivery'),
        ('delivered', 'Delivered'),
    )
    DELIVERY_SLOTS = (
        ('morning', 'Morning (8 AM - 12 PM)'),
        ('afternoon', 'Afternoon (12 PM - 4 PM)'),
        ('evening', 'Evening (4 PM - 8 PM)'),
        ('night', 'Night (8 PM - 11 PM)'),
    )
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_method = models.CharField(max_length=20, choices=(('online', 'Online'), ('cod', 'COD')), default='online')
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    delivery_date = models.DateField(null=True, blank=True)
    delivery_slot = models.CharField(max_length=20, choices=DELIVERY_SLOTS, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.customer.username}"

class OrderItem(models.Model):
    ITEM_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('baking', 'Baking'),
        ('ready', 'Ready for pickup'),
        ('delivered', 'Delivered'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    cake = models.ForeignKey(Cake, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    custom_message = models.CharField(max_length=255, blank=True, null=True, help_text="Message on Cake")
    flavor_choice = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=ITEM_STATUS_CHOICES, default='pending')

    def __str__(self):
        cake_name = self.cake.name if self.cake else 'Deleted Cake'
        return f"{self.quantity} x {cake_name} ({self.status})"

