from django.shortcuts import render
from . import services

def glitch_lab_view(request):
    analysis_data = services.analyze_forward_curve_glitch()
    context = {'analysis_data': analysis_data}
    return render(request, 'chapter_glitch_curve/glitch_lab.html', context)