from django.shortcuts import render
from django.http import JsonResponse
import json
from .forms import CapFloorForm
from . import working_services as services

def caps_floors_description_view(request):
    """Description page for caps and floors chapter"""
    context = {
        'chapter_title': '20. Caps and Floors',
        'chapter_icon': 'bi-shield-check',
        'chapter_description': 'Learn how to value interest rate caps and floors using QuantLib, including constant volatility and volatility surface approaches.'
    }
    return render(request, 'caps_floors/description.html', context)

def caps_floors_lab_view(request):
    """Interactive lab for caps and floors pricing"""
    form = CapFloorForm(request.POST or None)
    results = None
    
    if form.is_valid():
        # Use all form data - now fully dynamic
        params = form.cleaned_data
        
        # Validate dates to prevent negative time errors
        evaluation_date = params.get('evaluation_date')
        fixing_date = params.get('fixing_date')
        
        if fixing_date and evaluation_date and fixing_date >= evaluation_date:
            # Fix the fixing date to be before evaluation date
            from datetime import timedelta
            params['fixing_date'] = evaluation_date - timedelta(days=2)
        
        # Ensure fixing date is a business day (not weekend)
        if fixing_date:
            from datetime import timedelta
            while fixing_date.weekday() >= 5:  # Saturday = 5, Sunday = 6
                fixing_date = fixing_date - timedelta(days=1)
            params['fixing_date'] = fixing_date
        
        # Convert pricing method to lowercase for service compatibility
        if params.get('pricing_method') == 'Constant Volatility':
            params['pricing_method'] = 'constant'
        elif params.get('pricing_method') == 'Volatility Surface':
            params['pricing_method'] = 'surface'
        
        # Calculate results with form data
        try:
            results = services.calculate_caps_floors_metrics(**params)
        except Exception as e:
            results = {
                'error': True,
                'error_message': f"Calculation error: {str(e)}",
                'pricing_method': params.get('pricing_method', 'Unknown'),
                'strike_rate': params.get('strike_rate', 0),
                'notional': params.get('notional', 0),
                'start_date': params.get('start_date'),
                'end_date': params.get('end_date'),
            }
    else:
        # Create a clean form for GET or invalid POST
        if not form.is_bound:  # Only calculate default results on initial GET
            from datetime import date, timedelta
            
            # Helper function to get initial value, handling both values and callables
            def get_initial_value(field):
                initial = field.initial
                if callable(initial):
                    return initial()
                return initial
            
            params = {
                'evaluation_date': get_initial_value(form.fields['evaluation_date']),
                'notional': get_initial_value(form.fields['notional']),
                'start_date': get_initial_value(form.fields['start_date']),
                'end_date': get_initial_value(form.fields['end_date']),
                'strike_rate': get_initial_value(form.fields['strike_rate']),
                'fixing_date': get_initial_value(form.fields['fixing_date']),
                'fixing_rate': get_initial_value(form.fields['fixing_rate']),
                'pricing_method': get_initial_value(form.fields['pricing_method']),
                'constant_volatility': get_initial_value(form.fields['constant_volatility']),
                'surface_strike_1': get_initial_value(form.fields['surface_strike_1']),
                'surface_strike_2': get_initial_value(form.fields['surface_strike_2']),
                'surface_strike_3': get_initial_value(form.fields['surface_strike_3']),
                'zero_rate_1': get_initial_value(form.fields['zero_rate_1']),
                'zero_rate_2': get_initial_value(form.fields['zero_rate_2']),
                'zero_rate_3': get_initial_value(form.fields['zero_rate_3']),
                'zero_rate_4': get_initial_value(form.fields['zero_rate_4']),
                'zero_rate_5': get_initial_value(form.fields['zero_rate_5']),
                'zero_rate_6': get_initial_value(form.fields['zero_rate_6']),
                'zero_rate_7': get_initial_value(form.fields['zero_rate_7']),
                'zero_rate_8': get_initial_value(form.fields['zero_rate_8']),
                'zero_rate_9': get_initial_value(form.fields['zero_rate_9']),
                'zero_rate_10': get_initial_value(form.fields['zero_rate_10']),
            }
            
            # Convert pricing method to lowercase for service compatibility
            if params.get('pricing_method') == 'Constant Volatility':
                params['pricing_method'] = 'constant'
            elif params.get('pricing_method') == 'Volatility Surface':
                params['pricing_method'] = 'surface'
            
            # Calculate results with default data
            try:
                results = services.calculate_caps_floors_metrics(**params)
            except Exception as e:
                results = {
                    'error': True,
                    'error_message': f"Default calculation error: {str(e)}",
                    'pricing_method': 'Constant Volatility',
                    'strike_rate': 4.0,
                    'notional': 1000000,
                    'start_date': date.today() + timedelta(days=30),
                    'end_date': date.today() + timedelta(days=365*5),
                }
    
    # Convert volatility surface data to JSON for JavaScript
    if results and 'volatility_surface_data' in results:
        results['volatility_surface_data_json'] = json.dumps(results['volatility_surface_data'])
    
    context = {'form': form, 'results': results}
    return render(request, 'caps_floors/lab.html', context)