from django.db import models
from orders.models import Order

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=(('pending', 'Pending'), ('completed', 'Completed')), default='pending')
    method = models.CharField(max_length=20, choices=(('online', 'Online'), ('cod', 'COD')), default='online')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment #{self.id} for Order #{self.order.id}"
