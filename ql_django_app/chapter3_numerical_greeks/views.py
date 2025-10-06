"""
Chapter 3 - Numerical Greeks Lab views
Complete lab interface with form, outputs, and interactive chart
"""
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .forms import NumericalGreeksLabForm
from .services import calculate_numerical_greeks_lab_api
import json


def greeks_lab_view(request):
    """
    Main view for Chapter 3 Numerical Greeks Lab
    Complete page with form, outputs, and interactive chart
    """
    form = NumericalGreeksLabForm()
    
    # Default results for initial display
    default_results = {
        'npv': 0.0,
        'delta': 0.0,
        'gamma': 0.0,
        'rho': 0.0,
        'vega': 0.0,
        'theta': 0.0
    }
    
    # Context variables for chapter_base.html template
    context = {
        'chapter_title': 'Chapter 3: Numerical Greeks Lab',
        'chapter_icon': 'bi-calculator',
        'chapter_description': 'Calculate option sensitivities (Greeks) using numerical differentiation methods for barrier options.',
        'form': form,
        'results': default_results
    }
    
    return render(request, 'chapter3_numerical_greeks/greeks_lab.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def numerical_greeks_lab_api(request):
    """
    API endpoint for numerical Greeks lab calculation
    """
    try:
        # Parse form data
        barrier_type = request.POST.get('barrier_type')
        barrier_level = float(request.POST.get('barrier_level', 120.0))
        underlying_price = float(request.POST.get('underlying_price', 100.0))
        
        # Auto-adjust parameters for meaningful results
        barrier_adjusted = False
        strike_adjusted = False
        
        # Check if option is too far out-of-the-money
        strike_price = float(request.POST.get('strike_price', 100.0))
        if strike_price > underlying_price * 1.5:  # Strike too high
            strike_price = underlying_price * 1.1  # Set strike 10% above underlying
            strike_adjusted = True
        
        # Auto-adjust barrier level based on barrier type
        if barrier_type in ['UpIn', 'UpOut'] and barrier_level <= underlying_price:
            barrier_level = underlying_price * 1.2
            barrier_adjusted = True
        elif barrier_type in ['DownIn', 'DownOut'] and barrier_level >= underlying_price:
            # For DownIn/DownOut, set barrier closer to current price for more interesting results
            barrier_level = underlying_price * 0.95  # 95% instead of 80%
            barrier_adjusted = True
        
        data = {
            'evaluation_date': request.POST.get('evaluation_date'),
            'barrier_type': barrier_type,
            'barrier_level': barrier_level,
            'rebate': float(request.POST.get('rebate', 0.0)),
            'option_type': request.POST.get('option_type'),
            'strike_price': strike_price,
            'maturity_date': request.POST.get('maturity_date'),
            'underlying_price': underlying_price,
            'risk_free_rate': float(request.POST.get('risk_free_rate', 0.01)),
            'volatility': float(request.POST.get('volatility', 0.20)),
            'h_underlying': float(request.POST.get('h_underlying', 0.01)),
            'h_rate': float(request.POST.get('h_rate', 0.0001)),
            'h_volatility': float(request.POST.get('h_volatility', 0.0001))
        }
        
        # Calculate results
        result = calculate_numerical_greeks_lab_api(data)
        
        # Add adjustment info if needed
        if (barrier_adjusted or strike_adjusted) and result.get('success'):
            result['barrier_adjusted'] = barrier_adjusted
            result['strike_adjusted'] = strike_adjusted
            if barrier_adjusted:
                result['new_barrier_level'] = barrier_level
            if strike_adjusted:
                result['new_strike_price'] = strike_price
            result['message'] = f"Parameters automatically adjusted for meaningful results: "
            if strike_adjusted:
                result['message'] += f"Strike price set to {strike_price:.1f}. "
            if barrier_adjusted:
                result['message'] += f"Barrier level set to {barrier_level:.1f}."
        
        return JsonResponse(result)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })