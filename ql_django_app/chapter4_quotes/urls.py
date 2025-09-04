# chapter4_quotes/urls.py (VERSION FINALE ET COMPLÈTE)

from django.urls import path
from .views import market_lab_view

app_name = 'chapter4_quotes'

urlpatterns = [
    path('market-lab/', market_lab_view, name='market_lab'),
]