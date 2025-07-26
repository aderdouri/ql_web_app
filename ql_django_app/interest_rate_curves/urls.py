from django.urls import path, include
from . import views

# On déclare l'espace de nom pour cette catégorie
app_name = 'interest_rate_curves'

urlpatterns = [
    # Page d'accueil de la catégorie
    path('', views.home, name='home'),
    
    # --- URLs pour chaque chapitre ---
    
    # Chapitre EONIA : On inclut l'application interactive
    path('eonia-curve-bootstrapping/', include('chapter_eonia_curve.urls')),
    
    # Chapitre Euribor : Pointeur vers une vue statique
    path('euribor-curve-bootstrapping/', include('chapter_euribor_curve.urls')),
    
    # Chapitre Treasury Curve : On inclut l'application interactive
    path('constructing-a-yield-curve/', include('chapter10_treasury_curve.urls')),
    
    # Le reste des chapitres pointe vers des vues statiques
    path('dangerous-day-count-conventions/', views.dangerous_day_count_view, name='dangerous_day_count'),
    
    path('implied-term-structures/', views.implied_term_structures_view, name='implied_term_structures'),
    
    path('interest-rate-sensitivities/', views.sensitivities_view, name='sensitivities'),
    
    path('glitch-in-forward-rate-curves/', views.glitch_forward_curves_view, name='glitch_forward_curves'),
]