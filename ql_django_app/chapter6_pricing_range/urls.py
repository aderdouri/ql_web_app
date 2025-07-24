from django.urls import path
from . import views

app_name = 'chapter6_pricing_range'
urlpatterns = [
    path('', views.price_history_lab_view, name='price_history_lab'),
]