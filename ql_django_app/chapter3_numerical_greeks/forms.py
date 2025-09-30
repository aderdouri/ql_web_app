"""
Chapter 3 - Numerical Greeks Lab forms
Complete form with all required fields and validation
"""
from django import forms
import datetime


class NumericalGreeksLabForm(forms.Form):
    """
    Complete form for Chapter 3 Numerical Greeks Lab
    All fields with proper validation and default values
    """
    
    # Barrier Option Parameters
    barrier_type = forms.ChoiceField(
        label="Barrier Type",
        choices=[
            ('UpIn', 'Up-and-In'),
            ('UpOut', 'Up-and-Out'),
            ('DownIn', 'Down-and-In'),
            ('DownOut', 'Down-and-Out')
        ],
        initial='UpIn',
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
        choices=[
            ('Call', 'Call'),
            ('Put', 'Put')
        ],
        initial='Call',
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
        initial=datetime.date(2014, 10, 8),
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    maturity_date = forms.DateField(
        label="Maturity Date",
        initial=datetime.date(2015, 1, 8),
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    # Market Data
    underlying_price = forms.FloatField(
        label="Underlying Price (Spot Price, S)",
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
    h_underlying = forms.FloatField(
        label="Perturbation h for Underlying",
        initial=0.01,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001'})
    )
    
    h_rate = forms.FloatField(
        label="Perturbation h for Rate",
        initial=0.0001,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.00001'})
    )
    
    h_volatility = forms.FloatField(
        label="Perturbation h for Volatility",
        initial=0.0001,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.00001'})
    )
    
    def clean(self):
        """Validate form data"""
        cleaned_data = super().clean()
        
        # Ensure maturity date is after evaluation date
        evaluation_date = cleaned_data.get('evaluation_date')
        maturity_date = cleaned_data.get('maturity_date')
        
        if evaluation_date and maturity_date and maturity_date <= evaluation_date:
            raise forms.ValidationError("Maturity date must be after evaluation date.")
        
        # Auto-adjust barrier level based on barrier type
        barrier_level = cleaned_data.get('barrier_level')
        underlying_price = cleaned_data.get('underlying_price')
        barrier_type = cleaned_data.get('barrier_type')
        
        if barrier_level and underlying_price and barrier_type:
            if barrier_type in ['UpIn', 'UpOut'] and barrier_level <= underlying_price:
                # For Up barriers, set barrier above underlying
                cleaned_data['barrier_level'] = underlying_price * 1.2
            elif barrier_type in ['DownIn', 'DownOut'] and barrier_level >= underlying_price:
                # For Down barriers, set barrier below underlying
                cleaned_data['barrier_level'] = underlying_price * 0.95
        
        return cleaned_data