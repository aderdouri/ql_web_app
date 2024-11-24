from django.urls import path
from . import views

app_name = 'swap'

urlpatterns = [
    path('price/', views.price_swap, name='price_swap'),
]