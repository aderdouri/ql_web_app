# chapter2_instruments/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .forms import OptionPricingForm
from . import services

def pricer_lab_view(request):
    """Main option pricing lab view"""
    form = OptionPricingForm()
    context = {
        'form': form,
        'lab_title': 'Chapter 2: Instruments & Pricing - Interactive Lab',
        'lab_icon': 'bi-gear',
        'lab_description': 'Interactive laboratory for option pricing using different engines and models.'
    }
    return render(request, 'chapter2_instruments/pricer_lab.html', context)

@csrf_exempt
@require_http_methods(["POST"])
def calculate_option_price_api(request):
    """API endpoint for calculating option price"""
    try:
        data = json.loads(request.body)
        form = OptionPricingForm(data)
        
        if form.is_valid():
            result = services.calculate_option_price(form.cleaned_data)
            return JsonResponse(result)
        else:
            return JsonResponse({
                'success': False,
                'error': 'Invalid form data',
                'form_errors': form.errors
            })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@csrf_exempt
@require_http_methods(["POST"])
def calculate_price_series_api(request):
    """API endpoint for calculating price series"""
    try:
        data = json.loads(request.body)
        form_data = data.get('form_data', {})
        underlying_prices = data.get('underlying_prices', [])
        
        result = services.calculate_price_series(underlying_prices, form_data)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@csrf_exempt
@require_http_methods(["POST"])
def calculate_volatility_series_api(request):
    """API endpoint for calculating volatility series"""
    try:
        data = json.loads(request.body)
        form_data = data.get('form_data', {})
        volatilities = data.get('volatilities', [])
        
        result = services.calculate_volatility_series(volatilities, form_data)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@csrf_exempt
@require_http_methods(["POST"])
def calculate_time_decay_series_api(request):
    """API endpoint for calculating time decay series"""
    try:
        data = json.loads(request.body)
        form_data = data.get('form_data', {})
        evaluation_dates = data.get('evaluation_dates', [])
        
        result = services.calculate_time_decay_series(evaluation_dates, form_data)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@csrf_exempt
@require_http_methods(["POST"])
def compare_engines_api(request):
    """API endpoint for comparing different pricing engines"""
    try:
        data = json.loads(request.body)
        form = OptionPricingForm(data)
        
        if form.is_valid():
            result = services.compare_engines(form.cleaned_data)
            return JsonResponse(result)
        else:
            return JsonResponse({
                'success': False,
                'error': 'Invalid form data',
                'form_errors': form.errors
            })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })