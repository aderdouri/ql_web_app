from django.shortcuts import render
from django.http import JsonResponse
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
            return JsonResponse({'error': 'Invalid form data.'}, status=400)

    # Initial page load (GET)
    form = DurationFRNForm()
    initial_data = {key: field.initial for key, field in form.fields.items()}
    
    try:
        results = analyze_frn_duration(initial_data)
    except Exception as e:
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