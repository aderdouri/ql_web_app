from django.shortcuts import render
from .forms import NumericalGreeksForm
from . import services

def greeks_lab_view(request):
    form = NumericalGreeksForm(request.POST or None)
    results = None
    
    if request.method == 'POST' and form.is_valid():
        option_params = {
            'maturity_dt': form.cleaned_data['maturity_dt'],
            'spot_price': form.cleaned_data['spot_price'],
            'strike_price': form.cleaned_data['strike_price'],
            'volatility_pct': form.cleaned_data['volatility_pct'],
            'risk_free_rate_pct': form.cleaned_data['risk_free_rate_pct'],
        }
        
        results = services.calculate_numerical_greeks(
            option_params=option_params, 
            bump_size=form.cleaned_data['bump_size'],
            evaluation_dt=form.cleaned_data['evaluation_dt']
        )
    
    context = {'form': form, 'results': results}
    return render(request, 'chapter3_greeks/greeks_lab.html', context)