from django import forms
from datetime import date

class CurveLabForm(forms.Form):
    """
    A form to control the parameters for the Term Structures Lab.
    It allows selecting both the evaluation date and the curve interpolation method.
    """
    
    INTERPOLATION_CHOICES = [
        ('log_cubic', 'Log-Cubic Discount'),
        ('linear_zero', 'Linear Zero Rates'),
        ('cubic_zero', 'Cubic Zero Rates'),
        ('flat_forward', 'Flat Forward Rates'),
    ]
    
    evaluation_dt = forms.DateField(
        label='Evaluation Date', 
        initial=date(2015, 1, 15), # Default date from the first notebook
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Changes the reference date for the 'Relative' curve."
    )
    
    interpolation_type = forms.ChoiceField(
        label='Interpolation Method', 
        choices=INTERPOLATION_CHOICES,
        initial='log_cubic', # Default method
        help_text="Select the algorithm used to build the curve from market instruments."
    )