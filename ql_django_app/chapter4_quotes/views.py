from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from datetime import date
from .forms import BondCurveForm
from . import services

def bond_curve_lab_view(request):
    """
    Main view for the bond curve construction lab.
    Handles form display and initial calculations.
    """
    form = BondCurveForm(request.POST or None)
    results = None
    
    if form.is_valid():
        # Extract form data
        evaluation_date = form.cleaned_data['evaluation_date']
        coupon_data = form.cleaned_data['coupon_matrix']
        bond_quotes = form.cleaned_data['bond_quotes']
        enable_observer = form.cleaned_data['enable_observer']
        is_frozen = form.cleaned_data['is_frozen']
        
        # Build curve and calculate
        try:
            results = services.build_bond_curve(
                evaluation_date=evaluation_date,
                coupon_data=coupon_data,
                bond_quotes=bond_quotes,
                enable_observer=enable_observer,
                is_frozen=is_frozen
            )
        except Exception as e:
            results = {
                'error': f"Error in calculation: {str(e)}",
                'initial_price': 0,
                'price_history': [],
                'curve_data': {'maturities': [], 'discount_factors': []},
                'discount_chart': '',
                'price_evolution_chart': '',
                'messages': [f"Calculation failed: {str(e)}"]
            }
    else:
        # Use default values for initial display - NO CALCULATIONS
        form = BondCurveForm()
        results = None  # No initial calculations for fast loading
    
    context = {
        'form': form,
        'results': results,
        'coupon_data': coupon_data if 'coupon_data' in locals() else json.loads(form.fields['coupon_matrix'].initial),
        'bond_quotes': bond_quotes if 'bond_quotes' in locals() else json.loads(form.fields['bond_quotes'].initial),
        'lab_title': 'Chapter 4: Market Quotes - Interactive Lab',
        'lab_icon': 'bi-graph-up',
        'lab_description': 'Build Nelson-Siegel yield curves and analyze bond price evolution with real-time market quote updates.'
    }
    
    return render(request, 'chapter4_quotes/market_lab.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def update_quotes_ajax(request):
    """
    AJAX endpoint to update bond quotes and recalculate prices with new charts.
    """
    try:
        data = json.loads(request.body)
        bond_quotes = data.get('bond_quotes', [])
        coupon_data = data.get('coupon_data', [])
        evaluation_date_str = data.get('evaluation_date', '2016-10-17')
        enable_observer = data.get('enable_observer', True)
        is_frozen = data.get('is_frozen', False)
        
        if not bond_quotes or not coupon_data:
            return JsonResponse({'error': 'Missing bond_quotes or coupon_data'}, status=400)
        
        # Validate quotes
        for quote in bond_quotes:
            if not isinstance(quote, (int, float)) or quote <= 0:
                return JsonResponse({'error': 'Invalid quote values'}, status=400)
        
        # Parse evaluation date
        from datetime import datetime
        evaluation_date = datetime.strptime(evaluation_date_str, '%Y-%m-%d').date()
        
        # Rebuild curve with new data
        results = services.build_bond_curve(
            evaluation_date=evaluation_date,
            coupon_data=coupon_data,
            bond_quotes=bond_quotes,
            enable_observer=enable_observer,
            is_frozen=is_frozen
        )
        
        response_data = {
            'success': True,
            'message': 'Quotes updated successfully',
            'initial_price': results['initial_price'],
            'final_price': results['final_price'],
            'price_change': results['price_change'],
            'price_history': results['price_history'],
            'all_prices': results['all_prices'],
            'curve_chart_data': results['curve_chart_data'],
            'price_chart_data': results['price_chart_data'],
            'curve_data': results['curve_data'],
            'dynamic_explanation': results.get('dynamic_explanation', {})
        }
        
        return JsonResponse(response_data)
        
    except json.JSONDecodeError as e:
        return JsonResponse({'error': f'Invalid JSON data: {str(e)}'}, status=400)
    except Exception as e:
        import traceback
        return JsonResponse({'error': f'Server error: {str(e)}', 'traceback': traceback.format_exc()}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def freeze_unfreeze_ajax(request):
    """
    AJAX endpoint to freeze/unfreeze calculations.
    """
    try:
        data = json.loads(request.body)
        action = data.get('action', '')
        
        if action not in ['freeze', 'unfreeze']:
            return JsonResponse({'error': 'Invalid action'}, status=400)
        
        # Simulate freeze/unfreeze
        response_data = {
            'success': True,
            'action': action,
            'message': f'Calculations {action}d successfully'
        }
        
        return JsonResponse(response_data)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)