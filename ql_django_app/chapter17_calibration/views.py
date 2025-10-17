from django.shortcuts import render
from .forms import ModelChoiceForm
from . import services

def calibration_description_view(request):
    """Description page for short rate model calibration chapter"""
    model_descriptions = services.get_model_descriptions()
    
    context = {
        'chapter_title': '17. Short interest rate model calibration',
        'chapter_icon': 'bi-sliders',
        'chapter_description': 'Learn how to calibrate short-rate models to market data using various calibration techniques and optimization methods.',
        'model_descriptions': model_descriptions
    }
    return render(request, 'chapter_calibration/description.html', context)

def calibration_lab_view(request):
    """Main calibration laboratory view"""
    form = ModelChoiceForm(request.POST or None)
    results = None
    error_message = None
    
    print(f"DEBUG: Request method: {request.method}")
    print(f"DEBUG: Form is valid: {form.is_valid()}")
    if not form.is_valid():
        print(f"DEBUG: Form errors: {form.errors}")
    
    if request.method == 'POST' and form.is_valid():
        model_name = form.cleaned_data['model_name']
        calibration_type = form.cleaned_data['calibration_type']
        fixed_reversion = form.cleaned_data.get('fixed_reversion', 0.05)
        
        print(f"DEBUG: Calibrating {model_name} with type {calibration_type}")
        
        try:
            results = services.calibrate_short_rate_model(model_name, calibration_type, fixed_reversion)
            print(f"DEBUG: Calibration successful, results: {results is not None}")
        except Exception as e:
            error_message = f"Calibration failed: {str(e)}"
            print(f"ERROR during calibration: {e}")
    
    context = {
        'form': form,
        'results': results,
        'error_message': error_message
    }
    print(f"DEBUG: Context results: {results is not None}")
    return render(request, 'chapter_calibration/calibration_lab.html', context)