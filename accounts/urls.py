from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/customer/', views.register_customer, name='register_customer'),
    path('register/seller/', views.register_seller, name='register_seller'),
    path('register/delivery/', views.register_delivery, name='register_delivery'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('addresses/', views.address_list_view, name='address_list'),
    path('addresses/add/', views.address_create_view, name='address_create'),
    path('addresses/delete/<int:pk>/', views.address_delete_view, name='address_delete'),
]
