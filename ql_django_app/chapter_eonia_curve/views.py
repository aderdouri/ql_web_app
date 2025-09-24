from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
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
    """
    Vue principale pour le laboratoire EONIA.
    Affiche le formulaire et les résultats initiaux.
    """
    form = EoniaCurveForm()
    
    context = {
        'form': form,
        'page_title': 'EONIA Curve Bootstrapping',
        'page_description': 'Construction de la courbe de discount EONIA selon le livre QuantLib'
    }
    
    return render(request, 'chapter_eonia_curve/eonia_lab.html', context)

@csrf_exempt
def eonia_run_api(request):
    """
    API endpoint pour exécuter les calculs EONIA.
    Version simplifiée qui fonctionne à coup sûr.
    """
    try:
        print(f"DEBUG: Content-Type: {request.content_type}")
        print(f"DEBUG: Method: {request.method}")
        
        # Test simple d'abord
        if request.method == 'GET':
            return JsonResponse({
                'success': True,
                'message': 'API EONIA fonctionne',
                'test': True
            })
        
        # Gérer les données de formulaire
        form = EoniaCurveForm(request.POST)
        
        print(f"DEBUG: Form valid: {form.is_valid()}")
        if not form.is_valid():
            print(f"DEBUG: Form errors: {form.errors}")
            return JsonResponse({
                'success': False,
                'error': 'Données de formulaire invalides',
                'form_errors': form.errors
            })
        
        print("DEBUG: Starting EONIA calculations...")
        
        # Exécuter les calculs avec les paramètres du formulaire
        try:
            # Extraire les paramètres du formulaire
            evaluation_date = form.cleaned_data['evaluation_date'].isoformat()
            simulation_duration_years = form.cleaned_data['simulation_duration_years']
            interpolation_type = form.cleaned_data['interpolation_type']
            include_jump = form.cleaned_data['include_jump']
            settlement_days = form.cleaned_data['settlement_days']
            day_counter = form.cleaned_data['day_counter']
            
            print(f"DEBUG: Using parameters: {evaluation_date}, {simulation_duration_years}, {interpolation_type}, {include_jump}")
            
            # Appeler la fonction avec les paramètres
            results = services.build_eonia_curves_complete(
                evaluation_date=evaluation_date,
                simulation_duration_years=simulation_duration_years,
                interpolation_type=interpolation_type,
                include_jump=include_jump,
                settlement_days=settlement_days,
                day_counter=day_counter
            )
            print(f"DEBUG: EONIA results success: {results.get('success', False)}")
            
            if results.get('success', False):
                # Ajouter les paramètres utilisés
                results['parameters'] = {
                    'evaluation_date': evaluation_date,
                    'simulation_duration_years': simulation_duration_years,
                    'interpolation_type': interpolation_type,
                    'include_jump': include_jump,
                    'settlement_days': settlement_days,
                    'day_counter': day_counter
                }
                
                print("DEBUG: Returning successful JSON response")
                return JsonResponse(results)
            else:
                print(f"DEBUG: EONIA service failed: {results.get('error', 'Unknown error')}")
                return JsonResponse({
                    'success': False,
                    'error': f'Erreur dans les calculs EONIA: {results.get("error", "Unknown error")}'
                })
                
        except Exception as service_error:
            print(f"DEBUG: Service error: {service_error}")
            return JsonResponse({
                'success': False,
                'error': f'Erreur dans les services: {str(service_error)}'
            })
        
    except Exception as e:
        print(f"DEBUG: Exception in eonia_run_api: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'error': f'Erreur générale: {str(e)}'
        })

def eonia_help_view(request):
    """
    Vue d'aide pour le module EONIA.
    Affiche la documentation et les exemples.
    """
    context = {
        'page_title': 'Aide - EONIA Curve Bootstrapping',
        'documentation': {
            'title': 'EONIA Curve Bootstrapping',
            'description': 'Construction de la courbe de discount EONIA à partir des swaps OIS',
            'reference': 'QuantLib Book - Chapter EONIA',
            'instruments': [
                '3 dépôts 1-jour (0, 1, 2 jours de fixing)',
                '4 swaps OIS court terme (1-4 semaines)',
                '5 forwards OIS datés (janvier-juin 2013)',
                '18 swaps OIS long terme (15 mois - 30 ans)'
            ],
            'curve_type': 'PiecewiseLogCubicDiscount',
            'extrapolation': True
        }
    }
    
    return render(request, 'chapter_eonia_curve/eonia_help.html', context)

    """
    Vue principale pour le laboratoire EONIA.
    Affiche le formulaire et les résultats initiaux.
    """
    form = EoniaCurveForm()
    
    context = {
        'form': form,
        'page_title': 'EONIA Curve Bootstrapping',
        'page_description': 'Construction de la courbe de discount EONIA selon le livre QuantLib'
    }
    
    return render(request, 'chapter_eonia_curve/eonia_lab.html', context)

