# Fichier : ql_web_app/interactive_basics/forms.py (VERSION AMÉLIORÉE)

from django import forms

class DateForm(forms.Form):
    day = forms.IntegerField(
        label="Day*",
        initial=31, min_value=1, max_value=31,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm'}) # Ajout des classes CSS
    )
    month = forms.IntegerField(
        label="Month*",
        initial=3, min_value=1, max_value=12,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm'})
    )
    year = forms.IntegerField(
        label="Year*",
        initial=2015,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm'})
    )

class PeriodForm(forms.Form):
    PERIOD_CHOICES = [('Days', 'Days'), ('Weeks', 'Weeks'), ('Months', 'Months'), ('Years', 'Years')]
    
    start_date_str = forms.CharField(
        label="Start Date (DD-MM-YYYY)",
        initial="31-03-2015",
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'})
    )
    quantity = forms.IntegerField(
        label="Add Quantity",
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm'})
    )
    unit = forms.ChoiceField(
        label="Unit",
        choices=PERIOD_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    )

class CalendarForm(forms.Form):
    CALENDAR_CHOICES = [('UnitedStates', 'United States'), ('TARGET', 'TARGET (Europe)'), ('UnitedKingdom', 'United Kingdom')]

    start_date_str = forms.CharField(
        label="Start Date (DD-MM-YYYY)",
        initial="31-03-2015",
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'})
    )
    period_days = forms.IntegerField(
        label="Period (in days)",
        initial=60,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm'})
    )
    calendar = forms.ChoiceField(
        label="Calendar",
        choices=CALENDAR_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    )