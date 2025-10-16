from django.shortcuts import render
from django.http import JsonResponse
from .forms import DiscountMarginForm
from .services import calculate_discount_margin
import json

def discount_margin_lab_view(request):
    """
    Handles the interactive lab for discount margin calculation.
    """
    context = {
        'chapter_title': '32. Discount Margin Calculation',
        'chapter_icon': 'bi-calculator',
        'chapter_description': 'An interactive lab to calculate the discount margin for floating-rate bonds using numerical solvers.'
    }
    
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = DiscountMarginForm(request.POST)
        if form.is_valid():
            results = calculate_discount_margin(form.cleaned_data)
            return JsonResponse(results)
        else:
            return JsonResponse({'error': 'Invalid form data.', 'form_errors': form.errors}, status=400)
            
    form = DiscountMarginForm()
    initial_data = {key: field.initial for key, field in form.fields.items()}
    
    try:
        results = calculate_discount_margin(initial_data)
    except Exception as e:
        results = {'error': str(e)}
    
    context['form'] = form
    if 'error' in results:
        context['error'] = results['error']
    else:
        context['results_json'] = results
        context['results'] = results
        
    return render(request, 'chapter32_discount_margin/discount_margin_lab.html', context)

def discount_margin_description_view(request):
    """
    Handles the description page for discount margin calculation.
    """
    context = {
        'chapter_title': '32. Discount Margin Calculation',
        'chapter_icon': 'bi-calculator',
        'chapter_description': 'Learn how to calculate the discount margin for floating-rate bonds using QuantLib Python and numerical solvers.'
    }
    return render(request, 'chapter32_discount_margin/description.html', context)