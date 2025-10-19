from django import forms

class RandomNumbersForm(forms.Form):
    """Form for Chapter 7: A note on random numbers and dimensionality"""
    
    # RNG Type
    RNG_TYPE_CHOICES = [
        ('Mersenne Twister', 'Mersenne Twister'),
        ('Inverse Cumulative Normal', 'Inverse Cumulative Normal'),
        ('Sobol', 'Sobol'),
    ]
    
    rng_type = forms.ChoiceField(
        label='Random Number Generator',
        choices=RNG_TYPE_CHOICES,
        initial='Mersenne Twister',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'title': 'Choice of random number generator'
        })
    )
    
    # Seed
    seed = forms.IntegerField(
        label='Random Seed',
        initial=42,
        min_value=0,
        max_value=999999,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'title': 'Random seed for reproducibility'
        })
    )
    
    # Number of simulations
    num_simulations = forms.IntegerField(
        label='Number of Simulations',
        initial=10000,
        min_value=10,
        max_value=1000000,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'title': 'Number of random samples to generate'
        })
    )
    
    # Dimensionality
    dimensionality = forms.IntegerField(
        label='Dimensionality',
        initial=1,
        min_value=1,
        max_value=10,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'title': 'Number of dimensions (1D, 2D, 5D, etc.)'
        })
    )
    
    # Option Parameters
    maturity = forms.FloatField(
        label='Maturity (years)',
        initial=1.0,
        min_value=0.01,
        max_value=10.0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'title': 'Option maturity in years'
        })
    )
    
    strike = forms.FloatField(
        label='Strike Price',
        initial=100.0,
        min_value=1.0,
        max_value=1000.0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'title': 'Strike price of the option'
        })
    )
    
    spot = forms.FloatField(
        label='Spot Price',
        initial=100.0,
        min_value=1.0,
        max_value=1000.0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'title': 'Initial spot price'
        })
    )
    
    volatility = forms.FloatField(
        label='Volatility',
        initial=0.20,
        min_value=0.01,
        max_value=2.0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'title': 'Volatility of the underlying asset'
        })
    )
    
    risk_free_rate = forms.FloatField(
        label='Risk-Free Rate',
        initial=0.05,
        min_value=0.0,
        max_value=1.0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.001',
            'title': 'Risk-free interest rate'
        })
    )
    
    def get_rng_parameters(self):
        """Get RNG parameters from form data"""
        if self.is_valid():
            return {
                'rng_type': self.cleaned_data.get('rng_type', 'Mersenne Twister'),
                'seed': self.cleaned_data.get('seed', 42),
                'num_simulations': self.cleaned_data.get('num_simulations', 10000),
                'dimensionality': self.cleaned_data.get('dimensionality', 1),
            }
        return {
            'rng_type': 'Mersenne Twister',
            'seed': 42,
            'num_simulations': 10000,
            'dimensionality': 1,
        }
    
    def get_option_parameters(self):
        """Get option parameters from form data"""
        if self.is_valid():
            return {
                'maturity': self.cleaned_data.get('maturity', 1.0),
                'strike': self.cleaned_data.get('strike', 100.0),
                'spot': self.cleaned_data.get('spot', 100.0),
                'volatility': self.cleaned_data.get('volatility', 0.20),
                'risk_free_rate': self.cleaned_data.get('risk_free_rate', 0.05),
            }
        return {
            'maturity': 1.0,
            'strike': 100.0,
            'spot': 100.0,
            'volatility': 0.20,
            'risk_free_rate': 0.05,
        }


