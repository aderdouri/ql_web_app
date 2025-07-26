from django import forms
from datetime import date

class EuriborCurveForm(forms.Form):
    evaluation_dt = forms.DateField(
        label='Evaluation Date', 
        initial=date(2012, 12, 11),
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="The 'as-of' date for the market data."
    )
    simulation_duration_years = forms.IntegerField(
        label='Simulation Duration (Years)', 
        initial=4, 
        min_value=1, 
        max_value=25,
        help_text="How many years into the future to plot the curve."
    )
    base_spread_bps = forms.FloatField(
        label="Base Spread (bps)",
        initial=26.0,
        help_text="Assumed spread between Euribor 6M and EONIA."
    )