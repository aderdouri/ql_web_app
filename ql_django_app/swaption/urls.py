# Fichier : ql_web_app/swaption/urls.py

from django.urls import path
from . import views

# Déclare l'espace de nom pour cette application
app_name = 'swaption'

# C'EST CETTE LISTE QUI MANQUAIT PROBABLEMENT À VOTRE FICHIER
urlpatterns = [
    # Chemin vide, qui correspond à l'URL /rates/swaption/
    # Assurez-vous que le nom de la vue (ici 'pricer_view') existe bien dans swaption/views.py
    path('', views.pricer_view, name='pricer'),
]