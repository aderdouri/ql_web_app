from django import forms
from datetime import date

class SpreadCurveForm(forms.Form):
    evaluation_dt = forms.DateField(
        label='Evaluation Date', 
        initial=date(2015, 5, 15),
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="The 'as-of' date for the base curve construction."
    )
    spread_bps = forms.FloatField(
        label="Credit Spread (in basis points)",
        initial=150.0,
        help_text="The spread to add to the base curve."
    )