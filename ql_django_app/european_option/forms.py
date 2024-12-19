from django import forms

class EuropeanOptionForm(forms.Form):
    OPTION_TYPE_CHOICES = [
        ('Call', 'Call'),
        ('Put', 'Put'),
    ]

    option_type = forms.ChoiceField(label='Option Type', choices=OPTION_TYPE_CHOICES)
    maturity_date = forms.DateField(label='Maturity Date', widget=forms.DateInput(attrs={'type': 'date'}))
    spot_price = forms.FloatField(label='Spot Price', min_value=0)
    strike_price = forms.FloatField(label='Strike Price', min_value=0)
    volatility = forms.FloatField(label='Volatility (%)', min_value=0)
    dividend_rate = forms.FloatField(label='Dividend Rate (%)', min_value=0)
    risk_free_rate = forms.FloatField(label='Risk-Free Rate (%)', min_value=0)