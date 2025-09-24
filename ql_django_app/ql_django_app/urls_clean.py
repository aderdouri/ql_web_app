from django.contrib import admin
from django.urls import path, include
from . import views as home_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_views.home, name='home'),

    # On ne garde QUE les catégories qui existent et sont configurées
    path('basics/', include('basics.urls')),
    path('basics/', include('interactive_basics.urls')),
    path('chapter2-instruments/', include('chapter2_instruments.urls')),
    path('chapter3-numerical-greeks/', include('chapter3_numerical_greeks.urls')),
    path('chapter4-quotes/', include('chapter4_quotes.urls')),
    path('interest-rate-curves/', include('interest_rate_curves.urls')),
    path('interest-rate-models/', include('interest_rate_models.urls')),
    path('equity-models/', include('equity_models.urls')),
]
