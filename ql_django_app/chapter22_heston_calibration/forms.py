from django import forms
import datetime

class VolatilitySmileForm(forms.Form):
    evaluation_date = forms.DateField(
        label="Evaluation Date", 
        initial=datetime.date(2015, 11, 6),
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'value': '2015-11-06'})
    )
    spot_price = forms.FloatField(
        label="Spot Price", 
        initial=659.37, 
        min_value=100, 
        max_value=2000,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'value': '659.37', 'min': 100, 'max': 2000, 'step': 'any'})
    )
    risk_free_rate = forms.FloatField(
        label="Risk-Free Rate (%)", 
        initial=1.0, 
        min_value=0.0, 
        max_value=20.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'value': '1.0', 'min': 0.0, 'max': 20.0, 'step': 'any'})
    )
    dividend_rate = forms.FloatField(
        label="Dividend Rate (%)", 
        initial=0.0, 
        min_value=0.0, 
        max_value=10.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'value': '0.0', 'min': 0.0, 'max': 10.0, 'step': 'any'})
    )

    # Paramètre pour le graphique 2D
    smile_expiry = forms.FloatField(
        label="Smile Expiry (Years)", 
        initial=1.0, 
        min_value=0.1, 
        max_value=2.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'value': '1.0', 'min': 0.1, 'max': 2.0, 'step': 'any'})
    )
    
    # Paramètre pour la calibration
    calibration_expiry_index = forms.IntegerField(
        label="Calibration Expiry (Index)", 
        initial=11, 
        min_value=0, 
        max_value=23,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'value': '11', 'min': 0, 'max': 23})
    )
    
    # Paramètres Heston initiaux
    initial_variance = forms.FloatField(
        label="Initial Variance (v₀)", 
        initial=0.01, 
        min_value=0.001, 
        max_value=0.1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'value': '0.01', 'min': 0.001, 'max': 0.1, 'step': 'any'})
    )
    kappa = forms.FloatField(
        label="Mean Reversion Speed (κ)", 
        initial=0.2, 
        min_value=0.01, 
        max_value=5.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'value': '0.2', 'min': 0.01, 'max': 5.0, 'step': 'any'})
    )
    theta = forms.FloatField(
        label="Long-term Variance (θ)", 
        initial=0.02, 
        min_value=0.001, 
        max_value=0.1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'value': '0.02', 'min': 0.001, 'max': 0.1, 'step': 'any'})
    )
    sigma = forms.FloatField(
        label="Vol of Vol (σ)", 
        initial=0.5, 
        min_value=0.01, 
        max_value=2.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'value': '0.5', 'min': 0.01, 'max': 2.0, 'step': 'any'})
    )
    rho = forms.FloatField(
        label="Correlation (ρ)", 
        initial=-0.75, 
        min_value=-0.99, 
        max_value=0.99,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'value': '-0.75', 'min': -0.99, 'max': 0.99, 'step': 'any'})
    )