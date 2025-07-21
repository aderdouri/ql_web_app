# File: ql_web_app/interest_rate_curves/views.py

from django.shortcuts import render

def home(request):
    """
    This view renders the homepage for the "Interest-Rate Curves" category.
    It displays the base template which includes the sub-navbar for this section.
    """
    return render(request, 'interest_rate_curves/base.html')

# When you implement Chapter 10, you will create a new app (e.g., 'yield_curve_builder')
# and its view will be in 'yield_curve_builder/views.py', not here.
# This file is ONLY for views related to the category itself.