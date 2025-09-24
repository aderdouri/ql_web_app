# chapter2_instruments/urls.py

from django.urls import path
from . import views

app_name = 'chapter2_instruments'

urlpatterns = [
    path('pricer-lab/', views.pricer_lab_view, name='pricer_lab'),
    path('api/calculate-price/', views.calculate_option_price_api, name='calculate_price_api'),
    path('api/price-series/', views.calculate_price_series_api, name='price_series_api'),
    path('api/volatility-series/', views.calculate_volatility_series_api, name='volatility_series_api'),
    path('api/time-decay-series/', views.calculate_time_decay_series_api, name='time_decay_series_api'),
    path('api/compare-engines/', views.compare_engines_api, name='compare_engines_api'),
]