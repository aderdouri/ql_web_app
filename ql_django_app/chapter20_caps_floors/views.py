from django.shortcuts import render
from django.http import JsonResponse
import json
from .forms import CapFloorForm
from . import services

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
        # Use form data directly - now all fields match
        params = form.cleaned_data.copy()
        
        # Convert percentage fields to decimal
        params['strike_rate'] = params['strike_rate'] / 100.0
        params['fixing_rate'] = params['fixing_rate'] / 100.0
        params['constant_volatility'] = params['constant_volatility'] / 100.0
        params['surface_strike_1'] = params['surface_strike_1'] / 100.0
        params['surface_strike_2'] = params['surface_strike_2'] / 100.0
        params['surface_strike_3'] = params['surface_strike_3'] / 100.0
        
        # Convert zero rates to decimal
        for i in range(1, 11):
            params[f'zero_rate_{i}'] = params[f'zero_rate_{i}'] / 100.0
        
        # Calculate results with form data
        results = services.calculate_caps_floors_metrics(**params)
    else:
        form = CapFloorForm() # Create a clean form for GET or invalid POST
        from datetime import date
        
        # Helper function to get initial value, handling both values and callables
        def get_initial_value(field):
            initial = field.initial
            if callable(initial):
                return initial()
            return initial
        
        # Get initial values for all fields
        params = {}
        for field_name, field in form.fields.items():
            initial_value = get_initial_value(field)
            params[field_name] = initial_value
        
        # Convert percentage fields to decimal
        percentage_fields = ['strike_rate', 'fixing_rate', 'constant_volatility', 
                           'surface_strike_1', 'surface_strike_2', 'surface_strike_3']
        for field in percentage_fields:
            if field in params:
                params[field] = params[field] / 100.0
        
        # Convert zero rates to decimal
        for i in range(1, 11):
            field_name = f'zero_rate_{i}'
            if field_name in params:
                params[field_name] = params[field_name] / 100.0
        
        # Calculate results with default data
        results = services.calculate_caps_floors_metrics(**params)
    
    # Convert volatility surface data to JSON for JavaScript
    if results and 'volatility_surface_data' in results:
        results['volatility_surface_data_json'] = json.dumps(results['volatility_surface_data'])
    
    context = {'form': form, 'results': results}
    return render(request, 'caps_floors/lab.html', context)