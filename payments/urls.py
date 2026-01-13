from django.urls import path
from .views import home, register, pay, success, history
urlpatterns = [path('',home,name='home'),path('register/',register,name='register'),path('pay/<int:merchant_id>/',pay,name='pay'),path('success/',success,name='success'),path('history/',history,name='history')]
