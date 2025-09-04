# chapter3_greeks/forms.py (VERSION FINALE AVEC AIDE)

from django import forms

class NumericalGreeksForm(forms.Form):
    # Paramètres de l'option à barrière
    barrier_type = forms.ChoiceField(
        choices=[('UpIn', 'Up-and-In'), ('UpOut', 'Up-and-Out'), ('DownIn', 'Down-and-In'), ('DownOut', 'Down-and-Out')],
        initial='UpIn', label="Type de Barrière"
    )
    barrier_level = forms.FloatField(
        initial=120.0, label="Niveau de la Barrière",
        help_text="Pour une barrière 'Up', doit être > au prix du sous-jacent. Pour 'Down', doit être <."
    )
    rebate = forms.FloatField(initial=0.0, label="Rebate")
    
    # Paramètres de l'option sous-jacente
    option_type = forms.ChoiceField(choices=[('Call', 'Call'), ('Put', 'Put')], initial='Call', label="Type d'Option")
    strike_price = forms.FloatField(initial=100.0, label="Prix d'Exercice (Strike)")
    
    # Dates
    evaluation_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        label="Date d'Évaluation"
    )
    expiry_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        label="Date d'Échéance", help_text="Doit être après la date d'évaluation."
    )
    
    # Données de marché
    underlying_price = forms.FloatField(initial=100.0, label="Prix du Sous-jacent")
    risk_free_rate = forms.FloatField(initial=0.01, label="Taux Sans Risque")
    volatility = forms.FloatField(initial=0.20, label="Volatilité")

    # Paramètres pour le calcul numérique
    h_underlying = forms.FloatField(initial=0.01, label="Perturbation (h) du Sous-jacent")
    h_rate = forms.FloatField(initial=0.0001, label="Perturbation (h) du Taux")
    h_vol = forms.FloatField(initial=0.0001, label="Perturbation (h) de la Volatilité")