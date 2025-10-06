from django import forms
from datetime import date

class HestonComparisonForm(forms.Form):
    """
    A form for the Heston vs. BSM lab, matching the book's Chapter 21 exactly.
    """
    
    # --- Date Parameters (matching book) ---
    evaluation_dt = forms.DateField(
        label='Calculation Date', 
        initial=date(2015, 5, 8), # May 8, 2015 from the book
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Today's date for the calculation"
    )
    maturity_dt = forms.DateField(
        label='Maturity Date', 
        initial=date(2016, 1, 15), # January 15, 2016 from the book
        widget=forms.DateInput(attrs={'type': 'date'}),
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
        choices=[('call', 'Call Option'), ('put', 'Put Option')],
        initial='call',
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text="Call: Right to buy | Put: Right to sell"
    )
    
    exercise_type = forms.ChoiceField(
        label='Exercise Type',
        choices=[('european', 'European (Exercise only at maturity)'), ('american', 'American (Exercise anytime)')],
        initial='european',
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text="European: Can only exercise at expiration | American: Can exercise anytime"
    )
    volatility_pct = forms.FloatField(
        label='Stock Volatility (%)', 
        initial=20.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': '20.0'}),
        help_text="How much the stock price fluctuates (higher = more risky)"
    )
    dividend_rate_pct = forms.FloatField(
        label='Dividend Yield (%)', 
        initial=1.63,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '1.63'}),
        help_text="Annual dividend payments as % of stock price"
    )
    risk_free_rate_pct = forms.FloatField(
        label='Risk-Free Interest Rate (%)', 
        initial=0.1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.1'}),
        help_text="Safe investment return rate (like government bonds)"
    )

    # --- Heston Model Parameters (Advanced) ---
    v0 = forms.FloatField(
        label="Initial Variance (v₀)", 
        initial=0.04,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.04'}),
        help_text="Starting volatility level (0.04 = 20% volatility)"
    )
    kappa = forms.FloatField(
        label="Mean Reversion Speed (κ)", 
        initial=0.1,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.1'}),
        help_text="How quickly volatility returns to normal (0.1 = slow)"
    )
    theta = forms.FloatField(
        label="Long-term Variance (θ)", 
        initial=0.04,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.04'}),
        help_text="Normal volatility level (0.04 = 20% volatility)"
    )
    sigma = forms.FloatField(
        label="Volatility of Volatility (σ)", 
        initial=0.1,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.1'}),
        help_text="How much volatility itself changes (0.1 = moderate)"
    )
    rho = forms.FloatField(
        label="Price-Volatility Correlation (ρ)", 
        initial=-0.75,
        min_value=-1.0,
        max_value=1.0,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '-0.75'}),
        help_text="How stock price and volatility move together (-0.75 = opposite)"
    )
    
    # --- Advanced Engine Settings ---
    heston_engine_rate = forms.FloatField(
        label="Integration Accuracy", 
        initial=0.01,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001', 'placeholder': '0.01'}),
        help_text="Calculation precision (0.01 = high accuracy, slower)"
    )
    heston_engine_steps = forms.IntegerField(
        label="Calculation Steps", 
        initial=1000,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1000'}),
        help_text="Number of calculation iterations (1000 = good balance)"
    )