from django.shortcuts import render
from django.http import JsonResponse
from .forms import EuriborCurveForm
from . import services

def euribor_lab_view(request):
    # Gère la requête POST (AJAX) pour la mise à jour
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = EuriborCurveForm(request.POST)
        if form.is_valid():
            curve_data = services.build_euribor_curves(
                base_spread_bps=form.cleaned_data['base_spread_bps'],
                evaluation_dt=form.cleaned_data['evaluation_dt'],
                simulation_duration_years=form.cleaned_data['simulation_duration_years']
            )
            return JsonResponse(curve_data)
        else:
            return JsonResponse({'error': 'invalid form'}, status=400)

    # Gère la requête GET (chargement initial de la page)
    # ou un POST normal (si JavaScript est désactivé)
    form = EuriborCurveForm(request.POST or None)
    curve_data = None
    
    if form.is_valid():
        eval_dt = form.cleaned_data['evaluation_dt']
        sim_duration = form.cleaned_data['simulation_duration_years']
        base_spread = form.cleaned_data['base_spread_bps']
    else:
        # En cas d'erreur ou de chargement initial, on utilise les valeurs par défaut
        form = EuriborCurveForm() # On s'assure que le formulaire est propre
        eval_dt = form.fields['evaluation_dt'].initial
        sim_duration = form.fields['simulation_duration_years'].initial
        base_spread = form.fields['base_spread_bps'].initial
            
    curve_data = services.build_euribor_curves(
        base_spread_bps=base_spread,
        evaluation_dt=eval_dt,
        simulation_duration_years=sim_duration
    )
    
    context = {'form': form, 'initial_data': curve_data} # On passe les données initiales au template
    return render(request, 'chapter_euribor_curve/euribor_lab.html', context)