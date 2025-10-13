# views.py

from django.shortcuts import render
from django.http import JsonResponse
from .forms import BlackFormulaForm
from .services import calculate_black_formula_option
import datetime

def black_formula_futures_description_view(request):
    """Chapter 25: Description page for Black Formula for Commodity Futures Options"""
    context = {
        'chapter_title': 'Chapter 25: Valuing Options on Commodity Futures using the Black Formula',
        'chapter_icon': 'bi-option',
        'chapter_description': 'Advanced option pricing for commodity futures using the Black formula, including Greeks calculation and risk management applications.'
    }
    return render(request, 'chapter25_black_formula_futures/black_formula_futures_description.html', context)

# Dictionnaires contenant les données des exemples du livre
TREASURY_DEFAULTS = {
    'evaluation_date': datetime.date(2015, 12, 1),
    'maturity_date': datetime.date(2015, 12, 24),
    'spot_price': 126.953,
    'strike_price': 119.0,
    'volatility': 0.11567,
    'interest_rate': 0.00105,
    'option_type': 'Call',
}
GAS_DEFAULTS = {
    'evaluation_date': datetime.date(2015, 9, 23),
    'maturity_date': datetime.date(2015, 12, 28), # T=96.12/365 ≈ 0.2633 years
    'spot_price': 2.919,
    'strike_price': 3.5,
    'volatility': 0.4251,
    'interest_rate': 0.0015,
    'option_type': 'Call',
}

def black_formula_lab_view(request):
    """
    Handles the interactive lab for the Black (1976) formula.
    """
    context = {
        'chapter_title': 'Chapter 25: Black Formula Laboratory',
        'chapter_description': 'Interactive laboratory for pricing options on commodity futures using the Black formula with real-time Greeks analysis.'
    }
    
    # Gère les requêtes AJAX pour les recalculs
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = BlackFormulaForm(request.POST)
        if form.is_valid():
            results = calculate_black_formula_option(form.cleaned_data)
            return JsonResponse(results)
        else:
            return JsonResponse({'error': form.errors.as_json()}, status=400)
    
    # Gère les requêtes POST normales (soumission de formulaire)
    if request.method == 'POST':
        form = BlackFormulaForm(request.POST)
        if form.is_valid():
            results = calculate_black_formula_option(form.cleaned_data)
            context['form'] = form
            context['results'] = results
            return render(request, 'chapter25_black_formula_futures/black_formula_lab.html', context)
        else:
            # Si le formulaire n'est pas valide, on garde les données saisies
            context['form'] = form
            context['results'] = None
            return render(request, 'chapter25_black_formula_futures/black_formula_lab.html', context)
    
    # Gère le premier chargement (GET)
    example_type = request.GET.get('example', 'treasury')
    initial_data = GAS_DEFAULTS if example_type == 'gas' else TREASURY_DEFAULTS
    
    form = BlackFormulaForm(initial=initial_data)
    results = calculate_black_formula_option(initial_data)
    
    context['form'] = form
    context['results'] = results
        
    return render(request, 'chapter25_black_formula_futures/black_formula_lab.html', context)