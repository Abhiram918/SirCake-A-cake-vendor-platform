from django.contrib import admin
from .models import Category, Cake, CakeImage

class CakeImageInline(admin.TabularInline):
    model = CakeImage
    extra = 3

@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'seller', 'price', 'is_available']
    list_filter = ['category', 'is_available', 'is_eggless']
    search_fields = ['name', 'description']
    inlines = [CakeImageInline]

admin.site.register(Category)
admin.site.register(CakeImage)
