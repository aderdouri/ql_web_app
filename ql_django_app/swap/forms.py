from django import forms

class VanillaSwapForm(forms.Form):
    notional = forms.FloatField(label="Notional", initial=1000000)
    maturity_years = forms.IntegerField(label="Maturity (years)", initial=10, min_value=1)
    fixed_rate_pct = forms.FloatField(label="Fixed Rate (%)", initial=1.5)
    float_spread_bps = forms.FloatField(label="Floating Spread (bps)", initial=0.0)
    curve_rate_pct = forms.FloatField(label="Discount Curve Rate (%)", initial=2.0, help_text="Rate for the flat yield curve.")