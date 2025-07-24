# File: ql_web_app/chapter6_pricing_range/forms.py
from django import forms
from datetime import date, timedelta

class PriceHistoryForm(forms.Form):
    start_date = forms.DateField(label='Start Date', initial=date.today() - timedelta(days=365))
    end_date = forms.DateField(label='End Date', initial=date.today())
    coupon_rate_pct = forms.FloatField(label="Coupon Rate (%)", initial=2.0)
    maturity_years = forms.IntegerField(label="Maturity (years)", initial=5, min_value=1)