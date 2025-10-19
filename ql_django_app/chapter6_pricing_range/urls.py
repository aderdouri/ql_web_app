from django.urls import path
from .views import price_history_lab_view

app_name = 'pricing_over_range'

urlpatterns = [
    path('lab/', price_history_lab_view, name='lab'),
]