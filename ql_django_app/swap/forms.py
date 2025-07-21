# Fichier : ql_web_app/swap/forms.py
from django import forms

class VanillaSwapForm(forms.Form):
    notional = forms.FloatField(
        label="Notionnel", 
        initial=1000000,
        help_text="Montant nominal du swap."
    )
    maturity_years = forms.IntegerField(
        label="Maturité (années)", 
        initial=10,
        min_value=1
    )
    fixed_rate_pct = forms.FloatField(
        label="Taux Fixe (%)", 
        initial=2.5,
        help_text="Taux de la jambe fixe. Ex: 2.5 pour 2.5%."
    )
    float_spread_pct = forms.FloatField(
        label="Spread sur Taux Flottant (%)", 
        initial=0.4,
        help_text="Marge au-dessus du Libor. Ex: 0.4 pour 0.4% (40 bps)."
    )
    discount_curve_rate_pct = forms.FloatField(
        label="Taux Courbe d'Actualisation (%)", 
        initial=1.0,
        help_text="Taux (flat) pour actualiser les flux. Ex: 1.0 pour 1.0%."
    )
    libor_curve_rate_pct = forms.FloatField(
        label="Taux Courbe de Projection (%)", 
        initial=2.0,
        help_text="Taux (flat) pour projeter les flux flottants. Ex: 2.0 pour 2.0%."
    )