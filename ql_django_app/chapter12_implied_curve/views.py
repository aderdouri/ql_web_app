from django.shortcuts import render
from .forms import SpreadCurveForm
from . import services

def implied_curve_lab_view(request):
    form = SpreadCurveForm(request.POST or None)
    plot_points = None
    
    if form.is_valid():
        eval_dt = form.cleaned_data['evaluation_dt']
        spread = form.cleaned_data['spread_bps']
    else:
        form = SpreadCurveForm()
        eval_dt = form.fields['evaluation_dt'].initial
        spread = form.fields['spread_bps'].initial
            
    plot_points = services.build_spreaded_curve(
        spread_bps=spread,
        evaluation_dt=eval_dt
    )
    
    context = {'form': form, 'plot_points': plot_points}
    return render(request, 'chapter_implied_curve/implied_curve_lab.html', context)