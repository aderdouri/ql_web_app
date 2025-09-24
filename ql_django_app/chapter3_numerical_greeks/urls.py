# chapter3_numerical_greeks/urls.py

from django.urls import path
from . import views

app_name = 'chapter3_numerical_greeks'

urlpatterns = [
    path('', views.greeks_lab_view, name='greeks_lab'),
    path('simple/', views.simple_greeks_lab_view, name='simple_greeks_lab'),
    path('api/calculate-greeks/', views.calculate_greeks_api, name='calculate_greeks_api'),
    path('api/price-series/', views.price_series_api, name='price_series_api'),
    path('api/chart-data/', views.chart_data_api, name='chart_data_api'),
]
