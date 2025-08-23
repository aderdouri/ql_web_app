from django.urls import path
from . import views

app_name = 'european_option'

urlpatterns = [
    
    path('', views.price_european_option, name='pricer'),
]