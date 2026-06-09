from django.db import models
from accounts.models import DeliveryProfile
from orders.models import Order

class DeliveryAssignment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='delivery_assignment')
    agent = models.ForeignKey(DeliveryProfile, on_delete=models.CASCADE, related_name='deliveries')
    STATUS_CHOICES = (
        ('assigned', 'Assigned'),
        ('picked_up', 'Picked Up'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='assigned')
    assigned_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order #{self.order.id} -> {self.agent.user.username}"
