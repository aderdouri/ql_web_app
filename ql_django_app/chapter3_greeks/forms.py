# File: ql_web_app/chapter3_greeks/forms.py

from django import forms
from datetime import date

class NumericalGreeksForm(forms.Form):
    """
    A form for the "Numerical Greeks Lab".
    It gathers standard European option parameters and the bump size for the calculation.
    """
    
    # --- Standard Option Parameters ---
    # These are used to define the instrument we want to analyze.
    
    maturity_dt = forms.DateField(
        label='Maturity Date', 
        initial=date(2016, 1, 15),
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="The expiration date of the option."
    )
    
    spot_price = forms.FloatField(
        label='Spot Price', 
        initial=100.0,
        help_text="Current market price of the underlying asset."
    )
    
    strike_price = forms.FloatField(
        label='Strike Price', 
        initial=100.0,
        help_text="The price at which the option can be exercised."
    )
    
    volatility_pct = forms.FloatField(
        label='Volatility (%)', 
        initial=20.0,
        help_text="Annualized volatility. E.g., 20.0 for 20%."
    )
    
    risk_free_rate_pct = forms.FloatField(
        label='Risk-Free Rate (%)', 
        initial=5.0,
        help_text="The risk-free interest rate. E.g., 5.0 for 5%."
    )
    
    # --- The key parameter for this chapter's demonstration ---
    
    bump_size = forms.FloatField(
        label='Spot Bump Size', 
        initial=0.01,
        help_text="The small change (e.g., 0.01) to apply to the spot price to calculate the derivative numerically."
    )