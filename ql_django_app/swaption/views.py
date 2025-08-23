from django.shortcuts import render
from django.contrib import messages
from .forms import SwaptionForm 
from . import services

def pricer_view(request): # On standardise le nom
    form = SwaptionForm()
    results = None

    if request.method == 'POST':
        form = SwaptionForm(request.POST)
        if form.is_valid():
            try:
                results = services.calculate_swaption_metrics(
                    option_type_str=form.cleaned_data['option_type'],
                    maturity_years=form.cleaned_data['maturity_years'],
                    swap_tenor_years=form.cleaned_data['swap_tenor_years'],
                    strike_rate_pct=form.cleaned_data['strike_rate_pct'],
                    notional=form.cleaned_data['notional'],
                    volatility_pct=form.cleaned_data['volatility_pct'],
                    curve_rate_pct=form.cleaned_data['curve_rate_pct']
                )
            except Exception as e:
                messages.error(request, f"Erreur lors du calcul QuantLib : {e}")
        else:
            messages.warning(request, "Données invalides. Veuillez corriger les erreurs.")
            
    context = {'form': form, 'results': results}
    return render(request, 'swaption/pricer.html', context)