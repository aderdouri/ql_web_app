from django import forms

class ModelChoiceForm(forms.Form):
    MODEL_CHOICES = [
        ('HullWhite', 'Hull-White 1-Factor'),
        ('BlackKarasinski', 'Black-Karasinski'),
        ('G2', 'G2++ 2-Factor'),
    ]
    
    CALIBRATION_TYPE_CHOICES = [
        ('standard', 'Standard Calibration'),
        ('constrained', 'Constrained Calibration (Fixed Reversion)'),
        ('normal_vol', 'Normal Volatility Calibration'),
    ]
    
    model_name = forms.ChoiceField(
        label="Short-Rate Model to Calibrate", 
        choices=MODEL_CHOICES,
        initial='HullWhite',
        help_text="Select a model to fit to the market data.",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    calibration_type = forms.ChoiceField(
        label="Calibration Type",
        choices=CALIBRATION_TYPE_CHOICES,
        initial='standard',
        help_text="Choose the type of calibration to perform.",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    fixed_reversion = forms.FloatField(
        label="Fixed Reversion Rate (for constrained calibration)",
        initial=0.05,
        min_value=0.001,
        max_value=1.0,
        required=False,
        help_text="Mean reversion rate to fix during constrained calibration (only used for Hull-White constrained calibration).",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001'})
    )