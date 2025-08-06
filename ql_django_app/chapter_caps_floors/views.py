from django.shortcuts import render
from .forms import CapFloorForm
from . import services

def parity_lab_view(request):
    form = CapFloorForm(request.POST or None)
    results = None
    if form.is_valid():
        results = services.analyze_cap_floor_parity(
            length_years=form.cleaned_data['length_years'],
            strike_pct=form.cleaned_data['strike_pct'],
            vol_pct=form.cleaned_data['vol_pct'],
            rate_pct=form.cleaned_data['rate_pct'],
            nominal=form.cleaned_data['nominal']
        )
    context = {'form': form, 'results': results}
    return render(request, 'chapter_caps_floors/parity_lab.html', context)