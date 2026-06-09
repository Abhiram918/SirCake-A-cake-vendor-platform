from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('seller', 'Seller'),
        ('delivery', 'Delivery Agent'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')

    def __str__(self):
        return self.username



class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - Customer"

class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    shop_name = models.CharField(max_length=100)
    shop_description = models.TextField(blank=True, null=True)
    shop_logo = models.ImageField(upload_to='shops/logos/', blank=True, null=True)
    shop_banner = models.ImageField(upload_to='shops/banners/', blank=True, null=True)
    shop_slug = models.SlugField(unique=True, blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        if not self.shop_slug and self.shop_name:
            self.shop_slug = slugify(self.shop_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.shop_name} ({self.user.username})"

class DeliveryProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='delivery_profile')
    vehicle_details = models.CharField(max_length=100, blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - Delivery"

class Address(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='addresses')
    full_name = models.CharField(max_length=100)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name}, {self.city} ({self.pincode})"

# Signals to auto-create profiles
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'customer':
            CustomerProfile.objects.create(user=instance)
        elif instance.role == 'seller':
            SellerProfile.objects.create(user=instance)
        elif instance.role == 'delivery':
            DeliveryProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.role == 'customer' and hasattr(instance, 'customer_profile'):
        instance.customer_profile.save()
    elif instance.role == 'seller' and hasattr(instance, 'seller_profile'):
        instance.seller_profile.save()
    elif instance.role == 'delivery' and hasattr(instance, 'delivery_profile'):
        instance.delivery_profile.save()

