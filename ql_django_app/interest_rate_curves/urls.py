# File: ql_web_app/interest_rate_curves/urls.py

from django.urls import path, include
from . import views

# This defines the namespace for this category.
# It's crucial for the main urls.py file and for templates.
app_name = 'interest_rate_curves'

urlpatterns = [
    # The URL for the "Interest-Rate Curves" category homepage.
    # When a user navigates to /interest-rate-curves/, this pattern will match.
    path('', views.home, name='home'),
    
    # --- Future chapters will be included here ---
    # Example for Chapter 10:
    # path('constructing-yield-curve/', include('yield_curve_builder.urls')),
    
    # Example for Chapter 9:
    # path('euribor-bootstrapping/', include('euribor_bootstrap.urls')),
]