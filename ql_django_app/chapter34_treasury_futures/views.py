# views.py

from django.shortcuts import render
from django.http import JsonResponse
from .forms import TreasuryFuturesForm
from .services import analyze_treasury_futures

def treasury_futures_description_view(request):
    """Description page for Treasury Futures Contracts chapter"""
    context = {
        'chapter_title': '34. Treasury Futures Contracts',
        'chapter_icon': 'bi-graph-up-arrow',
        'chapter_description': 'Learn how to value treasury futures contracts using QuantLib Python, including cheapest-to-deliver calculations and proper futures pricing.'
    }
    return render(request, 'chapter34_treasury_futures/description.html', context)

def treasury_futures_lab_view(request):
    """
    Handles the interactive lab for treasury futures.
    """
    if request.method == 'POST':
        form = TreasuryFuturesForm(request.POST)
        if form.is_valid():
            # Convert form data to the format expected by the service
            cleaned_data = form.cleaned_data.copy()
            # The date is already a datetime.date object from the form
            results = analyze_treasury_futures(cleaned_data)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse(results)
            else:
                # Regular POST request - render with results
                context = {
                    'form': form,
                    'results': results
                }
                return render(request, 'chapter34_treasury_futures/treasury_futures_lab.html', context)
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Invalid form data.'}, status=400)
            else:
                # Regular POST with invalid form - render with errors
                results = analyze_treasury_futures({key: field.initial for key, field in form.fields.items()})
                context = {
                    'form': form,
                    'results': results
                }
                return render(request, 'chapter34_treasury_futures/treasury_futures_lab.html', context)

    # Initial page load (GET)
    form = TreasuryFuturesForm()
    initial_data = {key: field.initial for key, field in form.fields.items()}
    results = analyze_treasury_futures(initial_data)
    
    context = {
        'form': form,
        'results': results
    }
    return render(request, 'chapter34_treasury_futures/treasury_futures_lab.html', context)