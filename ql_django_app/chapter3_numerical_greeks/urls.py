"""
Chapter 3 - Numerical Greeks calculation URLs
"""
from django.urls import path
from . import views

app_name = 'chapter3_numerical_greeks'

urlpatterns = [
    path('', views.greeks_lab_view, name='greeks_lab'),
    path('api/numerical-greeks-lab/', views.numerical_greeks_lab_api, name='numerical_greeks_lab_api'),
]