# File: ql_web_app/chapter_heston_scipy/views.py

from django.shortcuts import render
from .forms import OptimizerChoiceForm
from . import services

def scipy_lab_view(request):
    form = OptimizerChoiceForm(request.POST or None)
    results = None
    
    if request.method == 'POST' and form.is_valid():
        optimizer = form.cleaned_data['optimizer_name']
        try:
            results = services.run_calibration(optimizer)
        except Exception as e:
            # ==============================================================================
            # If the service fails for any reason, create a dictionary with an
            # explicit error message to be displayed in the template.
            # ==============================================================================
            error_message = (
                f"The '{optimizer}' optimizer failed to converge. "
                "This can happen with unconstrained methods like SciPy's Levenberg-Marquardt, "
                "which may explore financially unrealistic parameter values. "
                "Try using 'SciPy Least Squares' which supports bounds for more stability. "
                f"Raw error: {e}"
            )
            results = {'error': error_message}
    
    context = {'form': form, 'results': results}
    return render(request, 'chapter_heston_scipy/scipy_lab.html', context)