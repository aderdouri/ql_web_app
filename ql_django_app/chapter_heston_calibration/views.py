from django.shortcuts import render
from .forms import HestonCalibrationForm
from . import services

def calibration_description_view(request):
    """Chapter 23: Description page"""
    context = {
        'chapter_title': 'Chapter 23: Heston Model Parameter Calibration in QuantLib Python & SciPy',
        'chapter_icon': 'bi-gear',
        'chapter_description': 'Learn advanced parameter calibration techniques using QuantLib Python and SciPy optimization methods.'
    }
    return render(request, 'chapter_heston_calibration/heston_calibration_description.html', context)

def calibration_lab_view(request):
    """Chapter 23: Interactive calibration lab page"""
    form = HestonCalibrationForm(request.POST or None)
    results = None
    
    if form.is_valid():
        try:
            # Extract form data
            calibration_data = {
                'spot_price': form.cleaned_data['spot_price'],
                'risk_free_rate_pct': form.cleaned_data['risk_free_rate_pct'],
                'dividend_rate_pct': form.cleaned_data['dividend_rate_pct'],
                'calculation_date': form.cleaned_data['calculation_date'],
                'maturity_date': form.cleaned_data['maturity_date'],
                'strikes': form.cleaned_data['strikes'],
                'volatilities': form.cleaned_data['volatilities'],
                'solver_method': form.cleaned_data['solver_method'],
                'initial_theta': form.cleaned_data['initial_theta'],
                'initial_kappa': form.cleaned_data['initial_kappa'],
                'initial_sigma': form.cleaned_data['initial_sigma'],
                'initial_rho': form.cleaned_data['initial_rho'],
                'initial_v0': form.cleaned_data['initial_v0']
            }
            
            results = services.calibrate_heston_parameters(calibration_data)
            
        except Exception as e:
            results = {'error': str(e)}
    else:
        form = HestonCalibrationForm()

    context = {
        'form': form, 
        'results': results,
        'chapter_title': 'Chapter 23: Interactive Heston Calibration Laboratory',
        'chapter_icon': 'bi-gear',
        'chapter_description': 'Interactive laboratory for Heston model parameter calibration using QuantLib Python and SciPy optimization methods.'
    }
    return render(request, 'chapter_heston_calibration/heston_calibration_lab.html', context)