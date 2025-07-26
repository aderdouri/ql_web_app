from django.shortcuts import render
from .forms import PriceHistoryForm
from . import services

def price_history_lab_view(request):
    results = None
    
    # Si la requête est un POST, on crée le formulaire avec les données soumises
    if request.method == 'POST':
        form = PriceHistoryForm(request.POST)
        
        # On vérifie si le formulaire est valide
        if form.is_valid():
            # Si oui, on prépare les paramètres à partir des données "nettoyées" du formulaire
            bond_params = {
                'coupon_rate_pct': form.cleaned_data['coupon_rate_pct'],
                'maturity_years': form.cleaned_data['maturity_years'],
            }
            date_range = {
                'start_date': form.cleaned_data['start_date'],
                'end_date': form.cleaned_data['end_date'],
            }
            
            # On appelle le service avec les données validées
            results = services.calculate_price_history(bond_params, date_range)
    
    # Si la requête est un GET (premier chargement), on crée un formulaire vide
    else:
        form = PriceHistoryForm()
        # On n'effectue aucun calcul au chargement initial.
        # Le template affichera le message "Please define a bond...".

    context = {'form': form, 'results': results}
    return render(request, 'chapter6_pricing_range/price_history_lab.html', context)