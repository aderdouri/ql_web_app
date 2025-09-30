from django.urls import path, include
from . import views
from . import chapter_views

# On déclare l'espace de nom pour cette catégorie
app_name = 'basics'

urlpatterns = [
    # Page d'accueil de la catégorie -> /basics/
    path('', views.home, name='home'),
    
    # --- On inclut une application dédiée pour chaque chapitre interactif ---
    
    path('quantlib-basics/', include('interactive_basics.urls')),
    
    # Chapter pages
    path('chapter1/', chapter_views.chapter1_quantlib_basics, name='chapter1'),
    path('chapter2/', chapter_views.chapter2_instruments, name='chapter2'),    
    path('chapter4/', chapter_views.chapter4_quotes, name='chapter4'),
    path('chapter5/', chapter_views.chapter5_curves, name='chapter5'),
    path('chapter6/', chapter_views.chapter6_pricing_range, name='chapter6'),
    path('chapter7/', chapter_views.chapter7_random, name='chapter7'),
    
    # Interactive labs
    path('quotes/', chapter_views.chapter4_quotes, name='quotes'),
    
    path('market-quotes/', include('chapter4_quotes.urls')),
    
    path('term-structures/', include('chapter5_curves.urls')),
    
    path('pricing-over-range/', include('chapter6_pricing_range.urls')),
    
    path('random-numbers/', include('chapter7_random.urls')),
]