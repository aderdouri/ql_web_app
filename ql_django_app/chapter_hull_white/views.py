# File: ql_web_app/chapter_hull_white/views.py

from django.shortcuts import render
from . import services
# Import both form classes from your forms.py file
from .forms import CalibrationForm, HullWhiteSimulationForm

# --- View for the "Short-rate model calibration" Lab ---
def short_rate_calibration_view(request):
    """
    Handles the model calibration lab page.
    This is an interactive lab where the user can choose a model to calibrate.
    """
    form = CalibrationForm(request.POST or None)
    results = None
    
    # We always run a calculation, either with POST data or with initial data
    if form.is_valid():
        model_name = form.cleaned_data['model_name']
    else:
        form = CalibrationForm() # Recreate a clean form on GET or if invalid
        model_name = form.fields['model_name'].initial

    try:
        results = services.calibrate_short_rate_model(model_name)
    except Exception as e:
        # In case of a calculation error, we log it and results will be None
        print(f"ERROR during calibration service call: {e}")
            
    context = {'form': form, 'results': results}
    return render(request, 'chapter_hull_white/short_rate_calibration.html', context)


# --- View for the "Simulating interest rates using Hull White" Lab ---
def hull_white_simulation_view(request):
    """
    Handles the interactive Hull-White simulation lab page.
    It always runs a simulation to display a chart.
    """
    form = HullWhiteSimulationForm(request.POST or None)
    
    # Determine which parameters to use for the simulation
    if form.is_valid():
        # If the form was submitted and is valid, use the user's data
        alpha = form.cleaned_data['alpha']
        sigma = form.cleaned_data['sigma']
        num_paths = form.cleaned_data['num_paths']
        num_years = form.cleaned_data['num_years']
        seed = form.cleaned_data['seed']
    else:
        # On a GET request or if the form is invalid, use the default initial values
        form = HullWhiteSimulationForm()
        alpha = form.fields['alpha'].initial
        sigma = form.fields['sigma'].initial
        num_paths = form.fields['num_paths'].initial
        num_years = form.fields['num_years'].initial
        seed = form.fields['seed'].initial
    
    # Always run the simulation service with the determined parameters
    plot_data = services.simulate_hull_white_paths(
        alpha=alpha,
        sigma=sigma,
        num_paths=num_paths,
        num_years=num_years,
        seed=seed
    )
    
    context = {
        'form': form, 
        'plot_data': plot_data
    }
    # Renders the template for the simulation lab
    return render(request, 'chapter_hull_white/hull_white_lab.html', context)
