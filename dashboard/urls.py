from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('customer/', views.customer_dashboard, name='customer'),
    path('admin/', views.admin_approvals, name='admin_approvals'),
    path('admin/orders/', views.admin_orders, name='admin_orders'),
    path('admin/users/', views.admin_users, name='admin_users'),
    path('admin/sellers/', views.admin_sellers, name='admin_sellers'),
]
