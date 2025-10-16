from django.urls import path, include
from . import views

app_name = 'bonds'

urlpatterns = [
    path('', views.home, name='home'),
    path('chapter28-fixed-rate-bonds/', include('chapter28_fixed_rate_bonds.urls')),
    path('chapter29-irregular-bonds/', include('chapter29_irregular_bonds.urls')),
    path('chapter30-credit-spreads/', include('chapter30_credit_spreads.urls')),
    path('chapter31-callable-bonds/', include('chapter31_callable_bonds.urls')),
    path('chapter32-discount-margin/', include('chapter32_discount_margin.urls')),
    path('chapter33-floating-duration/', include('chapter33_floating_duration.urls')),
]
