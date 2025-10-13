from django.shortcuts import render
from .forms import HestonComparisonForm
from . import services

def heston_description_view(request):
    """Chapter 21: Description page (like Basics chapters)"""
    context = {
        'chapter_title': 'Chapter 21: Valuing European Option using the Heston Model',
        'chapter_icon': 'bi-graph-up',
        'chapter_description': 'Learn how to value European options using the Heston stochastic volatility model and compare it with Black-Scholes-Merton pricing.'
    }
    return render(request, 'chapter_heston_option/heston_description.html', context)

def heston_lab_view(request):
    """Chapter 21: Interactive lab page"""
    results = None
    
    if request.method == 'POST':
        form = HestonComparisonForm(request.POST)
        if form.is_valid():
            option_params = {
                'maturity_dt': form.cleaned_data['maturity_dt'],
                'spot_price': form.cleaned_data['spot_price'],
                'strike_price': form.cleaned_data['strike_price'],
                'option_type': form.cleaned_data.get('option_type', 'call'),
                'exercise_type': form.cleaned_data.get('exercise_type', 'european'),
                'volatility_pct': form.cleaned_data['volatility_pct'],
                'dividend_rate_pct': form.cleaned_data['dividend_rate_pct'],
                'risk_free_rate_pct': form.cleaned_data['risk_free_rate_pct'],
                'heston_engine_rate': form.cleaned_data.get('heston_engine_rate', 0.01),
                'heston_engine_steps': form.cleaned_data.get('heston_engine_steps', 1000),
            }
            heston_params = {
                'v0': form.cleaned_data.get('v0', 0.04),
                'kappa': form.cleaned_data.get('kappa', 0.1),
                'theta': form.cleaned_data.get('theta', 0.04),
                'sigma': form.cleaned_data.get('sigma', 0.1),
                'rho': form.cleaned_data.get('rho', -0.75),
            }
            
            # Pass the evaluation date from the form to the service
            results = services.compare_bsm_and_heston(
                option_params, 
                heston_params,
                evaluation_dt=form.cleaned_data['evaluation_dt']
            )
            # Keep the form with user's input values - don't reset
    else:
        form = HestonComparisonForm()

    context = {
        'form': form, 
        'results': results,
        'chapter_title': 'Chapter 21: Interactive Heston Pricing Laboratory',
        'chapter_icon': 'bi-bar-chart',
        'chapter_description': 'Interactive laboratory for European option pricing using Heston and Black-Scholes-Merton models.'
    }
    return render(request, 'chapter_heston_option/heston_lab_page.html', context)