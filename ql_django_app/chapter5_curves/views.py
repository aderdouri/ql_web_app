from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .forms import TermStructureForm
from . import services
import json
from datetime import date

def curve_lab_view(request):
    """Main curve lab view"""
    form = TermStructureForm(request.POST or None)
    results = None
    
    if form.is_valid():
        evaluation_date = form.cleaned_data['evaluation_date']
        market_data = form.get_market_data()
        curve_type = form.cleaned_data['curve_type']
        day_count = form.cleaned_data['day_count']
        calendar = form.cleaned_data['calendar']
        
        try:
            results = services.build_term_structures_with_reference_dates(
                evaluation_date=evaluation_date,
                market_data=market_data,
                curve_type=curve_type,
                day_count=day_count,
                calendar=calendar
            )
        except Exception as e:
            print(f"Error building term structures: {e}")
            results = None
    
    context = {
        'form': form,
        'results': results,
        'lab_title': 'Chapter 5: Term Structures and their Reference Dates',
        'lab_icon': 'bi-graph-up',
        'lab_description': 'Interactive laboratory for building term structures with different reference dates using QuantLib.'
    }
    return render(request, 'chapter5_curves/curve_lab.html', context)

@csrf_exempt
@require_http_methods(["POST"])
def calculate_term_structures_api(request):
    """API endpoint for AJAX calculations"""
    try:
        data = json.loads(request.body)
        form = TermStructureForm(data)
        
        if form.is_valid():
            evaluation_date = form.cleaned_data['evaluation_date']
            market_data = form.get_market_data()
            curve_type = form.cleaned_data['curve_type']
            day_count = form.cleaned_data['day_count']
            calendar = form.cleaned_data['calendar']
            
            result = services.build_term_structures_with_reference_dates(
                evaluation_date=evaluation_date,
                market_data=market_data,
                curve_type=curve_type,
                day_count=day_count,
                calendar=calendar
            )
            
            if result:
                return JsonResponse({
                    'success': True,
                    'data': result
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Failed to build term structures'
                })
        else:
            print(f"Form validation errors: {form.errors}")
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