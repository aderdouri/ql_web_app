from django import forms
from datetime import date

class NumericalGreeksForm(forms.Form):
    evaluation_dt = forms.DateField(label='Evaluation Date', initial=date(2015, 5, 15), widget=forms.DateInput(attrs={'type':'date'}))
    maturity_dt = forms.DateField(label='Maturity Date', initial=date(2016, 1, 15), widget=forms.DateInput(attrs={'type':'date'}))
    spot_price = forms.FloatField(label='Spot Price', initial=100.0)
    strike_price = forms.FloatField(label='Strike Price', initial=100.0)
    volatility_pct = forms.FloatField(label='Volatility (%)', initial=20.0)
    risk_free_rate_pct = forms.FloatField(label='Risk-Free Rate (%)', initial=1.0)

    # ==============================================================================
    # ON AJOUTE UNE RÈGLE DE VALIDATION PERSONNALISÉE
    # ==============================================================================
    def clean(self):
        cleaned_data = super().clean()
        eval_date = cleaned_data.get("evaluation_dt")
        maturity = cleaned_data.get("maturity_dt")

        if eval_date and maturity:
            # On vérifie que la maturité est bien après l'évaluation
            if maturity <= eval_date:
                # Si non, on lève une erreur qui sera affichée sur le formulaire
                raise forms.ValidationError(
                    "The Maturity Date must be after the Evaluation Date."
                )
        return cleaned_data