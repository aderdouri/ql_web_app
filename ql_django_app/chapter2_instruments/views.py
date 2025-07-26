from django.shortcuts import render
from django.contrib import messages
from .forms import EngineChoiceForm
from . import services

def pricer_lab_view(request):
    """
    This view manages the "Instruments & Engines" lab page.
    It handles both displaying the form and processing the submitted data.
    """
    
    # Initialize form and results for a GET request (when the user first visits the page)
    form = EngineChoiceForm()
    results = None

    # Check if the form has been submitted (POST request)
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = EngineChoiceForm(request.POST)
        
        # Check if the form is valid (all fields are correct)
        if form.is_valid():
            try:
                # Group all option parameters into a dictionary
                option_params = {
                    'maturity_dt': form.cleaned_data['maturity_dt'],
                    'spot_price': form.cleaned_data['spot_price'],
                    'strike_price': form.cleaned_data['strike_price'],
                    'volatility_pct': form.cleaned_data['volatility_pct'],
                    'risk_free_rate_pct': form.cleaned_data['risk_free_rate_pct'],
                }
                
                # Get the user's choice for the pricing engine
                engine_choice = form.cleaned_data['engine_choice']
                
                # Call our clean service function to perform the calculation
                results = services.price_option_with_selected_engine(engine_choice, option_params)

            except Exception as e:
                # If any error occurs during the QuantLib calculation, display a friendly message
                messages.error(request, f"An error occurred during calculation: {e}")
        
        else:
            # If the form itself has validation errors (e.g., text in a number field)
            messages.warning(request, "The submitted data was invalid. Please check the form.")
            
    # Prepare the context dictionary to pass data to the template
    context = {
        'form': form, 
        'results': results
    }
    
    # Render the final HTML page
    return render(request, 'chapter2_instruments/pricer_lab.html', context)