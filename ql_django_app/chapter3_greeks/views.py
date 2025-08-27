# Fichier : ql_web_app/chapter3_greeks/views.py (VERSION FINALE AVEC GESTION D'ERREUR)

from django.shortcuts import render
from .forms import NumericalGreeksForm
from . import services

def greeks_lab_view(request):
    results = None
    
    # Si la requête est un POST (l'utilisateur a cliqué sur le bouton)
    if request.method == 'POST':
        form = NumericalGreeksForm(request.POST)
        
        # On vérifie si les données envoyées sont valides
        if form.is_valid():
            # Si oui, on appelle le service avec les données "nettoyées"
            # La variable 'results' sera remplie
            results = services.calculate_all_numerical_greeks(form.cleaned_data)
        
        # Si le formulaire N'EST PAS VALIDE (ex: maturité <= évaluation),
        # on ne fait rien de plus. La variable 'results' restera None.
        # Django va automatiquement attacher les messages d'erreur au formulaire.
    
    # Si la requête est un GET (premier chargement de la page)
    else:
        form = NumericalGreeksForm()
        # On peut choisir de ne rien calculer au premier chargement pour une page plus propre
        # 'results' reste None, et le template affichera le message "Enter parameters...".

    context = {'form': form, 'results': results}
    return render(request, 'chapter3_greeks/greeks_lab.html', context)