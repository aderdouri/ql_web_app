from django.shortcuts import render
from django.http import JsonResponse
from .forms import CallableBondForm
from .services import price_callable_bond_and_analyze
import json

def callable_bond_lab_view(request):
    """
    Handles the interactive lab for callable bonds.
    """
    context = {
        'chapter_title': '31. Modeling Callable Bonds',
        'chapter_icon': 'bi-telephone',
        'chapter_description': 'An interactive lab to price callable bonds with the Hull-White model and analyze volatility sensitivity.'
    }
    
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = CallableBondForm(request.POST)
        if form.is_valid():
            results = price_callable_bond_and_analyze(form.cleaned_data)
            return JsonResponse(results)
        else:
            return JsonResponse({'error': 'Invalid form data.', 'form_errors': form.errors}, status=400)
    
    # Premier chargement (GET)
    form = CallableBondForm()
    initial_data = {key: field.initial for key, field in form.fields.items()}
    
    try:
        results = price_callable_bond_and_analyze(initial_data)
    except Exception as e:
        results = {'error': str(e)}
    
    context['form'] = form
    if 'error' in results:
        context['error'] = results['error']
    else:
        context['results_json'] = results  # Don't double-encode with json.dumps
        context['results'] = results
        
    return render(request, 'chapter31_callable_bonds/callable_bond_lab.html', context)

def callable_bonds_description_view(request):
    context = {
        'chapter_title': '31. Modeling Callable Bonds',
        'chapter_icon': 'bi-telephone',
        'chapter_description': 'Learn how to value callable bonds using QuantLib Python with Hull-White interest rate models'
    }
    return render(request, 'chapter31_callable_bonds/description.html', context)