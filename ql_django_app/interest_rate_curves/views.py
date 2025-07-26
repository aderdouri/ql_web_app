from django.shortcuts import render

def home(request):
    """Renders the homepage for the Interest-Rate Curves category."""
    return render(request, 'interest_rate_curves/base.html')

# --- Placeholder views for each chapter ---

def eonia_curve_view(request):
    return render(request, 'interest_rate_curves/eonia_curve.html')


def dangerous_day_count_view(request):
    return render(request, 'interest_rate_curves/dangerous_day_count.html')

def implied_term_structures_view(request):
    return render(request, 'interest_rate_curves/implied_term_structures.html')

def sensitivities_view(request):
    return render(request, 'interest_rate_curves/sensitivities.html')

def glitch_forward_curves_view(request):
    return render(request, 'interest_rate_curves/glitch_forward_curves.html')