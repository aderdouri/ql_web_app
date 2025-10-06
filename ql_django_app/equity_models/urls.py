from django.urls import path, include
from . import views

# On déclare l'espace de nom pour cette catégorie
app_name = 'equity_models'

urlpatterns = [
    # Page d'accueil de la catégorie
    path('', views.home, name='home'),
    
    # Chapter 21: Heston Option Pricer
    path('heston-option-pricer/', include('chapter_heston_option.urls')),
    
    # Chapter 22: Volatility Smile and Heston Model Calibration
    # path('volatility-smile-heston-calibration/', volatility_smile_views.volatility_smile_description_view, name='volatility_smile_description'),
    # path('volatility-smile-heston-calibration/lab/', volatility_smile_views.volatility_smile_lab_view, name='volatility_smile_lab'),
    
    # Chapter 23: Heston Parameter Calibration
    path('heston-parameter-calibration/', include('chapter_heston_calibration.urls')),
    
    # Chapter 24: European and American Options
    path('european-american-options/', include('chapter_european_american_options.urls')),
    
    # Chapter 25: Commodity Futures Options
    path('commodity-futures-options/', include('chapter_commodity_futures_options.urls')),
    
    # Chapter 26: Black Process Rho
    path('black-process-rho/', include('chapter_black_process_rho.urls')),
    
    # Chapter 27: Day-Count Conventions
    path('day-count-conventions/', include('chapter_day_count_conventions.urls')),
    
    # Lien vers la page (pour l'instant statique) de valorisation des options
    path('valuing-european-american-options/', views.valuing_options_view, name='valuing_options'),
    
]