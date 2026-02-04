from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pay/<int:merchant_id>/', views.pay, name='pay'),
    path('success/', views.success, name='success'),
    path('history/', views.history, name='history'),
    path('register/', views.register, name='register'),
]
