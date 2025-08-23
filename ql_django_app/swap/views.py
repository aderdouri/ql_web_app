from django.shortcuts import render
from .forms import VanillaSwapForm
from . import services

def pricer_view(request):
    form = VanillaSwapForm(request.POST or None)
    results = None
    
    if form.is_valid():
        params = form.cleaned_data
    else:
        form = VanillaSwapForm() # Create a clean form for GET or invalid POST
        params = {
            'notional': form.fields['notional'].initial,
            'maturity_years': form.fields['maturity_years'].initial,
            'fixed_rate_pct': form.fields['fixed_rate_pct'].initial,
            'floating_spread_bps': form.fields['floating_spread_bps'].initial,
            'discount_curve_rate_pct': form.fields['discount_curve_rate_pct'].initial,
        }
            
    results = services.calculate_vanilla_swap_metrics(**params)
    
    context = {'form': form, 'results': results}
    return render(request, 'swap/pricer.html', context)