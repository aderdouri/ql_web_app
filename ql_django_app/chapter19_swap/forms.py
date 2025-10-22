from django import forms
from datetime import date

class VanillaSwapForm(forms.Form):
    """
    A form for pricing a standard Plain Vanilla Interest Rate Swap.
    """
    
    notional = forms.FloatField(
        label="Notional (USD)", 
        initial=10000000,
        help_text="The principal amount of the swap."
    )
    
    maturity_years = forms.IntegerField(
        label="Maturity (years)", 
        initial=10,
        min_value=1,
        help_text="The total length of the swap contract."
    )
    
    fixed_rate_pct = forms.FloatField(
        label="Fixed Rate (%)", 
        initial=2.5,
        help_text="The rate of the fixed leg."
    )
    
    floating_spread_bps = forms.FloatField(
        label="Floating Spread (bps)", 
        initial=40.0,
        help_text="The spread over the floating rate in basis points (40 bps = 0.4%)."
    )
    
    risk_free_rate_pct = forms.FloatField(
        label="Risk-Free Rate (%)", 
        initial=1.0,
        help_text="The flat rate for the discount yield curve."
    )
    
    libor_rate_pct = forms.FloatField(
        label="Libor Rate (%)", 
        initial=2.0,
        help_text="The flat rate for the Libor curve."
    )
    
    evaluation_date = forms.DateField(
        label="Evaluation Date", 
        initial=date.today(),
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        help_text="The date on which the swap is evaluated."
    )