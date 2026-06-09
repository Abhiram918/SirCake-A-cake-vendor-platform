from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.cake_list, name='cake_list'),
    path('add/', views.cake_create, name='cake_create'),
    path('<int:pk>/', views.cake_detail, name='cake_detail'),
    path('<int:pk>/edit/', views.cake_update, name='cake_update'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/toggle/<int:cake_id>/', views.toggle_wishlist, name='toggle_wishlist'),
]
