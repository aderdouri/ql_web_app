# Fichier : ql_web_app/chapter5_curves/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .forms import CurveBuilderForm
from . import services

def curve_lab_view(request):
    form = CurveBuilderForm()
    market_rates = {'2Y': 0.201, '3Y': 0.258, '5Y': 0.464, '10Y': 1.151, '15Y': 1.588}
    
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = CurveBuilderForm(request.POST)
        if form.is_valid():
            data = services.build_and_get_curve_data(market_rates, form.cleaned_data['evaluation_dt'])
            return JsonResponse(data)
        return JsonResponse({'error': 'invalid form'}, status=400)

    initial_data = services.build_and_get_curve_data(market_rates, form.fields['evaluation_dt'].initial)
    context = {'form': form, 'initial_data': initial_data}
    return render(request, 'chapter5_curves/curve_lab.html', context)