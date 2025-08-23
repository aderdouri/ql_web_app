from django.shortcuts import render
from .forms import ModelChoiceForm
from . import services

def calibration_lab_view(request):
    form = ModelChoiceForm(request.POST or None)
    results = None
    
    if request.method == 'POST' and form.is_valid():
        model_name = form.cleaned_data['model_name']
        try:
            results = services.calibrate_short_rate_model(model_name)
        except Exception as e:
        
            print(f"ERROR during calibration: {e}")
        
    
    context = {'form': form, 'results': results}
    return render(request, 'chapter_calibration/calibration_lab.html', context)