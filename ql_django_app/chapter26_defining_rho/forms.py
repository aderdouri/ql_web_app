# forms.py

from django import forms
import datetime

class BlackProcessRhoForm(forms.Form):
    evaluation_date = forms.DateField(
        label="Evaluation Date",
        initial=datetime.date(2016, 12, 24),
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(attrs={"type": "date"}),
        help_text="Reference date for all calculations and market data"
    )
    underlying_price = forms.FloatField(
        label="Underlying Price", 
        initial=100.0,
        help_text="Current market price of the underlying asset (e.g., stock price)"
    )
    risk_free_rate = forms.FloatField(
        label="Risk-Free Rate", 
        initial=0.01,
        help_text="Risk-free interest rate (0.01 = 1% annually)"
    )
    volatility = forms.FloatField(
        label="Volatility", 
        initial=0.20,
        help_text="Annualized standard deviation of returns (0.20 = 20%)"
    )
    strike_price = forms.FloatField(
        label="Strike Price", 
        initial=100.0,
        help_text="Exercise price of the option contract"
    )
    days_to_expiry = forms.IntegerField(
        label="Days to Expiry", 
        initial=100,
        help_text="Time to expiration in calendar days"
    )