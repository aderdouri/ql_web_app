# forms.py

from django import forms
import datetime

class BlackFormulaForm(forms.Form):
    # Champ pour choisir l'exemple
    example_type = forms.ChoiceField(
        label="Example Scenario",
        choices=[
            ('treasury', 'Treasury Futures Option'),
            ('gas', 'Natural Gas Futures Option')
        ],
        help_text="Choose a pre-configured example to get started quickly"
    )

    # Paramètres communs
    evaluation_date = forms.DateField(
        label="Evaluation Date",
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(attrs={"type": "date"}),
        help_text="The pricing date (must be before maturity date)"
    )
    maturity_date = forms.DateField(
        label="Maturity Date",
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(attrs={"type": "date"}),
        help_text="The expiration date (must be after evaluation date)"
    )
    
    spot_price = forms.FloatField(
        label="Futures Price (Spot)",
        help_text="Current market price. If spot > strike, call options are valuable"
    )
    strike_price = forms.FloatField(
        label="Strike Price",
        help_text="Exercise price. Compare with spot to see if option is ITM/OTM"
    )
    volatility = forms.FloatField(
        label="Volatility",
        help_text="Price movement risk (0.20 = 20% annual volatility)"
    )
    interest_rate = forms.FloatField(
        label="Interest Rate",
        help_text="Risk-free rate (0.0015 = 0.15% per year)"
    )
    
    option_type = forms.ChoiceField(
        label="Option Type", 
        choices=[('Call', 'Call'), ('Put', 'Put')],
        help_text="Call: right to buy | Put: right to sell"
    )