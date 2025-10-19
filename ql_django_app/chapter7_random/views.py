from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .forms import RandomNumbersForm
from . import services

def random_numbers_view(request):
    """Main view for Chapter 7: Random Numbers and Dimensionality"""
    print("🎯 VUE RANDOM_NUMBERS_VIEW APPELÉE !")  # Test pour voir si la vue est appelée
    form = RandomNumbersForm()
    results = None
    
    # Always attempt to get results, even on initial GET request
    if request.method == 'GET':
        # For initial GET, use default form data to get demo results
        form = RandomNumbersForm()
        
        # Get all parameters
        rng_params = form.get_rng_parameters()
        option_params = form.get_option_parameters()
        
        # Calculate all results
        results = services.calculate_all_results(rng_params, option_params)
        
    elif request.method == 'POST':
        form = RandomNumbersForm(request.POST)
        if form.is_valid():
            # For POST requests, validate form
            rng_params = form.get_rng_parameters()
            option_params = form.get_option_parameters()
            
            # Calculate all results
            results = services.calculate_all_results(rng_params, option_params)
    
        # Include all chart data for the complete notebook implementation
        if results:
            # Keep all data for complete notebook reproduction
            complete_results = {
                'success': results.get('success', False),
                'random_numbers': results.get('random_numbers', []),
                'unit_square_data': results.get('unit_square_data', None),
                'sobol_1d_data': results.get('sobol_1d_data', None),
                'sobol_2d_data': results.get('sobol_2d_data', None),
                'correlated_stocks_data': results.get('correlated_stocks_data', None),
                'black_scholes_price': results.get('black_scholes_price', 0.0),
                'monte_carlo_price_rng': results.get('monte_carlo_price_rng', 0.0),
                'monte_carlo_price_sobol': results.get('monte_carlo_price_sobol', 0.0),
                'error': results.get('error', None)
            }
            results = complete_results
    
    context = {
        'form': form,
        'results': results,
        'lab_title': 'Chapter 7: Random Numbers Laboratory',
        'lab_icon': 'bi-dice-6',
        'lab_description': 'Explore different random number generators and their impact on Monte Carlo simulations.'
    }
    return render(request, 'chapter7_random/random_lab.html', context)

@csrf_exempt
@require_http_methods(["POST"])
def calculate_random_numbers_api(request):
    """API endpoint for AJAX calculations"""
    try:
        print("🔍 API Request received")
        
        # Handle both JSON and form data
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            print("📝 JSON data received")
        else:
            # Handle form data
            data = request.POST
            print("📝 Form data received")
        
        print(f"📊 Data: {data}")
        
        form = RandomNumbersForm(data)
        print(f"✅ Form created, valid: {form.is_valid()}")
        
        if form.is_valid():
            rng_params = form.get_rng_parameters()
            option_params = form.get_option_parameters()
            
            print(f"🎯 RNG params: {rng_params}")
            print(f"🎯 Option params: {option_params}")
            
            print("🚀 Starting calculations...")
            results = services.calculate_all_results(rng_params, option_params)
            print("✅ Calculations completed")
            
            return JsonResponse({
                'success': True,
                'data': results
            })
        else:
            print(f"❌ Form errors: {form.errors}")
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
            
    except Exception as e:
        print(f"💥 API Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'error': str(e)
        })
