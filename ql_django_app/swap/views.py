from django.shortcuts import render
from .forms import VanillaSwapForm
from . import services

def pricer_view(request):
    form = VanillaSwapForm(request.POST or None)
    results = None
    
    if request.method == 'POST' and form.is_valid():
        results = services.calculate_vanilla_swap_metrics(
            notional=form.cleaned_data['notional'],
            maturity_years=form.cleaned_data['maturity_years'],
            fixed_rate_pct=form.cleaned_data['fixed_rate_pct'],
            float_spread_bps=form.cleaned_data['float_spread_bps'],
            curve_rate_pct=form.cleaned_data['curve_rate_pct']
        )
    
    context = {'form': form, 'results': results}
    return render(request, 'swap/pricer.html', context)