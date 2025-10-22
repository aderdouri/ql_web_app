from django.shortcuts import render
from .forms import SensitivityForm
from . import services

def sensitivity_lab_view(request):
    form = SensitivityForm(request.POST or None)
    results = None
    
    if form.is_valid():
        shock_type = form.cleaned_data['shock_type']
        shock_size = form.cleaned_data['shock_size_bps']
    else:
        form = SensitivityForm()
        shock_type = form.fields['shock_type'].initial
        shock_size = form.fields['shock_size_bps'].initial
            
    results = services.analyze_sensitivity(
        shock_type=shock_type,
        shock_size_bps=shock_size
    )
    
    context = {'form': form, 'results': results}
    return render(request, 'chapter_sensitivities/sensitivity_lab.html', context)