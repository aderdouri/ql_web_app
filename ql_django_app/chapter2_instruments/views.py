# Fichier : ql_web_app/chapter2_instruments/views.py
from django.shortcuts import render
from .forms import PricingEngineForm
from . import services

def pricer_lab_view(request):
    form = PricingEngineForm(request.POST or None)
    results = None

    # On détermine les paramètres à utiliser
    if form.is_valid():
        engine_choice = form.cleaned_data['engine_choice']
        option_params = {k: v for k, v in form.cleaned_data.items() if k != 'engine_choice'}
    else:
        # En cas de GET ou d'erreur, on utilise les valeurs par défaut
        form = PricingEngineForm()
        engine_choice = form.fields['engine_choice'].initial
        option_params = {
            'maturity_dt': form.fields['maturity_dt'].initial,
            'spot_price': form.fields['spot_price'].initial,
            'strike_price': form.fields['strike_price'].initial,
            'volatility_pct': form.fields['volatility_pct'].initial,
            'dividend_rate_pct': form.fields['dividend_rate_pct'].initial,
            'risk_free_rate_pct': form.fields['risk_free_rate_pct'].initial,
        }
    
    # On lance toujours le calcul
    try:
        results = services.price_option_with_engine(option_params, engine_choice)
    except Exception as e:
        print(f"Error in Chapter 2 service: {e}")
    
    context = {'form': form, 'results': results}
    return render(request, 'chapter2_instruments/pricer_lab.html', context)