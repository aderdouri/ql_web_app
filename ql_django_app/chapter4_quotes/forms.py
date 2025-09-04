# chapter4_quotes/forms.py (VERSION FINALE DÉFINITIVE)

from django import forms

class MarketUpdateForm(forms.Form):
    # Le formulaire n'a besoin QUE du nouveau prix. La date est gérée par la vue.
    new_price = forms.FloatField(
        label="Nouveau Prix pour toutes les obligations",
        initial=101.0
    )