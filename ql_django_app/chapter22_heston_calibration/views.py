from django.shortcuts import render
from .forms import VolatilitySmileForm
from .services import process_volatility_data
import json

def heston_calibration_description_view(request):
    """Chapter 22: Description page"""
    context = {
        'chapter_title': 'Chapter 22: Volatility Smile and Heston Model Calibration',
        'chapter_icon': 'bi-graph-up-arrow',
        'chapter_description': 'Learn how to construct volatility smiles and calibrate the Heston stochastic volatility model to market data for European options.'
    }
    return render(request, 'chapter_heston_calibration/volatility_smile_simple.html', context)

def volatility_smile_lab_view(request):
    context = {}
    
    # Valeurs par défaut explicites
    import datetime
    default_data = {
        'evaluation_date': datetime.date(2015, 11, 6),
        'spot_price': 659.37,
        'risk_free_rate': 1.0,
        'dividend_rate': 0.0,
        'smile_expiry': 1.0,
        'calibration_expiry_index': 11,
        'initial_variance': 0.01,
        'kappa': 0.2,
        'theta': 0.02,
        'sigma': 0.5,
        'rho': -0.75
    }
    
    if request.method == 'POST':
        form = VolatilitySmileForm(request.POST)
        if form.is_valid():
            # Utiliser les données du formulaire validé
            results = process_volatility_data(form.cleaned_data)
        else:
            # Si le formulaire n'est pas valide, utiliser les données par défaut
            results = process_volatility_data(default_data)
    else:
        # Pour GET, seulement pré-remplir le formulaire, pas de calcul
        form = VolatilitySmileForm(initial=default_data)
        results = None
            
    context['form'] = form
    if results is None:
        # Pas de calcul effectué (première visite)
        context['error'] = None
        context['results_json'] = None
    elif 'error' in results:
        context['error'] = results['error']
        context['results_json'] = None
    else:
        context['results_json'] = json.dumps(results)
        
    return render(request, 'chapter_heston_calibration/volatility_smile_lab.html', context)