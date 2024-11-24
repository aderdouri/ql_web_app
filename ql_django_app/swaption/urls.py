from django.urls import path
from . import views

app_name = 'swaption'

urlpatterns = [
    path('price/', views.price_swaption, name='price_swaption'),
]