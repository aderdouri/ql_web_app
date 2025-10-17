from django.shortcuts import render
from django.http import JsonResponse
from .forms import ConvergenceForm
from .services import analyze_hull_white_convergence
import json

def convergence_description_view(request):
    """Description page for Monte Carlo convergence chapter"""
    context = {
        'chapter_title': '16. Thoughts on the convergence of Hull-White model Monte Carlo simulations',
        'chapter_icon': 'bi-cpu',
        'chapter_description': 'Understanding convergence properties and numerical stability in Monte Carlo simulations for Hull-White interest rate models.'
    }
    return render(request, 'chapter_mc_convergence/description.html', context)

def convergence_lab_view(request):
    context = {}
    
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = ConvergenceForm(request.POST)
        if form.is_valid():
            results = analyze_hull_white_convergence(form.cleaned_data)
            return JsonResponse(results)
        else:
            # Debug: afficher les erreurs de validation
            print(f"Form errors: {form.errors}")
            print(f"Form data: {request.POST}")
            return JsonResponse({
                'error': 'Invalid form data.',
                'form_errors': form.errors
            }, status=400)

    # Premier chargement (GET)
    form = ConvergenceForm()
    # On récupère les valeurs initiales du formulaire pour le premier calcul
    initial_data = {key: field.initial for key, field in form.fields.items()}
    results = analyze_hull_white_convergence(initial_data)
    
    context['form'] = form
    if 'error' in results:
        context['error'] = results['error']
    else:
        # On passe les résultats au template pour que le JavaScript puisse les utiliser
        context['results_json'] = json.dumps(results)
        
    return render(request, 'convergence_lab.html', context)