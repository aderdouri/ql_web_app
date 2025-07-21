from django.urls import path
from . import views

# Vérifiez que cette ligne est bien présente et correctement écrite
app_name = 'american_option'

urlpatterns = [
    # Vérifiez que le chemin est bien vide ('') et que le nom est bien 'pricer'
    # ATTENTION : Remplacez "pricer_view" par le vrai nom de votre vue dans american_option/views.py
    path('', views.pricer_view, name='pricer'), 
]