# day_count_glitch/forms.py (VERSION FINALE ET COMPLÈTE)

from django import forms
import datetime

class DayCountForm(forms.Form):
    # ==============================================================================
    # CORRECTION : On ajoute tous les champs nécessaires pour correspondre au livre
    # ==============================================================================

    # --- Option Parameters ---
    evaluation_date = forms.DateField(
        label="Evaluation Date",
        initial=datetime.date(2018, 7, 27),
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    exercise_date = forms.DateField(
        label="Exercise Date",
        initial=datetime.date(2018, 10, 27),  # 3 months after evaluation date
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    strike_price = forms.FloatField(
        label="Strike Price",
        initial=100.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'value': '100.0'})
    )
    spot_price = forms.FloatField(
        label="Spot Price",
        initial=100.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'value': '100.0'})
    )

    # --- Market Parameters ---
    volatility = forms.FloatField(
        label="Volatility",
        initial=0.20,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0.20'})
    )
    risk_free_rate = forms.FloatField(
        label="Risk-Free Rate",
        initial=0.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001', 'value': '0.0'})
    )

    # --- Day-Count Conventions ---
    r_day_count = forms.ChoiceField(
        label="Risk-Free Rate Day Count",
        choices=[
            ('Actual365Fixed', 'Actual/365 (Fixed)'),
            ('Business252', 'Business/252')
        ],
        initial='Actual365Fixed',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    sigma_day_count = forms.ChoiceField(
        label="Volatility Day Count",
        choices=[
            ('Actual365Fixed', 'Actual/365 (Fixed)'),
            ('Business252', 'Business/252')
        ],
        initial='Actual365Fixed',
        widget=forms.Select(attrs={'class': 'form-control'})
    )