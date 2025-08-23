from django.shortcuts import render
from .forms import ConvergenceForm
from . import services

def convergence_lab_view(request):
    form = ConvergenceForm(request.POST or None)
    results = None
    if request.method == 'POST' and form.is_valid():
        results = services.run_convergence_experiment(
            experiment_type=form.cleaned_data['experiment_type'],
            a=form.cleaned_data['a'],
            sigma=form.cleaned_data['sigma'],
            num_paths=form.cleaned_data['num_paths'],
            seed=form.cleaned_data['seed']
        )
    context = {'form': form, 'results': results}
    return render(request, 'chapter_mc_convergence/convergence_lab.html', context)