from django import forms
from datetime import date

class CurveConstructionForm(forms.Form):
    """
    A complete form for the interactive Yield Curve Construction Lab.
    """
    
    INTERPOLATION_CHOICES = [
        ('log_cubic', 'Log-Cubic Discount'),
        ('linear_zero', 'Linear Zero Rates'),
        ('cubic_zero', 'Cubic Zero Rates'),
        ('flat_forward', 'Flat Forward Rates'),
    ]
    
    evaluation_dt = forms.DateField(
        label='Evaluation Date', 
        initial=date(2004, 5, 15),
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="The as-of date for the curve construction."
    )
    
    interpolation_type = forms.ChoiceField(
        label='Interpolation Method', 
        choices=INTERPOLATION_CHOICES,
        initial='log_cubic'
    )
    
    # --- Market Rate Inputs ---
    
    depo_6m_rate = forms.FloatField(
        label="6M Deposit Rate (%)", 
        initial=3.63,
        help_text="Short-term market rate."
    )
    
    bond_2y_rate = forms.FloatField(
        label="2Y Bond Coupon (%)", 
        initial=2.25,
        help_text="Coupon of the 2-year benchmark bond."
    )
    
    bond_5y_rate = forms.FloatField(
        label="5Y Bond Coupon (%)", 
        initial=2.75,
        help_text="Coupon of the 5-year benchmark bond."
    )
    
    bond_10y_rate = forms.FloatField(
        label="10Y Bond Coupon (%)", 
        initial=3.50,
        help_text="Coupon of the 10-year benchmark bond."
    )