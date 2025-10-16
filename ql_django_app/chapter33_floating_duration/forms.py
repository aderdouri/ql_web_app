from django import forms
import datetime

class DurationFRNForm(forms.Form):
    evaluation_date = forms.DateField(
        label="Evaluation Date", 
        initial=datetime.date(2014, 10, 8),
        help_text="Date on which the bond is evaluated"
    )
    forecast_rate = forms.FloatField(
        label="Forecast Rate", 
        initial=0.002,
        help_text="Rate used to forecast future coupon payments"
    )
    yield_rate = forms.FloatField(
        label="Interest Rate", 
        initial=0.002,
        help_text="Bond's interest rate for duration calculation"
    )
    dy = forms.FloatField(
        label="Interest Rate Change", 
        initial=1e-5,
        help_text="Small change in interest rate to test bond sensitivity. Recommended: 1e-05 (0.00001 = 0.001%) for precise calculation, 1e-04 (0.0001 = 0.01%) for standard analysis, or 1e-03 (0.001 = 0.1%) for larger changes."
    )
