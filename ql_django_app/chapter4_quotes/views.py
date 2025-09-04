# chapter4_quotes/views.py (VERSION FINALE AVEC MÉMOIRE PARTAGÉE)

from django.shortcuts import render
from django.http import JsonResponse
from .forms import MarketUpdateForm
from .services import build_curve_and_get_initial_state, run_simulation_optimised
import datetime
import numpy as np
from .simulation_state import SHARED_QL_OBJECTS # <-- On importe notre "mémoire"

def market_lab_view(request):
    
    # Gère les simulations AJAX (POST)
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = MarketUpdateForm(request.POST)
        if form.is_valid():
            # Si la mémoire est vide (le serveur a redémarré), on renvoie une erreur polie
            if not SHARED_QL_OBJECTS:
                return JsonResponse({'error': 'La session du serveur a expiré, veuillez rafraîchir la page.'}, status=400)

            new_price = form.cleaned_data['new_price']
            simulation_type = request.POST.get('simulation_type')
            
            # On appelle la simulation en utilisant les objets déjà en mémoire : C'EST INSTANTANÉ
            results = run_simulation_optimised(SHARED_QL_OBJECTS['quotes'], SHARED_QL_OBJECTS['bond'], new_price, simulation_type)
            return JsonResponse(results)
        else:
            return JsonResponse({'error': form.errors.as_json()}, status=400)

    # Gère le premier chargement de la page (GET)
    context = {}
    form = MarketUpdateForm()
    context['form'] = form
    
    try:
        # On vérifie si les objets sont déjà en mémoire. Si non, on les construit.
        if not SHARED_QL_OBJECTS:
            print("--- Initialisation des objets QuantLib (cette opération est lente et ne doit se produire qu'une seule fois) ---")
            eval_date = datetime.date(2016, 10, 17)
            initial_prices = [100.0] * 15
            quotes, bond, curve = build_curve_and_get_initial_state(eval_date, initial_prices)
            
            # On remplit la mémoire partagée
            SHARED_QL_OBJECTS['quotes'] = quotes
            SHARED_QL_OBJECTS['bond'] = bond
            SHARED_QL_OBJECTS['curve'] = curve

        # On utilise les objets de la mémoire pour construire le contexte
        context['initial_price'] = SHARED_QL_OBJECTS['bond'].cleanPrice()
        
        sample_times = np.linspace(0.0, 30.0, 151)
        sample_discounts = [SHARED_QL_OBJECTS['curve'].discount(t) for t in sample_times]
        context['curve_chart_data'] = { 'times': list(sample_times), 'discounts': sample_discounts }
        
    except Exception as e:
        context['error'] = str(e)
        SHARED_QL_OBJECTS.clear() # On vide la mémoire en cas d'erreur

    return render(request, 'chapter4_quotes/market_lab.html', context)