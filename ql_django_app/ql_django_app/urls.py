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
    path('chapter5-curves/', include('chapter5_curves.urls')),
    path('chapter6-pricing-range/', include('chapter6_pricing_range.urls')),
    path('chapter7-random/', include('chapter7_random.urls')),
    path('interest-rate-curves/', include('interest_rate_curves.urls')),
    path('interest-rate-models/', include('interest_rate_models.urls')),
    path('equity-models/', include('equity_models.urls')),
    path('bonds/', include('bonds.urls')),
    path('chapter-heston-calibration/', include('chapter22_heston_calibration.urls')),
    path('chapter17-calibration/', include('chapter17_calibration.urls')),
    path('chapter18-par-indexed-coupons/', include('chapter18_par_indexed_coupons.urls')),
    path('chapter33-floating-duration/', include('chapter33_floating_duration.urls')),
    path('chapter34-treasury-futures/', include('chapter34_treasury_futures.urls')),
    path('chapter35-pricing-conventions/', include('chapter35_pricing_conventions.urls')),
    path('chapter36-more-conventions/', include('chapter36_more_conventions.urls')),
]