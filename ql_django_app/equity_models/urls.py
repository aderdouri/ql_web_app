from django.urls import path, include
from . import views

# On déclare l'espace de nom pour cette catégorie
app_name = 'equity_models'

urlpatterns = [
    # Page d'accueil de la catégorie
    path('', views.home, name='home'),
    
    path('heston-option-pricer/', include('chapter_heston_option.urls')),
    
    path('heston-calibration/', include('chapter_heston_calibration.urls')),
    
    # Lien vers la page (pour l'instant statique) de valorisation des options
    path('valuing-european-american-options/', views.valuing_options_view, name='valuing_options'),
    
]