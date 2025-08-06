from django import forms

class ForwardRateNodeForm(forms.Form):
    # Un champ pour la durée (ex: 1 pour 1 an, 2 pour 2 ans...)
    tenor_years = forms.IntegerField(label="Tenor (Years)", min_value=1)
    # Un champ pour le taux forward
    forward_rate_pct = forms.FloatField(label="Forward Rate (%)")