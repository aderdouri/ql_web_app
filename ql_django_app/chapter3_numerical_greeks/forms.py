# chapter3_numerical_greeks/forms.py

from django import forms
import QuantLib as ql

# Barrier Type Choices
BARRIER_TYPE_CHOICES = [
    ('up_and_in', 'Up-and-In'),
    ('up_and_out', 'Up-and-Out'),
    ('down_and_in', 'Down-and-In'),
    ('down_and_out', 'Down-and-Out'),
]

# Option Type Choices
OPTION_TYPE_CHOICES = [
    ('call', 'Call'),
    ('put', 'Put'),
]

class NumericalGreeksForm(forms.Form):
    # Barrier Parameters
    barrier_type = forms.ChoiceField(
        label="Barrier Type",
        choices=BARRIER_TYPE_CHOICES,
        initial='up_and_in',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    barrier_level = forms.FloatField(
        label="Barrier Level",
        initial=120.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
    )
    rebate = forms.FloatField(
        label="Rebate",
        initial=0.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
    )
    
    # Option Parameters
    option_type = forms.ChoiceField(
        label="Option Type",
        choices=OPTION_TYPE_CHOICES,
        initial='call',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    strike_price = forms.FloatField(
        label="Strike Price (K)",
        initial=100.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
    )
    
    # Dates
    evaluation_date = forms.DateField(
        label="Evaluation Date",
        initial="2014-10-08",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    maturity_date = forms.DateField(
        label="Maturity Date",
        initial="2015-01-08",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    # Market Parameters
    underlying_price = forms.FloatField(
        label="Underlying Price (u)",
        initial=100.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
    )
    risk_free_rate = forms.FloatField(
        label="Risk-free Rate (r)",
        initial=0.01,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001'})
    )
    volatility = forms.FloatField(
        label="Volatility (σ)",
        initial=0.20,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    
    # Perturbation Parameters
    underlying_perturbation = forms.FloatField(
        label="Underlying perturbation (h₍u₎)",
        initial=0.01,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001'})
    )
    rate_perturbation = forms.FloatField(
        label="Rate perturbation (h₍r₎)",
        initial=0.0001,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.00001'})
    )
    volatility_perturbation = forms.FloatField(
        label="Volatility perturbation (h₍σ₎)",
        initial=0.0001,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.00001'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        evaluation_date = cleaned_data.get('evaluation_date')
        maturity_date = cleaned_data.get('maturity_date')
        barrier_type = cleaned_data.get('barrier_type')
        barrier_level = cleaned_data.get('barrier_level')
        underlying_price = cleaned_data.get('underlying_price')
        
        # Validate maturity date is after evaluation date
        if evaluation_date and maturity_date and maturity_date <= evaluation_date:
            raise forms.ValidationError("Maturity date must be after evaluation date.")
        
        # Validate barrier level based on barrier type
        if barrier_type and barrier_level is not None and underlying_price is not None:
            if barrier_type.startswith('up') and barrier_level <= underlying_price:
                raise forms.ValidationError("For Up barriers, barrier level must be greater than underlying price.")
            elif barrier_type.startswith('down') and barrier_level >= underlying_price:
                raise forms.ValidationError("For Down barriers, barrier level must be less than underlying price.")
        
        return cleaned_data
