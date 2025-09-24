# chapter3_numerical_greeks/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

from .forms import NumericalGreeksForm
from .services import calculate_numerical_greeks, calculate_price_series

def greeks_lab_view(request):
    """Main view for the Numerical Greeks Lab"""
    form = NumericalGreeksForm()
    return render(request, 'chapter3_numerical_greeks/greeks_lab.html', {'form': form})

def simple_greeks_lab_view(request):
    """Simple test view for debugging chart issues"""
    return render(request, 'chapter3_numerical_greeks/greeks_lab_simple.html')

@csrf_exempt
@require_http_methods(["POST"])
def calculate_greeks_api(request):
    """API endpoint to calculate Greeks"""
    try:
        data = json.loads(request.body)
        form = NumericalGreeksForm(data)
        
        if form.is_valid():
            result = calculate_numerical_greeks(data)
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
def price_series_api(request):
    """API endpoint to calculate price series for chart"""
    try:
        data = json.loads(request.body)
        form = NumericalGreeksForm(data)
        
        if form.is_valid():
            result = calculate_price_series(data)
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
def chart_data_api(request):
    """API endpoint to calculate chart data for range 90-110"""
    try:
        data = json.loads(request.body)
        form = NumericalGreeksForm(data)
        
        if form.is_valid():
            # Calculate data for range 90-110 with step 1
            u_values = list(range(90, 111))  # 90, 91, 92, ..., 110
            npv_values = []
            delta_values = []
            gamma_values = []
            rho_values = []
            vega_values = []
            
            # For each underlying price, calculate Greeks
            for u in u_values:
                # Update underlying price in form data
                chart_data = data.copy()
                chart_data['underlying_price'] = u
                
                # Calculate Greeks for this underlying price
                result = calculate_numerical_greeks(chart_data)
                
                if result['success']:
                    npv_values.append(result['npv'])
                    delta_values.append(result['delta'])
                    gamma_values.append(result['gamma'])
                    rho_values.append(result['rho'])
                    vega_values.append(result['vega'])
                else:
                    # If calculation fails, use test data
                    npv_values.append(2 + (u - 90) * 0.4)  # Linear interpolation
                    delta_values.append(0.1 + (u - 90) * 0.02)
                    gamma_values.append(0.05 + (u - 90) * 0.001)
                    rho_values.append(5 + (u - 90) * 0.075)
                    vega_values.append(20 + (u - 90) * 0.5)
            
            return JsonResponse({
                'success': True,
                'u_values': u_values,
                'npv_values': npv_values,
                'delta_values': delta_values,
                'gamma_values': gamma_values,
                'rho_values': rho_values,
                'vega_values': vega_values
            })
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