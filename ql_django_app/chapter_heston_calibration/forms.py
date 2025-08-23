from django import forms

class SmileControlForm(forms.Form):
    atm_vol_pct = forms.FloatField(
        label="ATM Volatility (%)", 
        initial=28.0, 
        help_text="The At-The-Money volatility (center of the smile)."
    )
    smile_skew = forms.FloatField(
        label="Smile Skew", 
        initial=-0.1,
        help_text="Controls the steepness of the smile. Try values from -0.5 to 0.5."
    )