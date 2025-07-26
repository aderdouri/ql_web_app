from django.shortcuts import render
from .forms import RandomGeneratorForm
from . import services

def random_lab_view(request):
    """
    Manages the "Random Numbers Lab" page.
    It handles both displaying the form and processing the submitted data
    to generate and display random sequences.
    """
    
    # Initialize with an empty form for a GET request, or a populated one for POST
    form = RandomGeneratorForm(request.POST or None)
    results = None
    
    # Process the form only if the method is POST and the form is valid
    if request.method == 'POST' and form.is_valid():
        try:
            # Call the service with the cleaned data from the form
            results = services.generate_random_sequence(
                generator_type=form.cleaned_data['generator_type'],
                num_points=form.cleaned_data['num_points'],
                seed=form.cleaned_data['seed'],
                dimensionality=form.cleaned_data['dimensionality']
            )
        except Exception as e:
            # Handle potential errors from the service, although it's robust
            print(f"Error in random number generation service: {e}")
            # You could add a Django message here if you want
            # messages.error(request, f"Calculation failed: {e}")

    # Prepare the context to be passed to the template
    context = {
        'form': form, 
        'results': results
    }
    
    # Render the final HTML page
    return render(request, 'chapter7_random/random_lab.html', context)