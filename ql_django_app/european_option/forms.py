# File: ql_web_app/european_option/forms.py (FINAL AND COMPLETE CODE)

from django import forms
from datetime import date

class EuropeanOptionForm(forms.Form):
    """
    Form for entering the parameters of a European option, including the choice of pricing engine.
    """
    
    # --- Instrument Parameters ---
    
    OPTION_TYPE_CHOICES = [('Call', 'Call'), ('Put', 'Put')]
    option_type = forms.ChoiceField(
        label='Option Type', 
        choices=OPTION_TYPE_CHOICES,
        help_text="Choose whether it's a Call or Put option."
    )
    
    maturity_date = forms.DateField(
        label='Maturity Date', 
        initial=date(2016, 1, 15),
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="The expiration date of the option."
    )
    
    spot_price = forms.FloatField(
        label='Spot Price', 
        initial=127.62,
        help_text="Current market price of the underlying asset."
    )
    
    strike_price = forms.FloatField(
        label='Strike Price', 
        initial=130,
        help_text="The price at which the option can be exercised."
    )
    
    # --- Market Parameters ---

    volatility = forms.FloatField(
        label='Volatility (%)', 
        initial=20.0,
        help_text="Annualized volatility of the asset. E.g., 20 for 20%."
    )
    
    dividend_rate = forms.FloatField(
        label='Dividend Rate (%)', 
        initial=1.63,
        help_text="Annualized dividend yield of the asset. E.g., 1.63 for 1.63%."
    )
    
    risk_free_rate = forms.FloatField(
        label='Risk-Free Rate (%)', 
        initial=0.1,
        help_text="The risk-free interest rate. E.g., 0.1 for 0.1%."
    )
    
    # --- Engine Selection (Demonstration of Chapter 2) ---
    
    ENGINE_CHOICES = [
        ('AnalyticEuropeanEngine', 'Black-Scholes (Analytic Formula)'),
        ('BinomialCRR', 'Binomial Tree (CRR)'),
        ('BinomialJR', 'Binomial Tree (Jarrow-Rudd)'),
    ]
    
    pricing_engine = forms.ChoiceField(
        label='Pricing Engine',
        choices=ENGINE_CHOICES,
        help_text="Choose the mathematical model for valuation. Note: Greeks are only available for the Analytic engine."
    )
    
    binomial_steps = forms.IntegerField(
        label="Binomial Tree Steps",
        initial=200,
        required=False,
        help_text="Number of steps for binomial models (higher is more accurate but slower)."
    )