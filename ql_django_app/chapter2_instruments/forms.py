from django import forms
from datetime import date

class EngineChoiceForm(forms.Form):
    """
    A form for the interactive "Instruments & Engines" lab.
    It allows the user to select a pricing model and option parameters.
    """
    
    # This list defines the choices that will appear in the dropdown menu.
    # The first value ('analytic') is what your code will see.
    # The second value ('Analytic Black-Scholes...') is what the user will see.
    ENGINE_CHOICES = [
        ('analytic', 'Analytic Black-Scholes Formula'),
        ('binomial_crr', 'Binomial Tree (Cox-Ross-Rubinstein, 200 steps)'),
        ('monte_carlo', 'Monte Carlo Simulation (10k paths)'),
    ]

    # The key field for this demonstration: a dropdown menu (ChoiceField)
    engine_choice = forms.ChoiceField(
        label='Pricing Engine', 
        choices=ENGINE_CHOICES,
        help_text="Select the mathematical model to value the option."
    )
    
    # --- Standard option parameters ---
    # These fields define the input boxes for the user.
    
    maturity_dt = forms.DateField(
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
    
    volatility_pct = forms.FloatField(
        label='Volatility (%)', 
        initial=20.0,
        help_text="Annualized volatility of the asset. E.g., 20.0 for 20%."
    )
    
    risk_free_rate_pct = forms.FloatField(
        label='Risk-Free Rate (%)', 
        initial=0.1,
        help_text="The risk-free interest rate. E.g., 0.1 for 0.1%."
    )