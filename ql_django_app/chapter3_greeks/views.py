# File: ql_web_app/chapter3_greeks/views.py

from django.shortcuts import render
from django.contrib import messages  # Import the Django messaging framework
from .forms import NumericalGreeksForm
from . import services

def greeks_lab_view(request):
    """
    This view manages the "Numerical Greeks Lab" page.
    It handles displaying the form and processing the submitted data to show
    the step-by-step numerical calculation of Delta.
    """
    
    # Initialize with an empty form for a GET request (first visit to the page)
    form = NumericalGreeksForm()
    results = None

    # Check if the user submitted the form (POST request)
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = NumericalGreeksForm(request.POST)
        
        # Check if the form data is valid
        if form.is_valid():
            try:
                # Group all option parameters into a dictionary to pass to the service.
                # This keeps the call to the service clean and organized.
                option_params = {
                    'maturity_dt': form.cleaned_data['maturity_dt'],
                    'spot_price': form.cleaned_data['spot_price'],
                    'strike_price': form.cleaned_data['strike_price'],
                    'volatility_pct': form.cleaned_data['volatility_pct'],
                    'risk_free_rate_pct': form.cleaned_data['risk_free_rate_pct'],
                }
                
                # Get the bump size from the validated form data
                bump_size = form.cleaned_data['bump_size']
                
                # Call our clean service function to perform the calculation
                results = services.calculate_numerical_greeks(option_params, bump_size)

            except Exception as e:
                # ==============================================================================
                # CORRECTION IMPORTANTE : On n'utilise jamais "pass" dans un "except".
                # On affiche toujours une erreur claire à l'utilisateur.
                # ==============================================================================
                messages.error(request, f"An error occurred during the QuantLib calculation: {e}")
        
        else:
            # If the form itself has validation errors, Django will display them automatically.
            # We can add a general warning message.
            messages.warning(request, "The submitted data was invalid. Please correct the errors highlighted in the form.")
            
    # Prepare the context dictionary to pass all necessary data to the template
    context = {
        'form': form, 
        'results': results
    }
    
    # Render the final HTML page using the specified template and context
    return render(request, 'chapter3_greeks/greeks_lab.html', context)