@csrf_exempt
def eonia_run_api(request):
    """
    API endpoint pour exécuter les calculs EONIA.
    Version simplifiée qui fonctionne à coup sûr.
    """
    try:
        print(f"DEBUG: Content-Type: {request.content_type}")
        print(f"DEBUG: Method: {request.method}")
        
        # Test simple d'abord
        if request.method == 'GET':
            return JsonResponse({
                'success': True,
                'message': 'API EONIA fonctionne',
                'test': True
            })
        
        # Gérer les données de formulaire
        form = EoniaCurveForm(request.POST)
        
        print(f"DEBUG: Form valid: {form.is_valid()}")
        if not form.is_valid():
            print(f"DEBUG: Form errors: {form.errors}")
            return JsonResponse({
                'success': False,
                'error': 'Données de formulaire invalides',
                'form_errors': form.errors
            })
        
        print("DEBUG: Starting EONIA calculations...")
        
        # Exécuter les calculs avec les paramètres du formulaire
        try:
            # Extraire les paramètres du formulaire
            evaluation_date = form.cleaned_data['evaluation_date'].isoformat()
            simulation_duration_years = form.cleaned_data['simulation_duration_years']
            interpolation_type = form.cleaned_data['interpolation_type']
            include_jump = form.cleaned_data['include_jump']
            settlement_days = form.cleaned_data['settlement_days']
            day_counter = form.cleaned_data['day_counter']
            
            print(f"DEBUG: Using parameters: {evaluation_date}, {simulation_duration_years}, {interpolation_type}, {include_jump}")
            
            # Appeler la fonction avec les paramètres
            results = services.build_eonia_curves_complete(
                evaluation_date=evaluation_date,
                simulation_duration_years=simulation_duration_years,
                interpolation_type=interpolation_type,
                include_jump=include_jump,
                settlement_days=settlement_days,
                day_counter=day_counter
            )
            print(f"DEBUG: EONIA results success: {results.get('success', False)}")
            
            if results.get('success', False):
                # Ajouter les paramètres utilisés
                results['parameters'] = {
                    'evaluation_date': evaluation_date,
                    'simulation_duration_years': simulation_duration_years,
                    'interpolation_type': interpolation_type,
                    'include_jump': include_jump,
                    'settlement_days': settlement_days,
                    'day_counter': day_counter
                }
                
                print("DEBUG: Returning successful JSON response")
                return JsonResponse(results)
            else:
                print(f"DEBUG: EONIA service failed: {results.get('error', 'Unknown error')}")
                return JsonResponse({
                    'success': False,
                    'error': f'Erreur dans les calculs EONIA: {results.get("error", "Unknown error")}'
                })
                
        except Exception as service_error:
            print(f"DEBUG: Service error: {service_error}")
            return JsonResponse({
                'success': False,
                'error': f'Erreur dans les services: {str(service_error)}'
            })
        
    except Exception as e:
        print(f"DEBUG: Exception in eonia_run_api: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'error': f'Erreur générale: {str(e)}'
        })

def eonia_help_view(request):
    """
    Vue d'aide pour le module EONIA.
    Affiche la documentation et les exemples.
    """
    context = {
        'page_title': 'Aide - EONIA Curve Bootstrapping',
        'documentation': {
            'title': 'EONIA Curve Bootstrapping',
            'description': 'Construction de la courbe de discount EONIA à partir des swaps OIS',
            'reference': 'QuantLib Book - Chapter EONIA',
            'instruments': [
                '3 dépôts 1-jour (0, 1, 2 jours de fixing)',
                '4 swaps OIS court terme (1-4 semaines)',
                '5 forwards OIS datés (janvier-juin 2013)',
                '18 swaps OIS long terme (15 mois - 30 ans)'
            ],
            'curve_type': 'PiecewiseLogCubicDiscount',
            'extrapolation': True
        }
    }
    
    return render(request, 'chapter_eonia_curve/eonia_help.html', context)
