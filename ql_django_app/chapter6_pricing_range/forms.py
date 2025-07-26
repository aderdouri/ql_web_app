from django import forms
from datetime import date

class PriceHistoryForm(forms.Form):
    """
    A form for the "Pricing over a Range of Days" lab.
    """
    
    start_date = forms.DateField(
        label='Simulation Start Date', 
        initial=date(2017, 5, 9), 
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="The starting date for the historical pricing simulation."
    )
    
    end_date = forms.DateField(
        label='Simulation End Date', 
        initial=date(2018, 5, 9), 
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="The ending date for the historical pricing simulation."
    )
    
    coupon_rate_pct = forms.FloatField(
        label="Bond Coupon Rate (%)", 
        initial=1.0,
        help_text="The coupon for the bond that will be priced."
    )
    
    maturity_years = forms.IntegerField(
        label="Bond Maturity (Years)",
        initial=5,
        min_value=1,
        help_text="The total life of the bond from its issue date."
    )