# File: ql_web_app/chapter_2_lab/forms.py
from django import forms
from datetime import date

class EngineComparisonForm(forms.Form):
    # --- 1. Instrument Parameters ---
    spot_price = forms.FloatField(label='Spot Price', initial=100.0)
    strike_price = forms.FloatField(label='Strike Price', initial=100.0)
    maturity_date = forms.DateField(label='Maturity Date', initial=date(2026, 1, 15), widget=forms.DateInput(attrs={'type': 'date'}))
    volatility = forms.FloatField(label='Volatility (%)', initial=20.0)
    risk_free_rate = forms.FloatField(label='Risk-Free Rate (%)', initial=1.0)
    
    # --- 2. Engine Selection ---
    ENGINE_CHOICES = [
        ('AnalyticEuropeanEngine', 'Black-Scholes (Analytic Formula)'),
        ('BinomialCRR', 'Binomial Tree (CRR - 200 steps)'),
        ('BinomialJR', 'Binomial Tree (Jarrow-Rudd - 200 steps)'),
    ]
    
    engines_to_compare = forms.MultipleChoiceField(
        label='Select Engines to Compare',
        choices=ENGINE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        initial=['AnalyticEuropeanEngine', 'BinomialCRR'] # Pré-cocher des choix par défaut
    )