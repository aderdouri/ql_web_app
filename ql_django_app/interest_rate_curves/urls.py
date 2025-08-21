# Fichier : ql_web_app/interest_rate_curves/urls.py (VERSION FINALE AVEC NAMESPACES IMBRIQUÉS)

from django.urls import path, include
from . import views

# L'espace de nom principal pour cette catégorie
app_name = 'interest_rate_curves'

urlpatterns = [
    path('', views.home, name='home'),
    
    # ==============================================================================
    # On utilise un tuple (url_config, app_name) pour chaque include
    # afin de créer un sous-espace de nom.
    # ==============================================================================
    path('eonia-curve-bootstrapping/', include(('chapter_eonia_curve.urls', 'chapter_eonia_curve'))),
    
    path('euribor-curve-bootstrapping/', include(('chapter_euribor_curve.urls', 'chapter_euribor_curve'))),
    
    path('constructing-a-yield-curve/', include(('chapter_yield_curve.urls', 'chapter_yield_curve'))),
    
    path('dangerous-day-count-conventions/', include(('chapter_day_count.urls', 'chapter_day_count'))),
    
    path('implied-term-structures/', include(('chapter_implied_curve.urls', 'chapter_implied_curve'))),
    
    # Et surtout pour celui qui causait l'erreur
    path('glitch-in-forward-rate-curves/', include(('chapter_glitch_curve.urls', 'chapter_glitch_curve'))),

    # Les chapitres statiques ne changent pas
    path('interest-rate-sensitivities/', include('chapter_sensitivities.urls')),]