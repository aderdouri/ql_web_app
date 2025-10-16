# forms.py

from django import forms
import datetime

class ConventionForm(forms.Form):
    evaluation_date = forms.DateField(
        label="Evaluation Date", 
        initial=datetime.date(2010, 1, 5),
        help_text="Date on which the bond pricing analysis is performed",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    flat_rate = forms.FloatField(
        label="Flat Rate", 
        initial=0.10,
        help_text="Flat interest rate for both forecasting and discounting curves (10% = 0.10)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0.0',
            'max': '1.0'
        })
    )
    
    # Le cœur de l'expérience interactive
    bond_day_count = forms.ChoiceField(
        label="Bond Day Count",
        choices=[
            ('Thirty360', '30/360 (Bond Basis)'),
            ('Actual360', 'Actual/360'),
        ],
        initial='Thirty360',
        help_text="Day-count convention used by the floating rate bond cashflows",
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    curve_day_count = forms.ChoiceField(
        label="Curve Day Count",
        choices=[
            ('Thirty360', '30/360 (Bond Basis)'),
            ('Actual360', 'Actual/360'),
        ],
        initial='Thirty360',
        help_text="Day-count convention used by the yield curve for discounting",
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
