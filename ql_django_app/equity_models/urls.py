# Fichier : ql_web_app/equity_models/urls.py (NOUVEAU FICHIER)

from django.urls import path, include
from . import views

# On déclare l'espace de nom pour cette catégorie
app_name = 'equity_models'

urlpatterns = [
    # Page d'accueil de la catégorie
    path('', views.home, name='home'),
    
    # --- On inclut les applications de chapitre qui appartiennent à cette catégorie ---
    
    path('heston-option-pricer/', include('chapter_heston_option.urls')),
    
    path('heston-calibration/', include('chapter_heston_calibration.urls')),
    
    # Lien vers la page (pour l'instant statique) de valorisation des options
    path('valuing-european-american-options/', views.valuing_options_view, name='valuing_options'),
    
    # Vous ajouterez les autres chapitres ici
]