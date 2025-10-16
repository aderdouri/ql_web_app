# views.py

from django.shortcuts import render
from django.http import JsonResponse
from .forms import ShortCouponForm
from .services import analyze_short_coupon_glitch

def more_conventions_description_view(request):
    """Description page for More Mischievous Conventions chapter"""
    context = {
        'chapter_title': '36. More Mischievous Conventions',
        'chapter_icon': 'bi-exclamation-triangle-fill',
        'chapter_description': 'Learn about short coupon effects in fixed-rate bonds and the importance of proper day-count convention handling using QuantLib Python.'
    }
    return render(request, 'chapter36_more_conventions/description.html', context)

def short_coupon_lab_view(request):
    """
    Handles the interactive lab for the short coupon pricing glitch.
    """
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = ShortCouponForm(request.POST)
        if form.is_valid():
            results = analyze_short_coupon_glitch(form.cleaned_data)
            return JsonResponse(results)
        else:
            return JsonResponse({'error': 'Invalid form data.'}, status=400)

    # Initial page load (GET)
    form = ShortCouponForm()
    initial_data = {key: field.initial for key, field in form.fields.items()}
    results = analyze_short_coupon_glitch(initial_data)
    
    context = {
        'form': form,
        'results': results
    }
    return render(request, 'chapter36_more_conventions/lab.html', context)