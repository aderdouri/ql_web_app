from django import forms
from datetime import date, timedelta

class CapFloorForm(forms.Form):
    # Basic Parameters
    evaluation_date = forms.DateField(
        label="Evaluation Date",
        initial=date(2016, 6, 14),  # calc_date from QuantLib book
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    notional = forms.FloatField(
        label="Notional Amount",
        initial=1000000,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '1000'})
    )
    start_date = forms.DateField(
        label="Start Date",
        initial=date(2016, 6, 14),  # start_date from QuantLib book
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    end_date = forms.DateField(
        label="End Date",
        initial=date(2026, 6, 14),  # end_date from QuantLib book (10 years)
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    # Strike and Market Data
    strike_rate = forms.FloatField(
        label="Strike Rate (%)",
        initial=2.0,  # strike = 0.02 from QuantLib book
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    fixing_date = forms.DateField(
        label="Fixing Date",
        initial=date(2016, 6, 10),  # fixing date from QuantLib book
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    fixing_rate = forms.FloatField(
        label="Fixing Rate (%)",
        initial=0.6556,  # 0.0065560 from QuantLib book
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001'})
    )
    pricing_method = forms.ChoiceField(
        label="Pricing Method",
        choices=[
            ('Constant Volatility', 'Constant Volatility'),
            ('Volatility Surface', 'Volatility Surface')
        ],
        initial='Constant Volatility',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # Volatility Parameters
    constant_volatility = forms.FloatField(
        label="Constant Volatility (%)",
        initial=54.7295,  # 0.547295 from QuantLib book
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
    )
    surface_strike_1 = forms.FloatField(
        label="Surface Strike 1 (%)",
        initial=1.0,  # 0.01 from QuantLib book
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    surface_strike_2 = forms.FloatField(
        label="Surface Strike 2 (%)",
        initial=1.5,  # 0.015 from QuantLib book
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    surface_strike_3 = forms.FloatField(
        label="Surface Strike 3 (%)",
        initial=2.0,  # 0.02 from QuantLib book
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    
    # Zero Rate Term Structure
    zero_rate_1 = forms.FloatField(
        label="1Y Rate (%)",
        initial=0.7795,  # 0.007795 from QuantLib book
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001'})
    )
    zero_rate_2 = forms.FloatField(
        label="2Y Rate (%)",
        initial=0.9599,  # 0.009599 from QuantLib book
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001'})
    )
    zero_rate_3 = forms.FloatField(
        label="3Y Rate (%)",
        initial=1.1203,  # 0.011203 from QuantLib book
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001'})
    )
    zero_rate_4 = forms.FloatField(
        label="4Y Rate (%)",
        initial=1.5068,  # 0.015068 from QuantLib book
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001'})
    )
    zero_rate_5 = forms.FloatField(
        label="5Y Rate (%)",
        initial=1.7583,  # 0.017583 from QuantLib book
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001'})
    )
    zero_rate_6 = forms.FloatField(
        label="6Y Rate (%)",
        initial=1.8998,  # 0.018998 from QuantLib book
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001'})
    )
    zero_rate_7 = forms.FloatField(
        label="7Y Rate (%)",
        initial=2.0080,  # 0.020080 from QuantLib book
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001'})
    )
    zero_rate_8 = forms.FloatField(
        label="8Y Rate (%)",
        initial=2.0080,  # Same as 7Y for simplicity
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001'})
    )
    zero_rate_9 = forms.FloatField(
        label="9Y Rate (%)",
        initial=2.0080,  # Same as 7Y for simplicity
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001'})
    )
    zero_rate_10 = forms.FloatField(
        label="10Y Rate (%)",
        initial=2.0080,  # Same as 7Y for simplicity
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001'})
    )