from django import forms
from datetime import date

class CapsFloorsForm(forms.Form):
    """
    A form for pricing caps and floors using QuantLib.
    Based on Chapter 20 example from the book.
    """
    
    # Date Parameters
    evaluation_date = forms.DateField(
        label="Evaluation Date", 
        initial=date(2016, 6, 14),  # Book date: June 14, 2016
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        help_text="The date on which the cap/floor is evaluated (defaults to book date: June 14, 2016)."
    )
    
    # Cap/Floor Parameters
    notional = forms.FloatField(
        label="Notional (USD)", 
        initial=1000000,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text="The principal amount of the cap/floor (1M USD in book example)."
    )
    
    start_date = forms.DateField(
        label="Start Date", 
        initial=date(2016, 6, 14),  # Book date: June 14, 2016
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        help_text="The start date of the cap/floor (defaults to book date: June 14, 2016)."
    )
    
    end_date = forms.DateField(
        label="End Date", 
        initial=date(2026, 6, 14),  # Book date: June 14, 2026 (10 years later)
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        help_text="The end date of the cap/floor (defaults to book date: June 14, 2026)."
    )
    
    strike_rate = forms.FloatField(
        label="Strike Rate (%)", 
        initial=2.0,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text="The strike rate of the cap/floor (2% in book example)."
    )
    
    # Market Data Parameters
    fixing_date = forms.DateField(
        label="Fixing Date", 
        initial=date(2016, 6, 10),  # Book date: June 10, 2016
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        help_text="The fixing date for the first rate (defaults to book date: June 10, 2016)."
    )
    
    fixing_rate = forms.FloatField(
        label="Fixing Rate (%)", 
        initial=0.6556,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text="The fixing rate for the first period (0.6556% in book example)."
    )
    
    # Volatility Parameters
    pricing_method = forms.ChoiceField(
        label="Pricing Method",
        choices=[
            ('constant', 'Constant Volatility'),
            ('surface', 'Volatility Surface')
        ],
        initial='constant',
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text="Choose between constant volatility or volatility surface pricing."
    )
    
    constant_volatility = forms.FloatField(
        label="Constant Volatility (%)", 
        initial=54.7295,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text="The constant volatility for pricing (54.7295% in book example)."
    )
    
    # Volatility Surface Parameters (for surface method)
    surface_strike_1 = forms.FloatField(
        label="Surface Strike 1 (%)", 
        initial=1.0,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text="First strike for volatility surface (1%)."
    )
    
    surface_strike_2 = forms.FloatField(
        label="Surface Strike 2 (%)", 
        initial=1.5,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text="Second strike for volatility surface (1.5%)."
    )
    
    surface_strike_3 = forms.FloatField(
        label="Surface Strike 3 (%)", 
        initial=2.0,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text="Third strike for volatility surface (2%)."
    )
    
    # Term Structure Parameters
    zero_rate_1 = forms.FloatField(
        label="Zero Rate 1 (%)", 
        initial=0.0,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text="Zero rate for 3 months (0%)."
    )
    
    zero_rate_2 = forms.FloatField(
        label="Zero Rate 2 (%)", 
        initial=0.6616,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text="Zero rate for 6 months (0.6616%)."
    )
    
    zero_rate_3 = forms.FloatField(
        label="Zero Rate 3 (%)", 
        initial=0.7049,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text="Zero rate for 9 months (0.7049%)."
    )
    
    zero_rate_4 = forms.FloatField(
        label="Zero Rate 4 (%)", 
        initial=0.7795,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text="Zero rate for 1 year (0.7795%)."
    )
    
    zero_rate_5 = forms.FloatField(
        label="Zero Rate 5 (%)", 
        initial=0.9599,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text="Zero rate for 3 years (0.9599%)."
    )
    
    zero_rate_6 = forms.FloatField(
        label="Zero Rate 6 (%)", 
        initial=1.1203,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text="Zero rate for 5 years (1.1203%)."
    )
    
    zero_rate_7 = forms.FloatField(
        label="Zero Rate 7 (%)", 
        initial=1.5068,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text="Zero rate for 10 years (1.5068%)."
    )
    
    zero_rate_8 = forms.FloatField(
        label="Zero Rate 8 (%)", 
        initial=1.7583,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text="Zero rate for 15 years (1.7583%)."
    )
    
    zero_rate_9 = forms.FloatField(
        label="Zero Rate 9 (%)", 
        initial=1.8998,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text="Zero rate for 20 years (1.8998%)."
    )
    
    zero_rate_10 = forms.FloatField(
        label="Zero Rate 10 (%)", 
        initial=2.0080,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text="Zero rate for 30 years (2.0080%)."
    )