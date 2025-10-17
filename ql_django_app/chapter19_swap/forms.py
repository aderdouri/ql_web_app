from django import forms
from datetime import date

class VanillaSwapForm(forms.Form):
    """
    A form for pricing a standard Plain Vanilla Interest Rate Swap.
    Based on Chapter 19 example from the book.
    """
    
    notional = forms.FloatField(
        label="Notional (USD)", 
        initial=10000000,
        help_text="The principal amount of the swap (10M USD in book example)."
    )
    
    maturity_years = forms.IntegerField(
        label="Maturity (years)", 
        initial=10,
        min_value=1,
        help_text="The total length of the swap contract (10 years in book example)."
    )
    
    fixed_rate_pct = forms.FloatField(
        label="Fixed Rate (%)", 
        initial=2.5,
        help_text="The rate of the fixed leg (2.5% in book example)."
    )
    
    floating_spread_bps = forms.FloatField(
        label="Floating Spread (bps)", 
        initial=40.0,
        help_text="The spread over the floating rate in basis points (40 bps = 0.4% in book example)."
    )
    
    risk_free_rate_pct = forms.FloatField(
        label="Risk-Free Rate (%)", 
        initial=1.0,
        help_text="The flat rate for the discount yield curve (1% in book example)."
    )
    
    libor_rate_pct = forms.FloatField(
        label="Libor Rate (%)", 
        initial=2.0,
        help_text="The flat rate for the Libor curve (2% in book example)."
    )
    
    evaluation_date = forms.DateField(
        label="Evaluation Date", 
        initial=date.today(),
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        help_text="The date on which the swap is evaluated (defaults to today)."
    )