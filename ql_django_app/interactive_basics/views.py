# File: ql_web_app/interactive_basics/views.py
from django.shortcuts import render
from django.http import JsonResponse
import json
from .forms import CreateDateForm, AddPeriodForm, AdvanceBusinessDaysForm, ScheduleForm, InterestRateForm
from . import services

# --- Vue Principale (pour afficher la page) ---
def date_lab_view(request):
    context = {
        'create_date_form': CreateDateForm(),
        'add_period_form': AddPeriodForm(),
        'advance_days_form': AdvanceBusinessDaysForm(),
        'schedule_form': ScheduleForm(),
        'interest_rate_form': InterestRateForm(),
    }
    return render(request, 'interactive_basics/date_lab.html', context)

# --- Vues "API" pour les calculs en arrière-plan ---

def api_create_date(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = CreateDateForm(data)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            cleaned_data['month'] = int(cleaned_data['month'])
            result = services.create_ql_date(cleaned_data)
            return JsonResponse(result)
        else:
            # ==============================================================================
            # CORRECTION : On renvoie les erreurs de validation spécifiques du formulaire
            # ==============================================================================
            return JsonResponse({'status': 'error', 'form_errors': form.errors.as_json()}, status=400)
    return JsonResponse({'status': 'error', 'result': 'Invalid request method.'}, status=400)

def api_add_period(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = AddPeriodForm(data)
        if form.is_valid():
            result = services.add_ql_period(form.cleaned_data)
            return JsonResponse(result)
        else:
            return JsonResponse({'status': 'error', 'form_errors': form.errors.as_json()}, status=400)
    return JsonResponse({'status': 'error', 'result': 'Invalid request method.'}, status=400)

def api_advance_days(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = AdvanceBusinessDaysForm(data)
        if form.is_valid():
            result = services.calculate_calendar_dates(form.cleaned_data)
            return JsonResponse(result)
        else:
            return JsonResponse({'status': 'error', 'form_errors': form.errors.as_json()}, status=400)
    return JsonResponse({'status': 'error', 'result': 'Invalid request method.'}, status=400)
    
def api_create_schedule(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = ScheduleForm(data)
        if form.is_valid():
            result = services.create_schedule(form.cleaned_data)
            return JsonResponse(result)
        else:
            return JsonResponse({'status': 'error', 'form_errors': form.errors.as_json()}, status=400)
    return JsonResponse({'status': 'error', 'result': 'Invalid request method.'}, status=400)

def api_create_rate(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = InterestRateForm(data)
        if form.is_valid():
            result = services.create_interest_rate(form.cleaned_data)
            return JsonResponse(result)
        else:
            return JsonResponse({'status': 'error', 'form_errors': form.errors.as_json()}, status=400)
    return JsonResponse({'status': 'error', 'result': 'Invalid request method.'}, status=400)