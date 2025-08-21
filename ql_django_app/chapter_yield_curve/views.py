# File: ql_web_app/chapter10_treasury_curve/views.py
from django.shortcuts import render
from .forms import CurveConstructionForm
from . import services

def curve_lab_view(request):
    form = CurveConstructionForm(request.POST or None)
    plot_points = None
    
    if form.is_valid():
        eval_dt = form.cleaned_data['evaluation_dt']
        interpolation = form.cleaned_data['interpolation_type']
        # Create a dictionary with the market rates from the form
        market_rates = {
            'depo_6m_rate': form.cleaned_data['depo_6m_rate'],
            'bond_2y_rate': form.cleaned_data['bond_2y_rate'],
            'bond_5y_rate': form.cleaned_data['bond_5y_rate'],
            'bond_10y_rate': form.cleaned_data['bond_10y_rate'],
        }
    else:
        form = CurveConstructionForm() # Create a clean form for GET or invalid POST
        eval_dt = form.fields['evaluation_dt'].initial
        interpolation = form.fields['interpolation_type'].initial
        # Create a dictionary with the default rates from the form
        market_rates = {
            'depo_6m_rate': form.fields['depo_6m_rate'].initial,
            'bond_2y_rate': form.fields['bond_2y_rate'].initial,
            'bond_5y_rate': form.fields['bond_5y_rate'].initial,
            'bond_10y_rate': form.fields['bond_10y_rate'].initial,
        }
            
    plot_points = services.build_treasury_curve(
        evaluation_dt=eval_dt,
        interpolation_str=interpolation,
        market_rates=market_rates # Pass the rates to the service
    )
    
    context = {
        'form': form, 
        'plot_points': plot_points, 
        'eval_date': eval_dt.isoformat()
    }
    return render(request, 'chapter_yield_curve/curve_lab.html', context)