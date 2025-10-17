from django.urls import path, include
from . import views

# On déclare l'espace de nom pour cette catégorie
app_name = 'equity_models'

urlpatterns = [
    # Page d'accueil de la catégorie
    path('', views.home, name='home'),
    
    # Chapter 21: Heston Option Pricer
    path('heston-option-pricer/', include('chapter21_heston_option.urls')),
    
    # Chapter 22: Volatility Smile and Heston Model Calibration
    path('volatility-smile-heston-calibration/', include('chapter22_heston_calibration.urls')),
    
    # Chapter 23: Heston Parameter Calibration
    path('heston-calibration-scipy/', include('chapter23_heston_parameter_calibration.urls')),
    
    # Chapter 24: European and American Options
    path('european-american-options/', include('chapter24_european_american_options.urls')),
    
    # Chapter 25: Black Formula for Commodity Futures Options
    path('black-formula-futures/', include('chapter25_black_formula_futures.urls')),
    
    # Chapter 26: Defining Rho for the Black Process
    path('defining-rho/', include('chapter26_defining_rho.urls')),
    
    # Chapter 27: Day-Count Conventions
    path('day-count-conventions/', include('chapter27_day_count_conventions.urls')),
    
    # Lien vers la page (pour l'instant statique) de valorisation des options
    path('valuing-european-american-options/', views.valuing_options_view, name='valuing_options'),
    
]