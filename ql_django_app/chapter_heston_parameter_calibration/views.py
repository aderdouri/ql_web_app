from django.shortcuts import render

def parameter_calibration_lab(request):
    return render(request, 'chapter_heston_parameter_calibration/parameter_calibration_lab.html')