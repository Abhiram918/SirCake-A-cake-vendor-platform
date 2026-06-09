from django.urls import path
from . import views

app_name = 'sellers'

urlpatterns = [
    # Public Shop URLs
    path('shops/', views.ShopListView.as_view(), name='shop_list'),
    path('shops/<slug:slug>/', views.ShopDetailView.as_view(), name='shop_detail'),
    
    # Seller Dashboard & Management
    path('seller/dashboard/', views.SellerDashboardView.as_view(), name='dashboard'),
    path('seller/profile/', views.SellerProfileUpdateView.as_view(), name='profile_edit'),
    path('seller/cakes/', views.SellerCakeListView.as_view(), name='cake_list'),
    path('seller/cakes/add/', views.SellerCakeCreateView.as_view(), name='cake_create'),
    path('seller/cakes/edit/<int:pk>/', views.SellerCakeUpdateView.as_view(), name='cake_update'),
    path('seller/cakes/delete/<int:pk>/', views.SellerCakeDeleteView.as_view(), name='cake_delete'),
    
    # Sub-order management
    path('seller/orders/', views.SellerOrderListView.as_view(), name='order_list'),
    path('seller/orders/update-item/<int:pk>/', views.SellerOrderItemUpdateView.as_view(), name='order_item_update'),
]
