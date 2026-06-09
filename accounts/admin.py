from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, CustomerProfile, SellerProfile, DeliveryProfile, Address

admin.site.register(User, UserAdmin)
admin.site.register(CustomerProfile)
admin.site.register(SellerProfile)
admin.site.register(DeliveryProfile)
admin.site.register(Address)
