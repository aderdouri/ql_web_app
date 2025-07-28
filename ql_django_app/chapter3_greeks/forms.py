from django import forms
from datetime import date, timedelta

class NumericalGreeksForm(forms.Form):
    """
    A form for the "Numerical Greeks Lab" that allows specifying
    both the evaluation date and the maturity date.
    """
    
    # 1. Field for the user to choose the calculation date ("as-of" date)
    evaluation_dt = forms.DateField(
        label='Evaluation Date', 
        initial=date(2002, 1, 15), # Default to a historical date
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="The 'as-of' date for the calculation. Think of this as 'today'."
    )
    
    # 2. Field for the maturity date
    maturity_dt = forms.DateField(
        label='Maturity Date', 
        initial=date(2002, 7, 26), # Default to a future date relative to the initial evaluation_dt
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="The expiration date of the option. Must be after the Evaluation Date."
    )
    
    # 3. Standard option parameters
    spot_price = forms.FloatField(label='Spot Price', initial=100.0)
    strike_price = forms.FloatField(label='Strike Price', initial=100.0)
    volatility_pct = forms.FloatField(label='Volatility (%)', initial=20.0)
    risk_free_rate_pct = forms.FloatField(label='Risk-Free Rate (%)', initial=5.0)
    
    # 4. Bump parameter
    bump_size = forms.FloatField(
        label='Spot Bump Size', 
        initial=0.01,
        help_text="The small change to apply to the spot price for the numerical calculation."
    )

    # 5. Custom validation to ensure dates are coherent
    def clean(self):
        cleaned_data = super().clean()
        eval_date = cleaned_data.get("evaluation_dt")
        maturity = cleaned_data.get("maturity_dt")

        if eval_date and maturity:
            # Check that maturity date is after evaluation date
            if maturity <= eval_date:
                raise forms.ValidationError(
                    "The Maturity Date must be after the Evaluation Date."
                )
        return cleaned_data