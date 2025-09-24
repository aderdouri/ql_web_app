# chapter2_instruments/forms.py

from django import forms
import QuantLib as ql

# Option type choices
OPTION_TYPE_CHOICES = [
    ('call', 'Call'),
    ('put', 'Put')
]

# Pricing engine choices
PRICING_ENGINE_CHOICES = [
    ('black_scholes', 'Black-Scholes Analytic'),
    ('heston', 'Heston Model'),
    ('monte_carlo', 'Monte Carlo')
]

class OptionPricingForm(forms.Form):
    # Basic option parameters
    underlying_price = forms.FloatField(
        label="Underlying Price (S)",
        initial=100.0,
        min_value=0.01,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': '100.0'
        })
    )
    
    strike_price = forms.FloatField(
        label="Strike Price (K)",
        initial=100.0,
        min_value=0.01,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': '100.0'
        })
    )
    
    risk_free_rate = forms.FloatField(
        label="Risk-free Rate (r)",
        initial=0.01,
        min_value=0.0,
        max_value=1.0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.001',
            'placeholder': '0.01'
        })
    )
    
    volatility = forms.FloatField(
        label="Volatility (σ)",
        initial=0.20,
        min_value=0.001,
        max_value=2.0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.001',
            'placeholder': '0.20'
        })
    )
    
    evaluation_date = forms.DateField(
        label="Evaluation Date (t₀)",
        initial="2014-03-07",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'value': '2014-03-07'
        })
    )
    
    maturity_date = forms.DateField(
        label="Maturity Date (T)",
        initial="2014-06-07",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'value': '2014-06-07'
        })
    )
    
    option_type = forms.ChoiceField(
        label="Option Type",
        choices=OPTION_TYPE_CHOICES,
        initial='call',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    pricing_engine = forms.ChoiceField(
        label="Pricing Engine",
        choices=PRICING_ENGINE_CHOICES,
        initial='black_scholes',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    # Heston model parameters
    v0 = forms.FloatField(
        label="Initial Variance (v₀)",
        initial=0.04,
        min_value=0.001,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.001',
            'placeholder': '0.04'
        }),
        required=False
    )
    
    kappa = forms.FloatField(
        label="Mean Reversion Speed (κ)",
        initial=0.1,
        min_value=0.001,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.001',
            'placeholder': '0.1'
        }),
        required=False
    )
    
    theta = forms.FloatField(
        label="Long-term Variance (θ)",
        initial=0.01,
        min_value=0.001,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.001',
            'placeholder': '0.01'
        }),
        required=False
    )
    
    sigma = forms.FloatField(
        label="Volatility of Variance (σ)",
        initial=0.05,
        min_value=0.001,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.001',
            'placeholder': '0.05'
        }),
        required=False
    )
    
    rho = forms.FloatField(
        label="Correlation (ρ)",
        initial=-0.75,
        min_value=-1.0,
        max_value=1.0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': '-0.75'
        }),
        required=False
    )
    
    # Monte Carlo parameters
    time_steps = forms.IntegerField(
        label="Time Steps",
        initial=20,
        min_value=1,
        max_value=1000,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '20'
        }),
        required=False
    )
    
    required_samples = forms.IntegerField(
        label="Required Samples",
        initial=100000,
        min_value=1000,
        max_value=1000000,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '100000'
        }),
        required=False
    )
    
    
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Validate that maturity date is after evaluation date
        eval_date = cleaned_data.get('evaluation_date')
        maturity_date = cleaned_data.get('maturity_date')
        
        if eval_date and maturity_date and maturity_date < eval_date:
            raise forms.ValidationError("Maturity date must be after or equal to evaluation date.")
        
        return cleaned_data