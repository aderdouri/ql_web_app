
from django import forms

class BondSetupForm(forms.Form):
    coupon_rate_pct = forms.FloatField(label="Coupon Rate (%)", initial=3.0)
    maturity_years = forms.IntegerField(label="Maturity (years)", initial=5)

class MarketUpdateForm(forms.Form):
    new_rate_pct = forms.FloatField(
        label="New Market Rate (%)", 
        initial=2.5,
        help_text="Change this value to see the bond price update automatically."
    )