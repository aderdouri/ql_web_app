from django.shortcuts import render
from .forms import CurveLabForm
from . import services

def curve_lab_view(request):
    form = CurveLabForm(request.POST or None)
    plot_points = None

    if form.is_valid():
        eval_dt = form.cleaned_data['evaluation_dt']
        interpolation = form.cleaned_data['interpolation_type']
    else:
        form = CurveLabForm()
        eval_dt = form.fields['evaluation_dt'].initial
        interpolation = form.fields['interpolation_type'].initial
            
    plot_points = services.build_and_analyze_curves(
        evaluation_dt=eval_dt,
        interpolation_str=interpolation
    )
    
    context = {'form': form, 'plot_points': plot_points}
    return render(request, 'chapter5_curves/curve_lab.html', context)