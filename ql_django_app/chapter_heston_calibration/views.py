from django.shortcuts import render
from .forms import SmileControlForm
from . import services

def calibration_lab_view(request):
    form = SmileControlForm(request.POST or None)
    results = None
    
    if form.is_valid():
        atm_vol = form.cleaned_data['atm_vol_pct']
        skew = form.cleaned_data['smile_skew']
    else:
        form = SmileControlForm()
        atm_vol = form.fields['atm_vol_pct'].initial
        skew = form.fields['smile_skew'].initial

    try:
        
        results = services.calibrate_heston_and_get_smile(atm_vol, skew)

    except Exception as e:
        results = {'error': str(e)}
    
    context = {'form': form, 'results': results}
    return render(request, 'chapter_heston_calibration/heston_calibration_lab.html', context)