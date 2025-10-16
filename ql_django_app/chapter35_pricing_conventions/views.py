# views.py

from django.shortcuts import render
from django.http import JsonResponse
from .forms import ConventionForm
from .services import analyze_pricing_conventions

def pricing_conventions_description_view(request):
    """Description page for Pricing Conventions chapter"""
    context = {
        'chapter_title': '35. Mischievous Pricing Conventions',
        'chapter_icon': 'bi-exclamation-triangle',
        'chapter_description': 'Learn about the importance of consistent day-count conventions in floating rate bond pricing using QuantLib Python.'
    }
    return render(request, 'chapter35_pricing_conventions/description.html', context)

def convention_glitch_lab_view(request):
    """
    Handles the interactive lab for pricing convention mismatch.
    """
    if request.method == 'POST':
        form = ConventionForm(request.POST)
        if form.is_valid():
            # Convert form data to the format expected by the service
            cleaned_data = form.cleaned_data.copy()
            results = analyze_pricing_conventions(cleaned_data)
            context = {
                'form': form,
                'results': results
            }
            return render(request, 'chapter35_pricing_conventions/convention_glitch_lab.html', context)
        else:
            # Form is invalid, but still show results with default values
            results = analyze_pricing_conventions({key: field.initial for key, field in form.fields.items()})
            context = {
                'form': form,
                'results': results
            }
            return render(request, 'chapter35_pricing_conventions/convention_glitch_lab.html', context)
    else:
        # GET request - show form with default values
        form = ConventionForm()
        # Calculate results with default values
        results = analyze_pricing_conventions({key: field.initial for key, field in form.fields.items()})
        context = {
            'form': form,
            'results': results
        }
        return render(request, 'chapter35_pricing_conventions/convention_glitch_lab.html', context)
