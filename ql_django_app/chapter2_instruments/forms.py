# Fichier : ql_web_app/chapter2_instruments/forms.py (VERSION AVEC PARAMÈTRES RÉALISTES)
from django import forms
from datetime import date

class PricingEngineForm(forms.Form):
    ENGINE_CHOICES = [
        ('analytic', 'Analytic Black-Scholes Formula'),
        ('binomial_crr', 'Binomial Tree (Cox-Ross-Rubinstein)'),
        ('monte_carlo', 'Monte Carlo Simulation'),
    ]
    
    engine_choice = forms.ChoiceField(
        label='Pricing Engine', 
        choices=ENGINE_CHOICES
    )
    
    # ==============================================================================
    # ON UTILISE DES PARAMÈTRES "AT-THE-MONEY" PLUS COHÉRENTS
    # ==============================================================================
    maturity_dt = forms.DateField(label='Maturity Date', initial=date(2016, 5, 15), widget=forms.DateInput(attrs={'type':'date'}))
    spot_price = forms.FloatField(label='Spot Price', initial=100.0)
    strike_price = forms.FloatField(label='Strike Price', initial=100.0)
    volatility_pct = forms.FloatField(label='Volatility (%)', initial=20.0)
    dividend_rate_pct = forms.FloatField(label='Dividend Rate (%)', initial=1.5)
    risk_free_rate_pct = forms.FloatField(label='Risk-Free Rate (%)', initial=1.0)