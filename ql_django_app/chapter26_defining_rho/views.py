
from django.shortcuts import render
from .forms import BlackProcessRhoForm
from .services import analyze_rho_for_black_process

def defining_rho_description_view(request):
    context = {
        'chapter_title': 'Chapter 26: Defining Rho for the Black Process',
        'chapter_description': 'Understanding rho (interest rate sensitivity) calculation in the Black-Scholes framework, with focus on the Black process and challenges in calculating Greeks for different process types.'
    }
    return render(request, 'chapter26_defining_rho/defining_rho_description.html', context)

def defining_rho_lab_view(request):
    """
    Handles the interactive lab for the Black Process Rho glitch.
    """
    context = {
        'chapter_title': 'Chapter 26: Defining Rho for the Black Process',
        'chapter_description': "Explore the rho calculation glitch in QuantLib's BlackProcess. Compare analytical and numerical methods for calculating interest rate sensitivity.",
        'chapter_icon': 'bi bi-tools'
    }
    
    if request.method == 'POST':
        form = BlackProcessRhoForm(request.POST)
        if form.is_valid():
            results = analyze_rho_for_black_process(form.cleaned_data)
        else:
            results = None
    else:
        form = BlackProcessRhoForm()
        initial_data = {key: field.initial for key, field in form.fields.items()}
        results = analyze_rho_for_black_process(initial_data)
            
    context['form'] = form
    context['results'] = results
        
    return render(request, 'chapter26_defining_rho/rho_glitch_lab.html', context)

def rho_glitch_lab_view(request):
    """
    Handles the interactive lab for the Black Process Rho glitch.
    """
    context = {}
    
    if request.method == 'POST':
        form = BlackProcessRhoForm(request.POST)
        if form.is_valid():
            results = analyze_rho_for_black_process(form.cleaned_data)
    else:
        form = BlackProcessRhoForm()
        initial_data = {key: field.initial for key, field in form.fields.items()}
        results = analyze_rho_for_black_process(initial_data)
            
    context['form'] = form
    context['results'] = results
        
    return render(request, 'rho_glitch_lab.html', context)