# Fichier : ql_web_app/chapter4_quotes/views.py (VERSION AMÉLIORÉE)

from django.shortcuts import render
from django.contrib import messages
from .forms import BondSetupForm, MarketUpdateForm
from . import services

def market_lab_view(request):
    # On initialise toujours les deux formulaires
    setup_form = BondSetupForm(prefix='setup')
    update_form = MarketUpdateForm(prefix='update')
    context = {'setup_form': setup_form, 'update_form': update_form}

    if request.method == 'POST':
        # ==============================================================================
        # LA CORRECTION EST ICI : On vérifie quel bouton a été pressé
        # ==============================================================================
        if 'setup_bond' in request.POST:
            # L'utilisateur a cliqué sur le bouton du premier formulaire
            setup_form = BondSetupForm(request.POST, prefix='setup')
            if setup_form.is_valid():
                initial_data = services.setup_bond_and_market(
                    coupon_rate_pct=setup_form.cleaned_data['coupon_rate_pct'],
                    maturity_years=setup_form.cleaned_data['maturity_years']
                )
                context.update(initial_data)
        
        elif 'update_market' in request.POST:
            # L'utilisateur a cliqué sur le bouton du deuxième formulaire
            update_form = MarketUpdateForm(request.POST, prefix='update')
            if update_form.is_valid():
                new_data = services.update_market_and_reprice(
                    new_rate_pct=update_form.cleaned_data['new_rate_pct']
                )
                context.update(new_data)

    return render(request, 'chapter4_quotes/market_lab.html', context)