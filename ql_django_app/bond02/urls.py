from django.urls import path
from . import views

app_name = 'bond02'

urlpatterns = [
    path('price/', views.price_bond, name='price_bond'),
]