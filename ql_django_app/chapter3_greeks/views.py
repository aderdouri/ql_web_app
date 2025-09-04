# chapter3_greeks/views.py (VERSION FINALE ET COMPLÈTE)

from django.shortcuts import render
from django.http import JsonResponse
from .forms import NumericalGreeksForm
from .services import calculate_numerical_greeks
import datetime

def greeks_lab_view(request):
    """
    Gère le laboratoire interactif pour le calcul des Greeks numériques.
    """
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = NumericalGreeksForm(request.POST)
        if form.is_valid():
            results = calculate_numerical_greeks(form.cleaned_data)
            return JsonResponse(results)
        else:
            return JsonResponse({'error': form.errors.as_json()}, status=400)
    
    # Données initiales pour répliquer le livre au chargement
    initial_data_from_book = {
        'evaluation_date': datetime.date(2014, 10, 8),
        'expiry_date': datetime.date(2015, 1, 8),
        'barrier_type': 'UpIn',
        'barrier_level': 120.0,
        'rebate': 0.0,
        'option_type': 'Call',
        'strike_price': 100.0,
        'underlying_price': 100.0,
        'risk_free_rate': 0.01,
        'volatility': 0.20,
        'h_underlying': 0.01,
        'h_rate': 0.0001,
        'h_vol': 0.0001,
    }
    
    form = NumericalGreeksForm(initial=initial_data_from_book)
    results = calculate_numerical_greeks(initial_data_from_book)
        
    context = {
        'form': form,
        'results': results
    }
    return render(request, 'chapter3_greeks/greeks_lab.html', context)