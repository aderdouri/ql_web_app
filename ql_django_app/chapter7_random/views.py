# Fichier : ql_web_app/chapter7_random/views.py
from django.shortcuts import render
from .forms import RandomGeneratorForm
from . import services

def random_lab_view(request):
    form = RandomGeneratorForm(request.POST or None)
    results = None
    
    if request.method == 'POST':
        if form.is_valid():
            results = services.generate_random_points(
                generator_type=form.cleaned_data['generator_type'],
                num_points=form.cleaned_data['num_points'],
                seed=form.cleaned_data['seed']
            )
    
    context = {'form': form, 'results': results}
    return render(request, 'chapter7_random/random_lab.html', context)