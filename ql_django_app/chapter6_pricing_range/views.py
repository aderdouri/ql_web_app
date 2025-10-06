from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .forms import PricingRangeForm
from .services import calculate_pricing_over_range_api
import json

def pricing_range_lab_view(request):
    """
    Main view for Chapter 6: Pricing over a range of days
    Reproduces exactly the QuantLib Python Cookbook example
    """
    form = PricingRangeForm()
    
    # Default results for initial display
    default_results = {
        'npv_initial': 0.0,
        'summary': 'Enter parameters and click "Calculate Pricing Range" to see results.',
        'min_price': 0.0,
        'max_price': 0.0,
        'avg_price': 0.0,
        'total_dates': 0,
        'chart_data': {
            'labels': [],
            'datasets': [{
                'label': 'NPV',
                'data': [],
                'borderColor': 'blue',
                'backgroundColor': 'rgba(0, 0, 255, 0.1)',
                'fill': False,
                'tension': 0.2,
                'pointRadius': 0
            }]
        },
        'table_data': []
    }
    
    return render(request, 'chapter6_pricing_range/pricing_range_lab.html', {
        'form': form,
        'results': default_results,
        'chapter_title': 'Pricing over a Range of Days',
        'chapter_icon': 'bi-graph-up',
        'chapter_description': 'Visualize how the instrument value changes over time with discounting and time passing effects.'
    })

@csrf_exempt
@require_http_methods(["POST"])
def calculate_pricing_range_api(request):
    """
    API endpoint for pricing over range calculation
    Reproduces exactly the QuantLib Python Cookbook example
    """
    try:
        # Parse form data
        data = {
            'start_date': request.POST.get('start_date'),
            'end_date': request.POST.get('end_date'),
            'bond_start_date': request.POST.get('bond_start_date'),
            'bond_maturity_years': request.POST.get('bond_maturity_years'),
            'coupon_rate': request.POST.get('coupon_rate'),
            'face_value': request.POST.get('face_value'),
            'base_rate': request.POST.get('base_rate'),
            'rate_volatility': request.POST.get('rate_volatility'),
            'calendar': request.POST.get('calendar'),
            'settlement_convention': request.POST.get('settlement_convention'),
            'evaluation_frequency': request.POST.get('evaluation_frequency')
        }
        
        # Calculate results using the service
        result = calculate_pricing_over_range_api(data)
        
        return JsonResponse(result)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })