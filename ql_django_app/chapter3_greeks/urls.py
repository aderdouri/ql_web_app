# chapter3_greeks/urls.py (VERSION FINALE ET COMPLÈTE)

from django.urls import path
from .views import greeks_lab_view

app_name = 'chapter3_greeks'

urlpatterns = [
    path('greeks-lab/', greeks_lab_view, name='greeks_lab'),
]