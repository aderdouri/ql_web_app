from django.urls import path
from . import views

app_name = 'chapter28_fixed_rate_bonds'

urlpatterns = [
    path('description/', views.description, name='description'),
    path('lab/', views.lab, name='lab'),
    path('api/calculate-price/', views.calculate_bond_price_api, name='calculate_price_api'),
    path('api/calculate-sensitivity/', views.calculate_sensitivity_api, name='calculate_sensitivity_api'),
]
