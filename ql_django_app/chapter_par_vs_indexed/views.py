from django.shortcuts import render
from .forms import ConventionChoiceForm
from . import services

def coupon_lab_view(request):
    # On initialise les variables
    analysis = None
    
    # Si la requête est un POST (l'utilisateur a cliqué sur le bouton)
    if request.method == 'POST':
        form = ConventionChoiceForm(request.POST)
        
        # On vérifie si les données envoyées sont valides
        if form.is_valid():
            # Si oui, on appelle le service avec la NOUVELLE donnée du formulaire
            convention = form.cleaned_data['business_day_convention']
            analysis = services.analyze_coupon_details(convention_str=convention)
    
    # Si la requête est un GET (premier chargement de la page)
    else:
        form = ConventionChoiceForm()
        # On effectue un premier calcul avec la valeur par défaut pour afficher un résultat
        convention = form.fields['business_day_convention'].initial
        analysis = services.analyze_coupon_details(convention_str=convention)

    # On prépare le contexte et on rend la page
    context = {'form': form, 'analysis': analysis}
    return render(request, 'chapter_par_vs_indexed/coupon_lab.html', context)