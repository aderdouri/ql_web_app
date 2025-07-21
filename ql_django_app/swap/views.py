# Fichier : ql_web_app/swap/views.py

from django.shortcuts import render
from django.contrib import messages
from .forms import VanillaSwapForm # Nous créerons ce formulaire juste après
from . import services

def pricer_view(request): # On utilise un nom de vue standard
    form = VanillaSwapForm()
    results = None

    if request.method == 'POST':
        form = VanillaSwapForm(request.POST)
        if form.is_valid():
            try:
                # On appelle notre service avec les données du formulaire
                results = services.calculate_vanilla_swap_metrics(
                    notional=form.cleaned_data['notional'],
                    maturity_years=form.cleaned_data['maturity_years'],
                    fixed_rate_pct=form.cleaned_data['fixed_rate_pct'],
                    float_spread_pct=form.cleaned_data['float_spread_pct'],
                    discount_curve_rate_pct=form.cleaned_data['discount_curve_rate_pct'],
                    libor_curve_rate_pct=form.cleaned_data['libor_curve_rate_pct']
                )
            except Exception as e:
                messages.error(request, f"Erreur lors du calcul QuantLib : {e}")
        else:
            messages.warning(request, "Données invalides. Veuillez corriger les erreurs.")
            
    context = {'form': form, 'results': results}
    return render(request, 'swap/pricer.html', context)