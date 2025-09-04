from django.urls import path, include
from . import views

# On déclare l'espace de nom pour cette catégorie
app_name = 'basics'

urlpatterns = [
    # Page d'accueil de la catégorie -> /basics/
    path('', views.home, name='home'),
    
    # --- On inclut une application dédiée pour chaque chapitre interactif ---
    
    path('quantlib-basics/', include('interactive_basics.urls')),
    
    path('chapter2/', include('chapter2_instruments.urls', namespace='chapter2_instruments')),    
    path('numerical-greeks/', include('chapter3_greeks.urls')),
    
    path('market-quotes/', include('chapter4_quotes.urls')),
    
    path('term-structures/', include('chapter5_curves.urls')),
    
    path('pricing-over-range/', include('chapter6_pricing_range.urls')),
    
    path('random-numbers/', include('chapter7_random.urls')),
]