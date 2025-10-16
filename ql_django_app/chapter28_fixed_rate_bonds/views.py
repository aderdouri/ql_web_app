from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .forms import FixedRateBondForm
from . import services

def description(request):
    """Chapter 28 description view"""
    context = {
        'chapter_title': '28. Modeling Fixed Rate Bonds',
        'chapter_icon': 'bi-bank',
        'chapter_description': 'Learn how to model and price fixed rate bonds using QuantLib framework with yield curves and pricing engines.'
    }
    return render(request, 'chapter28_fixed_rate_bonds/description.html', context)

def lab(request):
    """Interactive lab for fixed rate bonds with all parameters from the chapter"""
    form = FixedRateBondForm()
    context = {
        'form': form,
        'chapter_title': '28. Modeling Fixed Rate Bonds - Interactive Lab',
        'chapter_icon': 'bi-bank',
        'chapter_description': 'Complete interactive laboratory with all QuantLib parameters and outputs from the chapter.'
    }
    return render(request, 'chapter28_fixed_rate_bonds/lab.html', context)

@csrf_exempt
@require_http_methods(["POST"])
def calculate_bond_price_api(request):
    """API endpoint for calculating bond price"""
    try:
        data = json.loads(request.body)
        form = FixedRateBondForm(data)
        
        if form.is_valid():
            result = services.calculate_bond_price(form.cleaned_data)
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
def calculate_sensitivity_api(request):
    """API endpoint for calculating price sensitivity"""
    try:
        data = json.loads(request.body)
        form_data = data.get('form_data', {})
        parameter_changes = data.get('parameter_changes', {})
        
        result = services.calculate_price_sensitivity(form_data, parameter_changes)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })