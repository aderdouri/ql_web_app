from django.shortcuts import render

def home(request):
    """Affiche la page d'accueil de la catégorie Interest-Rate Models."""
    return render(request, 'interest_rate_models/base.html')

# --- Vues placeholder pour chaque chapitre ---

def hull_white_simulation_view(request):
    return render(request, 'interest_rate_models/hull_white_simulation.html')

def short_rate_calibration_view(request):
    return render(request, 'interest_rate_models/short_rate_calibration.html')

def caps_floors_view(request):
    return render(request, 'interest_rate_models/caps_floors.html')

def heston_option_view(request):
    return render(request, 'interest_rate_models/heston_option.html')

def heston_calibration_view(request):
    return render(request, 'interest_rate_models/heston_calibration.html')
# ==============================================================================
def par_indexed_coupons_view(request):
    """
    Placeholder view for the "Par versus indexed coupons" chapter.
    """
    # Pour l'instant, elle rendra un template "en construction".
    return render(request, 'interest_rate_models/par_indexed_coupons.html')