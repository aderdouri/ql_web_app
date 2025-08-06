from django.shortcuts import render
from .forms import HullWhiteForm
from . import services

def hull_white_lab_view(request):
    form = HullWhiteForm(request.POST or None)
    results = None
    
    if request.method == 'POST' and form.is_valid():
        results = services.run_hull_white_simulation(
            a=form.cleaned_data['a'],
            sigma=form.cleaned_data['sigma'],
            forward_rate=form.cleaned_data['forward_rate'] / 100.0,
            length_years=form.cleaned_data['length_years'],
            num_paths=form.cleaned_data['num_paths'],
            timestep=form.cleaned_data['length_years'] * 12 # 12 pas par an
        )
    
    context = {'form': form, 'results': results}
    return render(request, 'chapter_hull_white/hull_white_lab.html', context)