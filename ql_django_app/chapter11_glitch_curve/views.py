from django.shortcuts import render
from .forms import InterpolationChoiceForm
from . import services

def glitch_lab_view(request):
    form = InterpolationChoiceForm(request.POST or None)
    
    if form.is_valid():
        interpolation = form.cleaned_data['interpolation_type']
    else:
        form = InterpolationChoiceForm()
        interpolation = form.fields['interpolation_type'].initial
        
    analysis_data = services.analyze_forward_curve_glitch(interpolation_str=interpolation)
    
    context = {'form': form, 'analysis_data': analysis_data}
    return render(request, 'chapter_glitch_curve/glitch_lab.html', context)