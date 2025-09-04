# chapter2_instruments/views.py (VERSION FINALE AVEC LE CHEMIN CORRIGÉ)

from django.shortcuts import render
from django.http import JsonResponse
from .forms import OptionPricerForm
from .services import calculate_option_values
import datetime

def pricer_lab_view(request):
    """
    Gère le laboratoire interactif pour le pricer d'options.
    """
    # Gère les mises à jour via AJAX
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = OptionPricerForm(request.POST)
        if form.is_valid():
            results = calculate_option_values(form.cleaned_data)
            return JsonResponse(results)
        else:
            return JsonResponse({'error': form.errors.as_json()}, status=400)
    
    # Gère le premier chargement de la page (requête GET)
    initial_data_from_book = {
        'evaluation_date': datetime.date(2014, 3, 7),
        'expiry_date': datetime.date(2014, 6, 7),
        'strike_price': 100.0,
        'underlying_price': 100.0,
        'risk_free_rate': 0.01,
        'volatility': 0.20,
        'option_type': 'Call'
    }
    
    form = OptionPricerForm(initial=initial_data_from_book)
    results = calculate_option_values(initial_data_from_book)
        
    context = { 'form': form, 'results': results }

    # ==============================================================================
    # CORRECTION DÉFINITIVE : Le chemin d'accès au template doit être court
    # ==============================================================================
    return render(request, 'chapter2_instruments/pricer_lab.html', context)