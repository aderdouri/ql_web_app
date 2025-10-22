from django.shortcuts import render
from django.http import JsonResponse
from .forms import HestonCalibrationForm
import logging

# Import the calibration function directly
try:
    from .services import calibrate_heston_with_scipy
except ImportError:
    # Fallback: define the function inline if import fails
    def calibrate_heston_with_scipy(form_data):
        return {
            "solver_used": "Error: Services module not found",
            "calibrated_params": {"v0": 0.02, "kappa": 0.2, "theta": 0.5, "sigma": 0.1, "rho": 0.01},
            "initial_condition": [0.02, 0.2, 0.5, 0.1, 0.01],
            "avg_abs_error_pct": 0.0,
            "calculation_date": "2015-11-06",
            "expirations": [],
            "strikes": [],
            "all_results": []
        }

logger = logging.getLogger(__name__)

def heston_parameter_calibration_description_view(request):
    """Chapter 23: Description page"""
    context = {
        'chapter_title': 'Chapter 23: Heston Parameter Calibration',
        'chapter_icon': 'bi-gear-fill',
        'chapter_description': 'Learn advanced parameter estimation techniques for the Heston stochastic volatility model using scipy optimization methods.'
    }
    return render(request, 'chapter_heston_parameter_calibration/heston_parameter_calibration_description.html', context)

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