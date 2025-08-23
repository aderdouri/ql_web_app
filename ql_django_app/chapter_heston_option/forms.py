from django import forms
from datetime import date

class HestonComparisonForm(forms.Form):
    """
    A form for the Heston vs. BSM lab, including a user-selectable evaluation date.
    """
    
    # --- Date Parameters ---
    evaluation_dt = forms.DateField(
        label='Evaluation Date', 
        initial=date(2015, 5, 8), # Default "today" from the notebook
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="The 'as-of' date for the calculation."
    )
    maturity_dt = forms.DateField(
        label='Maturity Date', 
        initial=date(2016, 1, 15), # A future date relative to the initial evaluation date
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    # --- Standard Option & BSM Parameters ---
    spot_price = forms.FloatField(label='Spot Price', initial=127.62)
    strike_price = forms.FloatField(label='Strike Price', initial=130)
    volatility_pct = forms.FloatField(label='BSM Volatility (%)', initial=20.0, help_text="Constant volatility for the BSM model.")
    dividend_rate_pct = forms.FloatField(label='Dividend Rate (%)', initial=1.63)
    risk_free_rate_pct = forms.FloatField(label='Risk-Free Rate (%)', initial=0.1)

    # --- Heston Model Specific Parameters ---
    v0 = forms.FloatField(label="Heston: v0 (Initial Variance)", initial=0.04)
    kappa = forms.FloatField(label="Heston: Kappa (Reversion Speed)", initial=0.1)
    theta = forms.FloatField(label="Heston: Theta (Long-term Var)", initial=0.04)
    sigma = forms.FloatField(label="Heston: Sigma (Vol of Vol)", initial=0.1)
    rho = forms.FloatField(label="Heston: Rho (Correlation)", initial=-0.75, min_value=-1.0, max_value=1.0)