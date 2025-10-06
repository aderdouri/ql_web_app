from django import forms
from datetime import date

class SmileControlForm(forms.Form):
    atm_vol_pct = forms.FloatField(
        label="ATM Volatility (%)", 
        initial=28.0, 
        help_text="The At-The-Money volatility (center of the smile)."
    )
    smile_skew = forms.FloatField(
        label="Smile Skew", 
        initial=-0.1,
        help_text="Controls the steepness of the smile. Try values from -0.5 to 0.5."
    )

class HestonCalibrationForm(forms.Form):
    """
    Professional Heston model parameter calibration form - Complete implementation
    """
    
    # Market Data
    spot_price = forms.FloatField(
        label='Spot Price ($)', 
        initial=659.37,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        help_text="Current market price of the underlying asset"
    )
    
    risk_free_rate_pct = forms.FloatField(
        label='Risk-Free Rate (%)', 
        initial=1.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        help_text="Annual risk-free interest rate"
    )
    
    dividend_rate_pct = forms.FloatField(
        label='Dividend Rate (%)', 
        initial=0.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        help_text="Annual dividend yield"
    )
    
    # Dates
    calculation_date = forms.DateField(
        label='Calculation Date', 
        initial=date(2015, 11, 6),
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        help_text="Reference date for calculations"
    )
    
    maturity_date = forms.DateField(
        label='Maturity Date', 
        initial=date(2016, 11, 6),
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        help_text="Option expiration date"
    )
    
    # Market Volatility Data
    strikes = forms.CharField(
        label='Strike Prices',
        initial='527.50, 560.46, 593.43, 626.40, 659.37, 692.34, 725.31, 758.28',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        help_text="Comma-separated strike prices (uses notebook data if empty)"
    )
    
    volatilities = forms.CharField(
        label='Market Volatilities (%)',
        initial='37.819, 34.177, 30.394, 27.832, 26.453, 25.916, 25.941, 26.127',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        help_text="Comma-separated implied volatilities (uses notebook data if empty)"
    )
    
    # Solver Method
    solver_method = forms.ChoiceField(
        label='Optimization Method',
        choices=[
            ('ql_lm', 'QuantLib Levenberg-Marquardt'),
            ('scipy_lm', 'SciPy Levenberg-Marquardt'),
            ('scipy_ls', 'SciPy Least Squares'),
            ('scipy_de', 'SciPy Differential Evolution'),
            ('scipy_bh', 'SciPy Basin Hopping')
        ],
        initial='ql_lm',
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text="Choose the optimization algorithm"
    )
    
    # Initial Parameters (default values)
    initial_theta = forms.FloatField(
        label='Initial θ (Long-term Variance)', 
        initial=0.02,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        help_text="Initial guess for long-term variance level"
    )
    
    initial_kappa = forms.FloatField(
        label='Initial κ (Mean Reversion Speed)', 
        initial=0.2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        help_text="Initial guess for mean reversion speed"
    )
    
    initial_sigma = forms.FloatField(
        label='Initial σ (Volatility of Volatility)', 
        initial=0.5,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        help_text="Initial guess for volatility of volatility"
    )
    
    initial_rho = forms.FloatField(
        label='Initial ρ (Correlation)', 
        initial=0.1,
        min_value=-1.0,
        max_value=1.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        help_text="Initial guess for correlation between asset and variance"
    )
    
    initial_v0 = forms.FloatField(
        label='Initial v₀ (Initial Variance)', 
        initial=0.01,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        help_text="Initial guess for initial variance level"
    )
    
    # Quick Scenarios from the book
    scenario_choice = forms.ChoiceField(
        label='Quick Scenarios (from the book)',
        choices=[
            ('', 'Select a scenario...'),
            ('scenario1', 'Scenario 1: (0.02, 0.2, 0.5, 0.1, 0.01) - Expected: θ≈0.1258, κ≈7.88'),
            ('scenario2', 'Scenario 2: (0.07, 0.5, 0.1, 0.1, 0.1) - Expected: θ≈0.0845, κ≈0.0000'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select', 'onchange': 'loadScenario(this.value)'}),
        help_text="Predefined scenarios from the QuantLib Python Cookbook"
    )