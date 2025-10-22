from django.urls import path, include
from . import views

# L'espace de nom principal pour cette catégorie
app_name = 'interest_rate_curves'

urlpatterns = [
    path('', views.home, name='home'),
  
    path('eonia-curve-bootstrapping/', include(('chapter8_eonia_curve.urls', 'chapter8_eonia_curve'))),
    
    path('euribor-curve-bootstrapping/', include(('chapter9_euribor_curve.urls', 'chapter9_euribor_curve'))),
    
    path('constructing-a-yield-curve/', include(('chapter14_yield_curve.urls', 'chapter14_yield_curve'))),
    
    path('dangerous-day-count-conventions/', include(('chapter_day_count.urls', 'chapter_day_count'))),
    
    path('implied-term-structures/', include(('chapter12_implied_curve.urls', 'chapter12_implied_curve'))),
    
    path('glitch-in-forward-rate-curves/', include(('chapter11_glitch_curve.urls', 'chapter11_glitch_curve'))),

    path('interest-rate-sensitivities/', include('chapter13_sensitivities.urls')),]