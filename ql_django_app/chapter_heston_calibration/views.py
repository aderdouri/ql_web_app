from django.shortcuts import render
from .forms import HestonCalibrationForm
from . import services

def heston_calibration_lab_view(request):
    form = HestonCalibrationForm(request.POST or None)
    results = None
    if request.method == 'POST' and form.is_valid():
        initial_params = {
            'v0': form.cleaned_data['v0'],
            'kappa': form.cleaned_data['kappa'],
            'theta': form.cleaned_data['theta'],
            'sigma': form.cleaned_data['sigma'],
            'rho': form.cleaned_data['rho'],
        }
        results = services.run_heston_calibration(
            initial_params=initial_params,
            max_iterations=form.cleaned_data['max_iterations']
        )
    context = {'form': form, 'results': results}
    return render(request, 'chapter_heston_calibration/heston_calibration_lab.html', context)