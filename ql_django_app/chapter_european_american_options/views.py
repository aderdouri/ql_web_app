# views.py (VERSION FINALE AVEC LE BON NOM DE TEMPLATE)

from django.shortcuts import render
from .forms import OptionValuationForm
from .services import price_options_and_convergence
import json

def option_valuation_description_view(request):
    """Chapter 24: Description page"""
    context = {
        'chapter_title': 'Chapter 24: Valuing European and American Options',
        'chapter_icon': 'bi-option',
        'chapter_description': 'Comprehensive option pricing models for European and American options using advanced numerical methods.'
    }
    return render(request, 'chapter_european_american_options/european_american_description.html', context)

def option_valuation_lab_view(request):
    """
    Handles the interactive lab for valuing European and American options.
    """
    context = {
        'chapter_title': 'Chapter 24: Interactive European and American Options Laboratory',
        'chapter_icon': 'bi-option',
        'chapter_description': 'Interactive laboratory for European and American option pricing using advanced numerical methods.'
    }
    
    if request.method == 'POST':
        form = OptionValuationForm(request.POST)
        if form.is_valid():
            results = price_options_and_convergence(form.cleaned_data)
        else:
            # If form is invalid, use default data but don't calculate
            form = OptionValuationForm()
            results = {'error': 'Please correct the form errors and try again'}
    else:
        form = OptionValuationForm()
        # On first load, calculate with default form data
        initial_data = {key: field.initial for key, field in form.fields.items()}
        results = price_options_and_convergence(initial_data)
            
    context['form'] = form
    if 'error' in results:
        context['error'] = results['error']
        print(f"Error in results: {results['error']}")
        # Don't set results_json when there's an error
    else:
        # Ensure proper JSON serialization
        context['results_json'] = json.dumps(results, ensure_ascii=False)
        print(f"Results generated successfully: {list(results.keys())}")
        print(f"Results type: {type(results)}")
        print(f"European convergence type: {type(results.get('european_convergence', 'NOT_FOUND'))}")
        
    return render(request, 'chapter_european_american_options/european_american_lab.html', context)