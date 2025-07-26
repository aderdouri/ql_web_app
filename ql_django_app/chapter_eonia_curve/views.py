from django.shortcuts import render
from .forms import EoniaCurveForm
from . import services

def eonia_lab_view(request):
    plot_points = None
    
    # Si la requête est un POST, on crée le formulaire avec les données soumises
    if request.method == 'POST':
        form = EoniaCurveForm(request.POST)
        
        # On vérifie si le formulaire est valide
        if form.is_valid():
            # Si oui, on utilise les données "nettoyées" qui sont dans les bons types
            plot_points = services.build_eonia_curve(
                interpolation_type=form.cleaned_data['interpolation_type'],
                include_jump=form.cleaned_data['include_jump'],
                evaluation_dt=form.cleaned_data['evaluation_dt'], # Sera un objet date
                simulation_duration_years=form.cleaned_data['simulation_duration_years']
            )
    
    # Si la requête est un GET (premier chargement), on crée un formulaire vide
    else:
        form = EoniaCurveForm()
        # Et on calcule la courbe avec les valeurs initiales du formulaire
        plot_points = services.build_eonia_curve(
            interpolation_type=form.fields['interpolation_type'].initial,
            include_jump=form.fields['include_jump'].initial,
            evaluation_dt=form.fields['evaluation_dt'].initial, # Est un objet date
            simulation_duration_years=form.fields['simulation_duration_years'].initial
        )
    
    context = {'form': form, 'plot_points': plot_points}
    return render(request, 'chapter_eonia_curve/eonia_lab.html', context)