# Fichier : ql_web_app/basics/urls.py (VERSION FINALE ET COMPLÈTE)

from django.urls import path, include
from . import views

# L'espace de nom pour cette catégorie
app_name = 'basics'

urlpatterns = [
    # URL de la page d'accueil de la catégorie -> /basics/
    path('', views.home, name='home'),
    
    # =====================================================================
    # C'EST ICI QUE SE TROUVE LA CORRECTION :
    # On ajoute les chemins pour chaque chapitre listé dans le Cookbook
    # =====================================================================
    path('quantlib-basics/', include('interactive_basics.urls'), name='quantlib_basics'),
    path('quantlib-basics/', views.quantlib_basics_view, name='quantlib_basics'),
    path('instruments-engines/', views.instruments_engines_view, name='instruments_engines'),
    path('numerical-greeks/', views.numerical_greeks_view, name='numerical_greeks'),
    path('market-quotes/', views.market_quotes_view, name='market_quotes'),
    path('term-structures/', views.term_structures_view, name='term_structures'),
    path('pricing-over-range/', views.pricing_over_range_view, name='pricing_over_range'),
    path('random-numbers/', views.random_numbers_view, name='random_numbers'),
]