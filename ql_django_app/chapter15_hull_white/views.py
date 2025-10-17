from django.shortcuts import render
from django.http import JsonResponse
from .forms import HullWhiteForm
from .services import simulate_hull_white_paths
import json

def hull_white_description_view(request):
    """
    Displays the description page for the Hull-White model chapter.
    """
    context = {
        'chapter_title': '15. Simulating Interest Rates Using Hull-White Model',
        'chapter_icon': 'bi-graph-up-arrow',
        'chapter_description': 'Advanced simulation techniques for interest rate modeling using the Hull-White model'
    }
    return render(request, 'chapter_hull_white/description.html', context)

def hull_white_lab_view(request):
    """
    Handles the interactive lab for the Hull-White model simulation.
    """
    context = {}
    
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = HullWhiteForm(request.POST)
        if form.is_valid():
            results = simulate_hull_white_paths(form.cleaned_data)
            return JsonResponse(results)
        else:
            print(f"Form errors: {form.errors}")
            return JsonResponse({'error': 'Invalid form data.', 'form_errors': form.errors}, status=400)

    # Initial page load (GET)
    form = HullWhiteForm()
    initial_data = {key: field.initial for key, field in form.fields.items()}
    results = simulate_hull_white_paths(initial_data)
    
    context['form'] = form
    if 'error' in results:
        context['error'] = results['error']
    else:
        context['results_json'] = json.dumps(results)
        
    return render(request, 'chapter_hull_white/hull_white_lab.html', context)
