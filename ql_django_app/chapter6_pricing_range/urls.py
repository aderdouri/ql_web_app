from django.urls import path
from . import views

app_name = 'chapter6_pricing_range'

urlpatterns = [
    path('', views.pricing_range_lab_view, name='pricing_range_lab'),
    path('api/calculate/', views.calculate_pricing_range_api, name='calculate_pricing_range_api'),
]