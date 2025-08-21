# File: ql_web_app/swap/forms.py

from django import forms

class VanillaSwapForm(forms.Form):
    """
    A form for pricing a standard Plain Vanilla Interest Rate Swap.
    """
    
    notional = forms.FloatField(
        label="Notional", 
        initial=1000000,
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
        initial=1.5,
        help_text="The rate of the fixed leg. E.g., 1.5 for 1.5%."
    )
    
    # ==============================================================================
    # THE CORRECTION IS HERE: Renamed 'floating_spreads_bps' to 'floating_spread_bps'
    # ==============================================================================
    floating_spread_bps = forms.FloatField(
        label="Floating Spread (bps)", 
        initial=0.0,
        help_text="The spread over the floating rate in basis points. E.g., 20 for 0.20%."
    )
    
    discount_curve_rate_pct = forms.FloatField(
        label="Discount Curve Rate (%)", 
        initial=2.0,
        help_text="The flat rate for the discount yield curve, used for both discounting and forecasting."
    )