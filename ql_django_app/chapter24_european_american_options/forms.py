from django import forms
from datetime import date

class OptionValuationForm(forms.Form):
    """
    A form for European and American option valuation lab, matching the book's Chapter 24.
    """
    
    # --- Date Parameters (matching book) ---
    evaluation_date = forms.DateField(
        label='Calculation Date', 
        initial=date(2015, 5, 8),
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        help_text="Today's date for the calculation"
    )
    maturity_date = forms.DateField(
        label='Maturity Date', 
        initial=date(2016, 1, 15),
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        help_text="When the option expires"
    )

    # --- Option Parameters (matching book exactly) ---
    spot_price = forms.FloatField(
        label='Current Stock Price ($)', 
        initial=127.62,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '127.62'}),
        help_text="Current market price of the underlying stock"
    )
    strike_price = forms.FloatField(
        label='Strike Price ($)', 
        initial=130.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '130.0'}),
        help_text="Price at which you can buy/sell the stock"
    )
    
    # --- Option Type Parameters ---
    option_type = forms.ChoiceField(
        label='Option Type',
        choices=[('Call', 'Call Option'), ('Put', 'Put Option')],
        initial='Call',
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text="Call: Right to buy | Put: Right to sell"
    )
    
    # --- Market Parameters ---
    volatility = forms.FloatField(
        label='Stock Volatility', 
        initial=0.20,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.20'}),
        help_text="How much the stock price fluctuates (0.20 = 20%)"
    )
    dividend_rate = forms.FloatField(
        label='Dividend Rate', 
        initial=0.0163,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001', 'placeholder': '0.0163'}),
        help_text="Annual dividend payments as decimal (0.0163 = 1.63%)"
    )
    risk_free_rate = forms.FloatField(
        label='Risk-Free Rate', 
        initial=0.001,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001', 'placeholder': '0.001'}),
        help_text="Safe investment return rate (0.001 = 0.1%)"
    )
    
    # --- Binomial Tree Parameters ---
    max_steps = forms.IntegerField(
        label="Max Binomial Steps", 
        initial=200, 
        min_value=10, 
        max_value=500,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '200'}),
        help_text="Number of steps in the binomial tree (higher = more accurate but slower)"
    )
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Validate parameters to avoid negative probability
        spot_price = cleaned_data.get('spot_price')
        strike_price = cleaned_data.get('strike_price')
        volatility = cleaned_data.get('volatility')
        risk_free_rate = cleaned_data.get('risk_free_rate')
        dividend_rate = cleaned_data.get('dividend_rate')
        evaluation_date = cleaned_data.get('evaluation_date')
        maturity_date = cleaned_data.get('maturity_date')
        
        if spot_price and spot_price <= 0:
            raise forms.ValidationError("Spot price must be positive")
        if strike_price and strike_price <= 0:
            raise forms.ValidationError("Strike price must be positive")
        if volatility and volatility <= 0:
            raise forms.ValidationError("Volatility must be positive")
        if volatility and volatility > 5.0:
            raise forms.ValidationError("Volatility too high (max 500%)")
        if risk_free_rate and abs(risk_free_rate) > 1.0:
            raise forms.ValidationError("Risk-free rate too high (max 100%)")
        if dividend_rate and abs(dividend_rate) > 1.0:
            raise forms.ValidationError("Dividend rate too high (max 100%)")
        if evaluation_date and maturity_date and maturity_date <= evaluation_date:
            raise forms.ValidationError("Maturity date must be after calculation date")
        
        return cleaned_data