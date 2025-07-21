from django.shortcuts import render
from .forms import DateForm, PeriodForm, CalendarForm
from . import services

def interactive_lab_view(request):
    context = {}
    
    # Initialiser tous les formulaires
    date_form = DateForm()
    period_form = PeriodForm()
    calendar_form = CalendarForm()

    try:
        if request.method == 'POST':
            # Déterminer quel formulaire a été soumis
            if 'create_date_btn' in request.POST:
                date_form = DateForm(request.POST)
                if date_form.is_valid():
                    d = date_form.cleaned_data
                    context['date_result'] = services.create_date_from_form(d['day'], d['month'], d['year'])
            
            elif 'add_period_btn' in request.POST:
                period_form = PeriodForm(request.POST)
                if period_form.is_valid():
                    p = period_form.cleaned_data
                    context['period_result'] = services.add_period_from_form(p['start_date_str'], p['quantity'], p['unit'])

            elif 'advance_calendar_btn' in request.POST:
                calendar_form = CalendarForm(request.POST)
                if calendar_form.is_valid():
                    c = calendar_form.cleaned_data
                    context['calendar_result'] = services.advance_with_calendar_from_form(c['start_date_str'], c['period_days'], c['calendar'])
    except Exception as e:
        context['error'] = f"QuantLib Error: {e}"

    context['date_form'] = date_form
    context['period_form'] = period_form
    context['calendar_form'] = calendar_form
    
    return render(request, 'interactive_basics/lab.html', context)