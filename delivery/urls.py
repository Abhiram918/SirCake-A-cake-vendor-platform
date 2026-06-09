from django.urls import path
from . import views

app_name = 'delivery'

urlpatterns = [
    path('', views.delivery_dashboard, name='dashboard'),
    path('history/', views.delivery_history, name='history'),
]
