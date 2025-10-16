from django.shortcuts import render
from django.http import JsonResponse
from .forms import CreditSpreadForm
from .services import setup_bond_and_curve, price_bond_with_spread
import datetime

# Variable pour garder les objets QuantLib en mémoire (optimisation)
QL_OBJECTS = {}

def description(request):
    """Chapter 30 description view"""
    context = {
        'chapter_title': '30. Valuation of bonds with credit spreads',
        'chapter_icon': 'bi-shield-check',
        'chapter_description': 'Learn how to value bonds with credit spreads using different approaches including parallel and non-parallel shifts of yield curves.'
    }
    return render(request, 'chapter30_credit_spreads/description.html', context)

def credit_spread_lab_view(request):
    global QL_OBJECTS
    context = {}

    # Gère les requêtes AJAX pour les recalculs
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = CreditSpreadForm(request.POST)
        if form.is_valid():
            if not QL_OBJECTS:
                return JsonResponse({'error': 'Server state expired. Please refresh the page.'}, status=400)
            
            results = price_bond_with_spread(QL_OBJECTS['quantlib_objects'], form.cleaned_data)
            return JsonResponse(results)
        else:
            return JsonResponse({'error': form.errors.as_json()}, status=400)

    # Gère le premier chargement de la page (GET)
    form = CreditSpreadForm()
    context['form'] = form
    
    initial_data = {
        'evaluation_date': datetime.date(2016, 7, 26),
        'issue_date': datetime.date(2016, 7, 15),
        'maturity_date': datetime.date(2021, 7, 15),
        'base_rate': 0.15, # 0.0015
        'coupon_rate': 3.0,
    }
    
    try:
        # On ne construit les objets que si la mémoire est vide
        if not QL_OBJECTS:
            print("--- Initializing QuantLib Objects ---")
            setup_results = setup_bond_and_curve(initial_data)
            if 'error' in setup_results:
                context['error'] = setup_results['error']
            else:
                QL_OBJECTS = setup_results # On stocke tout
                context['initial_npv'] = setup_results['initial_npv']
        else:
            # Si les objets existent déjà, on les réutilise
            context['initial_npv'] = QL_OBJECTS['initial_npv']
    except Exception as e:
        context['error'] = str(e)
        QL_OBJECTS = {}

    return render(request, 'chapter30_credit_spreads/credit_spread_lab.html', context)