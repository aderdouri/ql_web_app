from django import forms
from datetime import date

class PricingRangeForm(forms.Form):
    """
    Form for Chapter 6: Pricing over a range of days
    Reproduces exactly the QuantLib Python Cookbook example
    """
    
    # Date range parameters - EXACTLY like the notebook (May 2017 to May 2018)
    start_date = forms.DateField(
        label='Start Date', 
        initial=date(2017, 5, 1), 
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        help_text="The starting date for the pricing range simulation. Default: May 1, 2017 (notebook default)."
    )
    
    end_date = forms.DateField(
        label='End Date', 
        initial=date(2018, 5, 31), 
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        help_text="The ending date for the pricing range simulation. Default: May 31, 2018 (notebook default)."
    )
    
    # Bond parameters (exactly as in the notebook)
    bond_start_date = forms.DateField(
        label='Bond Start Date', 
        initial=date(2016, 2, 8), 
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        help_text="The issue date of the bond to be priced. Default: Feb 8, 2016 (notebook default)."
    )
    
    bond_maturity_years = forms.IntegerField(
        label="Bond Maturity (Years)",
        initial=5,
        min_value=1,
        max_value=30,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text="The total life of the bond from its issue date. Default: 5 years (notebook default)."
    )
    
    coupon_rate = forms.FloatField(
        label="Coupon Rate (%)", 
        initial=1.0,
        min_value=0.0,
        max_value=20.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        help_text="The annual coupon rate for the bond (1.0 = 1%). Default: 1% (notebook default)."
    )
    
    face_value = forms.FloatField(
        label="Face Value",
        initial=100.0,
        min_value=1.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        help_text="The face value (principal) of the bond. Default: 100 (notebook default)."
    )
    
    # Market data parameters
    base_rate = forms.FloatField(
        label="Base Risk-Free Rate (%)",
        initial=0.7,
        min_value=0.0,
        max_value=20.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        help_text="The base risk-free rate for the discount curve (0.7 = 0.7%). Default: 0.7% (notebook default)."
    )
    
    rate_volatility = forms.FloatField(
        label="Rate Volatility (%)",
        initial=0.5,
        min_value=0.0,
        max_value=10.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        help_text="The volatility for generating random rate movements (0.5 = 0.5%). Default: 0.5% (notebook default)."
    )
    
    # Calendar and convention
    calendar = forms.ChoiceField(
        label="Calendar",
        choices=[
            ('TARGET', 'TARGET'),
            ('UnitedStates', 'United States'),
            ('UnitedKingdom', 'United Kingdom'),
        ],
        initial='TARGET',
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="The calendar for business day calculations."
    )
    
    settlement_convention = forms.ChoiceField(
        label="Settlement Convention",
        choices=[
            ('Following', 'Following'),
            ('Preceding', 'Preceding'),
            ('ModifiedFollowing', 'Modified Following'),
        ],
        initial='Following',
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="The settlement convention for business day adjustments."
    )
    
    # Evaluation frequency
    evaluation_frequency = forms.ChoiceField(
        label="Evaluation Frequency",
        choices=[
            ('Daily', 'Daily'),
            ('Weekly', 'Weekly'),
            ('Monthly', 'Monthly'),
        ],
        initial='Daily',
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="How often to evaluate the instrument over the date range."
    )
    
    def get_bond_parameters(self):
        """Get bond parameters for pricing"""
        if self.is_valid():
            return {
                'coupon_rate': self.cleaned_data['coupon_rate_pct'] / 100.0,
                'maturity_years': self.cleaned_data['maturity_years']
            }
        return {
            'coupon_rate': 0.01,  # 1% default
            'maturity_years': 5
        }
    
    def get_simulation_parameters(self):
        """Get simulation date parameters"""
        if self.is_valid():
            return {
                'start_date': self.cleaned_data['start_date'],
                'end_date': self.cleaned_data['end_date']
            }
        return {
            'start_date': date(2017, 5, 9),
            'end_date': date(2018, 5, 9)
        }
    
    def get_discount_curve_rates(self):
        """Get discount curve rates (default values)"""
        return {
            'risk_free_rate': 0.01,  # 1% default
            'spread': 0.005  # 50 bps spread
        }
    
    def get_ois_rates(self):
        """Get OIS rates (default values)"""
        return {
            'ois_rate': 0.005  # 0.5% default
        }
    
    def get_spread(self):
        """Get spread (default values)"""
        return {
            'spread': 0.005  # 50 bps default
        }
    
    def get_fixings(self):
        """Get fixings (default values)"""
        return {
            'fixings': []  # Empty list default
        }