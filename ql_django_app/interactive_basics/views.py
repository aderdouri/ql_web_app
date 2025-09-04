# interactive_basics/views.py

from django.shortcuts import render
from .forms import QuantLibBasicsForm
from . import services

def basics_lab_view(request):
    form = QuantLibBasicsForm(request.POST or None)
    context = {'form': form}

    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        action = request.POST.get('action') # Get which button was clicked
        
        results = {}
        if action == 'run_date' and all(k in data for k in ['date_day', 'date_month', 'date_year']):
            results['date_results'] = services.process_date_module(data['date_day'], int(data['date_month']), data['date_year'])
        
        if action == 'run_calendar' and all(k in data for k in ['calendar_start_date', 'calendar_period_days', 'calendar_choice']):
            results['calendar_results'] = services.process_calendar_module(data['calendar_start_date'], data['calendar_period_days'], data['calendar_choice'])
        
        if action == 'run_schedule' and all(k in data for k in ['schedule_effective_date', 'schedule_termination_date', 'schedule_tenor']):
            results['schedule_results'] = services.process_schedule_module(data)

        if action == 'run_interest_rate' and all(k in data for k in ['ir_annual_rate', 'ir_time_years']):
            results['ir_results'] = services.process_interest_rate_module(data)
            
        context['results'] = results

    return render(request, 'interactive_basics/basics_lab.html', context)