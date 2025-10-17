from django import forms
import datetime

class HullWhiteForm(forms.Form):
    sigma = forms.FloatField(
        label="σ (Volatility)", 
        initial=0.1,
        help_text="Volatility parameter σ. Higher values increase rate variability and uncertainty.",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01'
        })
    )
    
    a = forms.FloatField(
        label="a (Mean Reversion)", 
        initial=0.1,
        help_text="Mean reversion parameter a. Higher values make rates return to mean faster.",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01'
        })
    )
    
    timestep = forms.IntegerField(
        label="Total Time Steps", 
        initial=360, 
        help_text="e.g., 360 for 30 years monthly",
        widget=forms.NumberInput(attrs={
            'class': 'form-control'
        })
    )
    
    simulation_length = forms.IntegerField(
        label="Simulation Length (Years)", 
        initial=30,
        help_text="Total simulation period in years. Longer periods show more long-term behavior.",
        widget=forms.NumberInput(attrs={
            'class': 'form-control'
        })
    )
    
    forward_rate = forms.FloatField(
        label="Forward Rate", 
        initial=0.05,
        help_text="Constant forward rate for the term structure (e.g., 0.05 = 5%).",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01'
        })
    )
    
    num_paths = forms.IntegerField(
        label="Number of Paths", 
        initial=1000,
        help_text="Number of Monte Carlo paths to generate. More paths = better statistical accuracy.",
        widget=forms.NumberInput(attrs={
            'class': 'form-control'
        })
    )
    
    random_seed = forms.IntegerField(
        label="Random Seed", 
        initial=42,
        help_text="Seed for random number generation. Same seed = reproducible results.",
        widget=forms.NumberInput(attrs={
            'class': 'form-control'
        })
    )
    
    evaluation_date = forms.DateField(
        label="Evaluation Date", 
        initial=datetime.date(2015, 1, 15), 
        widget=forms.HiddenInput()
    )