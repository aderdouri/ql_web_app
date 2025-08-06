from django.urls import path, include
from . import views

app_name = 'interest_rate_models'

urlpatterns = [
    # Page d'accueil de la catégorie
    path('', views.home, name='home'),
    
    # --- URLs pour chaque chapitre ---
     path('hull-white-simulation/', include('chapter_hull_white.urls')),
    path('short-rate-calibration/', views.short_rate_calibration_view, name='short_rate_calibration'),
    
    # On connecte l'application 'swap' à ce chapitre
    path('interest-rate-swaps/', include('swap.urls')),
    
    path('caps-floors/', include('chapter_caps_floors.urls')),
    path('heston-option/', views.heston_option_view, name='heston_option'),
    path('heston-calibration/', include('chapter_heston_calibration.urls')),]