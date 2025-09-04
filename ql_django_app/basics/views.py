# basics/views.py (VERSION FINALE ET NETTOYÉE)

from django.shortcuts import render

def home(request):
    """
    Cette vue affiche UNIQUEMENT la page d'accueil de la section 'basics'.
    Elle ne doit faire aucun calcul. C'est la correction la plus importante.
    """
    return render(request, 'basics/base.html')

# Les autres vues pour les pages statiques peuvent rester ici
def quantlib_basics_view(request):
    return render(request, 'basics/quantlib_basics.html')

def market_quotes_view(request):
    return render(request, 'basics/market_quotes.html')

def numerical_greeks_view(request):
    return render(request, 'basics/numerical_greeks.html')

def term_structures_view(request):
    return render(request, 'basics/term_structures.html')

def pricing_over_range_view(request):
    return render(request, 'basics/pricing_over_range.html')

def random_numbers_view(request):
    return render(request, 'basics/random_numbers.html')