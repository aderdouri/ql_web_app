# File: ql_web_app/chapter_2_lab/views.py
from django.shortcuts import render
from .forms import EngineComparisonForm
from . import services

def lab_view(request):
    form = EngineComparisonForm()
    results = None
    if request.method == 'POST':
        form = EngineComparisonForm(request.POST)
        if form.is_valid():
            results = services.run_engine_comparison(
                spot_price=form.cleaned_data['spot_price'],
                strike_price=form.cleaned_data['strike_price'],
                maturity_dt=form.cleaned_data['maturity_date'],
                volatility_pct=form.cleaned_data['volatility'],
                risk_free_rate_pct=form.cleaned_data['risk_free_rate'],
                selected_engines=form.cleaned_data['engines_to_compare']
            )
    context = {'form': form, 'results': results}
    return render(request, 'chapter_2_lab/lab.html', context)