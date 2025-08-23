from django import forms
from datetime import date, timedelta

class AmericanOptionForm(forms.Form):
    OPTION_TYPE_CHOICES = [
        ('Call', 'Call'),
        ('Put', 'Put'),
    ]

    option_type = forms.ChoiceField(label='Option Type', choices=OPTION_TYPE_CHOICES)
    maturity_date = forms.DateField(
        label='Maturity Date',
        #initial=date.today() + timedelta(days=365),
        initial=date(2016, 1, 15),
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    spot_price = forms.FloatField(label='Spot Price', initial=127.62)
    strike_price = forms.FloatField(label='Strike Price', initial=130)
    volatility = forms.FloatField(label='Volatility (%)', initial=20)
    dividend_rate = forms.FloatField(label='Dividend Rate (%)', initial=1.63)
    risk_free_rate = forms.FloatField(label='Risk-Free Rate (%)', initial=0.1)
