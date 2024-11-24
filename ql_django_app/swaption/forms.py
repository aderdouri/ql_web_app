from django import forms

class SwaptionForm(forms.Form):
    OPTION_TYPES = [
        ('Call', 'Call'),
        ('Put', 'Put'),
    ]

    option_type = forms.ChoiceField(label='Option Type', choices=OPTION_TYPES)
    strike = forms.FloatField(label='Strike Rate (%)', initial=5.0)
    maturity = forms.IntegerField(label='Maturity (Years)', initial=1)
    tenor = forms.IntegerField(label='Swap Tenor (Years)', initial=5)
    notional = forms.FloatField(label='Notional Amount', initial=1000000)
    fixed_rate = forms.FloatField(label='Fixed Rate (%)', initial=5.0)
    volatility = forms.FloatField(label='Volatility (%)', initial=20.0)