from django.shortcuts import render
from .forms import DayCountForm
from . import services

def day_count_lab_view(request):
    results = None
    
    # Si la requête est un POST (l'utilisateur a cliqué sur "Analyze")
    if request.method == 'POST':
        form = DayCountForm(request.POST)
        
        # On vérifie si les données envoyées sont valides
        if form.is_valid():
            # Si oui, on appelle le service avec les NOUVELLES données du formulaire.
            # Le service va retourner TOUS les résultats (year_fraction ET plot_points).
            results = services.analyze_day_count_convention(
                convention_str=form.cleaned_data['convention'],
                d1_py=form.cleaned_data['start_date'],
                d2_py=form.cleaned_data['end_date']
            )
    
    # Si la requête est un GET (premier chargement de la page)
    else:
        form = DayCountForm()
        # On n'effectue aucun calcul au départ. 'results' reste None.

    context = {'form': form, 'results': results}
    return render(request, 'chapter_day_count/day_count_lab.html', context)