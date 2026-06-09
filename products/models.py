from django.db import models
from django.utils.text import slugify
from accounts.models import User, SellerProfile

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Cake(models.Model):
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='cakes')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='cakes')
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    flavor = models.CharField(max_length=100, blank=True, null=True)
    weight = models.CharField(max_length=50, help_text="e.g., 1kg, 500g")
    image = models.ImageField(upload_to='cakes/') # Primary image
    is_eggless = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    stock_quantity = models.PositiveIntegerField(default=10)
    customization_options = models.TextField(blank=True, null=True, help_text="List available options")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} by {self.seller.shop_name}"

class CakeImage(models.Model):
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE, related_name='additional_images')
    image = models.ImageField(upload_to='cakes/gallery/')
    is_feature = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.cake.name}"


class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items')
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE, related_name='wishlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'cake')
        verbose_name = "Wishlist Item"
        verbose_name_plural = "Wishlist Items"

    def __str__(self):
        return f"{self.user.username} - {self.cake.name}"
