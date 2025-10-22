from django.shortcuts import render
from .forms import VanillaSwapForm
from . import services

def swap_description_view(request):
    """Description page for interest rate swaps chapter"""
    context = {
        'chapter_title': '19. Modeling interest rate swaps using QuantLib',
        'chapter_icon': 'bi-arrow-repeat',
        'chapter_description': 'Learn how to model and price interest rate swaps using QuantLib, including vanilla swaps, forward rate agreements, and swap curve construction.'
    }
    return render(request, 'swap/description.html', context)

def pricer_view(request):
    form = VanillaSwapForm(request.POST or None)
    results = None
    book_validation = None
    
    if form.is_valid():
        params = form.cleaned_data
    else:
        form = VanillaSwapForm() # Create a clean form for GET or invalid POST
        from datetime import date
        params = {
            'notional': form.fields['notional'].initial,
            'maturity_years': form.fields['maturity_years'].initial,
            'fixed_rate_pct': form.fields['fixed_rate_pct'].initial,
            'floating_spread_bps': form.fields['floating_spread_bps'].initial,
            'risk_free_rate_pct': form.fields['risk_free_rate_pct'].initial,
            'libor_rate_pct': form.fields['libor_rate_pct'].initial,
            'evaluation_date': None,  # Use book's default date
        }
    
    # Calculate results
    results = services.calculate_vanilla_swap_metrics(**params)
    
    # Validate against book example if using default parameters
    if (params['notional'] == 10000000 and 
        params['maturity_years'] == 10 and 
        params['fixed_rate_pct'] == 2.5 and 
        params['floating_spread_bps'] == 40.0 and 
        params['risk_free_rate_pct'] == 1.0 and 
        params['libor_rate_pct'] == 2.0):
        book_validation = services.calculate_book_example_swap()
    
    context = {
        'form': form, 
        'results': results,
        'book_validation': book_validation
    }
    return render(request, 'swap/pricer.html', context)