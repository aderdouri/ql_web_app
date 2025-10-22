from django import forms
from datetime import date

class EoniaCurveForm(forms.Form):
    INTERPOLATION_CHOICES = [
        ('log_cubic', 'Log-Cubic Discount (Smooth)'),
        ('flat_forward', 'Flat Forward Rates (Stepped)'),
    ]
    
    evaluation_dt = forms.DateField(
        label='Evaluation Date', 
        initial=date(2012, 12, 11),
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="The 'as-of' date for the market data."
    )
    

    simulation_duration_years = forms.IntegerField(
        label='Simulation Duration (Years)', 
        initial=2, 
        min_value=1, 
        max_value=25,
        help_text="How many years into the future to plot the curve."
    )
    

    interpolation_type = forms.ChoiceField(
        label='Interpolation Method', 
        choices=INTERPOLATION_CHOICES,
        initial='log_cubic'
    )
    include_jump = forms.BooleanField(
        label='Include Turn-of-Year Jump', 
        required=False,
        initial=True
    )