from django.urls import path, include
from . import views
from chapter_eonia_curve import views as eonia_views
from chapter_euribor_curve import views as euribor_views
from chapter10_treasury_curve import views as treasury_views
from chapter_day_count import views as day_count_views
from chapter_implied_curve import views as implied_views
from chapter_glitch_curve import views as glitch_views
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
    path('dangerous-day-count-conventions/', include('chapter_day_count.urls')),
    
    path('implied-term-structures/', include('chapter_implied_curve.urls')),
    
     path(
        'glitch-in-forward-rate-curves/', 
        include(('chapter_glitch_curve.urls', 'chapter_glitch_curve'))
    ),
     path('interest-rate-sensitivities/', include('chapter_sensitivities.urls')),]