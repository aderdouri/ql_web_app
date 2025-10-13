from django import forms
import datetime

class HestonCalibrationForm(forms.Form):
    # Champs obligatoires pour le chapitre 23
    solver_method = forms.ChoiceField(
        label="Solver Method",
        choices=[
            ('ql_lm', 'QuantLib Levenberg-Marquardt'),
            ('scipy_lm', 'SciPy Levenberg-Marquardt'),
            ('scipy_ls', 'SciPy Least Squares'),
            ('scipy_de', 'SciPy Differential Evolution'),
            ('scipy_bh', 'SciPy Basin Hopping'),
        ],
        # Pas de valeur par défaut - laisser l'utilisateur choisir
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # Paramètres de base (obligatoires)
    evaluation_date = forms.DateField(
        label="Evaluation Date", 
        initial=datetime.date(2015, 11, 6),
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    spot_price = forms.FloatField(
        label="Spot Price", 
        initial=659.37,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    risk_free_rate = forms.FloatField(
        label="Risk-Free Rate (%)", 
        initial=1.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
    )
    dividend_rate = forms.FloatField(
        label="Dividend Rate (%)", 
        initial=0.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
    )

    # Paramètres initiaux Heston (obligatoires)
    theta = forms.FloatField(
        label="θ (Theta)", 
        initial=0.02,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    kappa = forms.FloatField(
        label="κ (Kappa)", 
        initial=0.2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
    )
    sigma = forms.FloatField(
        label="σ (Sigma)", 
        initial=0.5,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    rho = forms.FloatField(
        label="ρ (Rho)", 
        initial=0.1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
    )
    v0 = forms.FloatField(
        label="v₀ (V0)", 
        initial=0.01,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )