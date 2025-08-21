from django.shortcuts import render
from .forms import HestonComparisonForm
from . import services

def heston_lab_view(request):
    form = HestonComparisonForm(request.POST or None)
    results = None
    
    if request.method == 'POST' and form.is_valid():
        option_params = {
            'maturity_dt': form.cleaned_data['maturity_dt'],
            'spot_price': form.cleaned_data['spot_price'],
            'strike_price': form.cleaned_data['strike_price'],
            'volatility_pct': form.cleaned_data['volatility_pct'],
            'dividend_rate_pct': form.cleaned_data['dividend_rate_pct'],
            'risk_free_rate_pct': form.cleaned_data['risk_free_rate_pct'],
        }
        heston_params = {
            'v0': form.cleaned_data['v0'],
            'kappa': form.cleaned_data['kappa'],
            'theta': form.cleaned_data['theta'],
            'sigma': form.cleaned_data['sigma'],
            'rho': form.cleaned_data['rho'],
        }
        
        # Pass the evaluation date from the form to the service
        results = services.compare_bsm_and_heston(
            option_params, 
            heston_params,
            evaluation_dt=form.cleaned_data['evaluation_dt']
        )

    context = {'form': form, 'results': results}
    return render(request, 'chapter_heston_option/heston_lab.html', context)