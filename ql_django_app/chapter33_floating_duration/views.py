from django.shortcuts import render
from django.http import JsonResponse
import datetime
from .forms import DurationFRNForm
from .services import analyze_frn_duration

def frn_duration_lab_view(request):
    """
    Handles the interactive lab for FRN duration.
    """
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = DurationFRNForm(request.POST)
        if form.is_valid():
            results = analyze_frn_duration(form.cleaned_data)
            return JsonResponse(results)
        else:
            # Afficher les erreurs de validation pour debug
            errors = {}
            for field, field_errors in form.errors.items():
                errors[field] = [str(error) for error in field_errors]
            print(f"Form validation errors: {errors}")  # Debug
            return JsonResponse({'error': f'Invalid form data: {errors}'}, status=400)

    # Initial page load (GET)
    form = DurationFRNForm()
    initial_data = {key: field.initial for key, field in form.fields.items()}
    
    # Forcer le calcul initial avec des données par défaut
    default_data = {
        'evaluation_date': initial_data.get('evaluation_date', datetime.date(2014, 10, 8)),
        'forecast_rate': initial_data.get('forecast_rate', 0.002),
        'yield_rate': initial_data.get('yield_rate', 0.002),
        'dy': initial_data.get('dy', 1e-5)
    }
    
    try:
        results = analyze_frn_duration(default_data)
        print(f"Initial calculation results: {results}")  # Debug
    except Exception as e:
        print(f"Initial calculation error: {str(e)}")  # Debug
        results = {'error': f'Initial calculation failed: {str(e)}'}
    
    context = {
        'form': form,
        'results': results
    }
    return render(request, 'chapter33_floating_duration/frn_duration_lab.html', context)

def floating_duration_description_view(request):
    context = {
        'chapter_title': '33. Duration of floating-rate bonds',
        'chapter_icon': 'bi-clock-history',
        'chapter_description': 'Learn how to correctly calculate the modified duration of floating-rate bonds using QuantLib Python and proper curve linking techniques.'
    }
    return render(request, 'chapter33_floating_duration/description.html', context)