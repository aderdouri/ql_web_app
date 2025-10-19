from django.shortcuts import render
from django.http import HttpResponse
from .forms import PriceHistoryForm
from .services import simulate_bond_price_history
import json

def price_history_lab_view(request):
    context = {
        'chapter_title': 'Chapter 6: Pricing Over a Range of Days',
        'chapter_icon': 'bi-calendar-range',
        'chapter_description': 'Learn to price instruments over a range of days and time periods for historical analysis and risk monitoring.'
    }
    results = None
    
    if request.method == 'POST':
        form = PriceHistoryForm(request.POST)
        if form.is_valid():
            results = simulate_bond_price_history(form.cleaned_data)
        else:
            results = {'error': 'Form is not valid'}
    else:
        form = PriceHistoryForm()
            
    context['form'] = form
    
    # Always set results_json
    if results and 'error' in results:
        context['error'] = results['error']
        context['results_json'] = json.dumps(results)
    elif results:
        context['results_json'] = json.dumps(results)
    else:
        context['results_json'] = json.dumps({})
        
    return render(request, 'chapter6_pricing_range/price_history_lab.html', context)