from django.urls import path, include
from . import views

# L'espace de nom pour cette catégorie
app_name = 'interest_rate_models'

urlpatterns = [
    # Page d'accueil de la catégorie
    path('', views.home, name='home'),
    
    # --- Chapitres Interactifs de cette Section (15, 17, 19, 20) ---
    
    # Chapitre 15: Simulating interest rates using Hull White model
    path('simulating-hull-white/', include('chapter_hull_white.urls')),
    
    # Chapitre 17: Short interest rate model calibration
    path('short-rate-calibration/', include('chapter_calibration.urls')),
    
    # Chapitre 19: Modeling interest rate swaps (utilise l'application 'swap')
    path('modeling-swaps/', include('swap.urls')),
    
    # Chapitre 20: Caps and floors
    path('caps-and-floors/', include('chapter_caps_floors.urls')),

    # --- Chapitres Statiques/Explicatifs de cette Section (16, 18) ---
    
    # Chapitre 16: Thoughts on convergence...
    path('hull-white-convergence/', include('chapter_mc_convergence.urls')),
    
    # Chapitre 18: Par versus indexed coupons
    path('par-vs-indexed-coupons/', include('chapter_par_vs_indexed.urls')),
]