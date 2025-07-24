# Fichier : ql_web_app/chapter6_pricing_range/views.py (VERSION DÉBOGAGE)
from django.shortcuts import render
from .forms import PriceHistoryForm
from . import services

def price_history_lab_view(request):
    print("--- VUE CHARGÉE ---")
    form = PriceHistoryForm()
    results = None

    if request.method == 'POST':
        print(">>> REQUÊTE POST REÇUE")
        form = PriceHistoryForm(request.POST)
        
        if form.is_valid():
            print(">>> FORMULAIRE VALIDE. Données :", form.cleaned_data)
            bond_params = {
                'coupon_rate_pct': form.cleaned_data['coupon_rate_pct'],
                'maturity_years': form.cleaned_data['maturity_years'],
            }
            date_range = {
                'start_date': form.cleaned_data['start_date'],
                'end_date': form.cleaned_data['end_date'],
            }
            
            print(">>> APPEL DU SERVICE...")
            try:
                results = services.calculate_price_history(bond_params, date_range)
                print(">>> SERVICE TERMINÉ. Nombre de résultats :", len(results) if results else 0)
            except Exception as e:
                print(f">>> ERREUR DANS LE SERVICE : {e}")

        else:
            print(">>> FORMULAIRE NON VALIDE. Erreurs :", form.errors)
    
    context = {'form': form, 'results': results}
    return render(request, 'chapter6_pricing_range/price_history_lab.html', context)