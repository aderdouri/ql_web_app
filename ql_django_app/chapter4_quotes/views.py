# File: ql_web_app/chapter4_quotes/views.py
from django.shortcuts import render
from .forms import NelsonSiegelForm # On utilise le bon nom de formulaire
from . import services

def market_lab_view(request):
    form = NelsonSiegelForm(request.POST or None)
    results = None
    
    if form.is_valid():
        # On sépare les paramètres pour le service
        ns_params = {k: v for k, v in form.cleaned_data.items() if k.startswith(('beta', 'tau'))}
        bond_params = {k: v for k, v in form.cleaned_data.items() if k.startswith('bond')}
    else:
        # On utilise les valeurs par défaut
        form = NelsonSiegelForm()
        ns_params = {k: v.initial for k, v in form.fields.items() if k.startswith(('beta', 'tau'))}
        bond_params = {k: v.initial for k, v in form.fields.items() if k.startswith('bond')}
        
    results = services.build_ns_curve_and_price_bond(ns_params, bond_params)

    context = {'form': form, 'results': results}
    return render(request, 'chapter4_quotes/market_lab.html', context)