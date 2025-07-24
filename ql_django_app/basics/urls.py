from django.urls import path, include
from . import views

app_name = 'basics'

urlpatterns = [
    path('', views.home, name='home'),
    
    path('quantlib-basics/', include('interactive_basics.urls'), name='quantlib_basics'),
   # Chapitre 1 : QuantLib basics (page statique pour l'instant)
    path('quantlib-basics/', views.quantlib_basics_view, name='quantlib_basics'),

# Chapitre 2 : Instruments and pricing engines (rendu interactif par l'app 'chapter2_instruments')
    path('instruments-engines/', include('chapter2_instruments.urls', namespace='instruments_engines')),
    path('numerical-greeks/', include('chapter3_greeks.urls', namespace='numerical_greeks')),
    path('market-quotes/', include('chapter4_quotes.urls', namespace='market_quotes')),
    path('numerical-greeks/', views.numerical_greeks_view, name='numerical_greeks'),
    path('term-structures/', include('chapter5_curves.urls', namespace='term_structures')),
    path('pricing-over-range/', include('chapter6_pricing_range.urls', namespace='pricing_over_range')),
    path('random-numbers/', include('chapter7_random.urls', namespace='random_numbers')),
    path('market-quotes/', views.market_quotes_view, name='market_quotes'),
    path('term-structures/', views.term_structures_view, name='term_structures'),
    path('pricing-over-range/', views.pricing_over_range_view, name='pricing_over_range'),
    path('random-numbers/', views.random_numbers_view, name='random_numbers'),
]