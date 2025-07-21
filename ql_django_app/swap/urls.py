# Fichier : ql_web_app/swap/urls.py
from django.urls import path
from . import views

app_name = 'swap'

urlpatterns = [
    # Utilise notre nouvelle vue standardisée 'pricer_view'
    path('', views.pricer_view, name='pricer'),
]