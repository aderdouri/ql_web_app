from django.shortcuts import render
from django.http import JsonResponse
from .forms import HestonCalibrationForm
from .services import calibrate_heston_with_scipy
import logging

logger = logging.getLogger(__name__)

def test_solver_view(request):
    return render(request, 'chapter_heston_parameter_calibration/test_solver.html')

def heston_calibration_lab_view(request):
    context = {}
    
    if request.method == 'POST':
        try:
            logger.info(f"POST request received: {request.POST}")
            logger.info(f"Solver method in POST: {request.POST.get('solver_method', 'NOT FOUND')}")
            form = HestonCalibrationForm(request.POST)
            logger.info(f"Form is valid: {form.is_valid()}")
            if form.is_valid():
                logger.info(f"Form data: {form.cleaned_data}")
                logger.info(f"Solver method in cleaned_data: {form.cleaned_data.get('solver_method', 'NOT FOUND')}")
                results = calibrate_heston_with_scipy(form.cleaned_data)
                logger.info(f"Calibration results: {type(results)}")
                logger.info(f"Solver used in results: {results.get('solver_used', 'NOT FOUND')}")
                # Always return JSON for POST requests (AJAX)
                return JsonResponse(results)
            else:
                logger.error(f"Form errors: {form.errors}")
                # Handle form errors - always return JSON for POST
                return JsonResponse({'error': 'Invalid form data.', 'form_errors': form.errors}, status=400)
        except Exception as e:
            logger.error(f"Exception in POST: {str(e)}", exc_info=True)
            # Handle any unexpected errors
            return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)
    else:
        form = HestonCalibrationForm()
        # Ne pas calculer les résultats au chargement initial - laisser l'utilisateur interagir
        results = None
            
    context['form'] = form
    context['results'] = results
    return render(request, 'chapter_heston_parameter_calibration/heston_calibration_lab.html', context)