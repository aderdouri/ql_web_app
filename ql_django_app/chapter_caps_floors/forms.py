from django import forms

class CapFloorForm(forms.Form):
    length_years = forms.IntegerField(label="Length (Years)", initial=5)
    strike_pct = forms.FloatField(label="Strike (%)", initial=4.0)
    vol_pct = forms.FloatField(label="Volatility (%)", initial=20.0)
    rate_pct = forms.FloatField(label="Interest Rate (%)", initial=3.0)
    nominal = forms.FloatField(label="Notional", initial=1000000)