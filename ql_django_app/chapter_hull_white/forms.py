from django import forms

class HullWhiteForm(forms.Form):
    a = forms.FloatField(label="Mean Reversion (a)", initial=0.1)
    sigma = forms.FloatField(label="Volatility (sigma)", initial=0.1)
    forward_rate = forms.FloatField(label="Initial Forward Rate (%)", initial=5.0)
    length_years = forms.IntegerField(label="Simulation Length (Years)", initial=10, min_value=1, max_value=30)
    num_paths = forms.IntegerField(label="Number of Paths to Simulate", initial=10, min_value=1, max_value=1000)