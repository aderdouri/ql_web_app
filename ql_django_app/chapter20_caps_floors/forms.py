from django import forms
from datetime import date, timedelta

class CapFloorForm(forms.Form):
    # Basic Parameters
    evaluation_date = forms.DateField(
        label="Evaluation Date", 
        initial=date.today,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    notional = forms.FloatField(
        label="Notional", 
        initial=1000000,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    start_date = forms.DateField(
        label="Start Date", 
        initial=lambda: date.today() + timedelta(days=30),
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    end_date = forms.DateField(
        label="End Date", 
        initial=lambda: date.today() + timedelta(days=30 + 365*5),
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    
    # Strike and Market Data
    strike_rate = forms.FloatField(
        label="Strike Rate (%)", 
        initial=4.0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    fixing_date = forms.DateField(
        label="Fixing Date", 
        initial=lambda: date.today() - timedelta(days=2),
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    fixing_rate = forms.FloatField(
        label="Fixing Rate (%)", 
        initial=3.0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    pricing_method = forms.ChoiceField(
        label="Pricing Method",
        choices=[
            ('constant_volatility', 'Constant Volatility'),
            ('volatility_surface', 'Volatility Surface')
        ],
        initial='constant_volatility',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # Volatility Parameters
    constant_volatility = forms.FloatField(
        label="Constant Volatility (%)", 
        initial=20.0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    surface_strike_1 = forms.FloatField(
        label="Surface Strike 1 (%)", 
        initial=1.0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    surface_strike_2 = forms.FloatField(
        label="Surface Strike 2 (%)", 
        initial=2.0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    surface_strike_3 = forms.FloatField(
        label="Surface Strike 3 (%)", 
        initial=3.0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    # Term Structure
    zero_rate_1 = forms.FloatField(
        label="Zero Rate 1 (%)", 
        initial=2.0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    zero_rate_2 = forms.FloatField(
        label="Zero Rate 2 (%)", 
        initial=2.5,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    zero_rate_3 = forms.FloatField(
        label="Zero Rate 3 (%)", 
        initial=3.0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    zero_rate_4 = forms.FloatField(
        label="Zero Rate 4 (%)", 
        initial=3.5,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    zero_rate_5 = forms.FloatField(
        label="Zero Rate 5 (%)", 
        initial=4.0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    zero_rate_6 = forms.FloatField(
        label="Zero Rate 6 (%)", 
        initial=4.5,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    zero_rate_7 = forms.FloatField(
        label="Zero Rate 7 (%)", 
        initial=5.0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    zero_rate_8 = forms.FloatField(
        label="Zero Rate 8 (%)", 
        initial=5.5,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    zero_rate_9 = forms.FloatField(
        label="Zero Rate 9 (%)", 
        initial=6.0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    zero_rate_10 = forms.FloatField(
        label="Zero Rate 10 (%)", 
        initial=6.5,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )