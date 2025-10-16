from django import forms
import datetime

class CreditSpreadForm(forms.Form):
    # Paramètres de base de la simulation
    evaluation_date = forms.DateField(
        label="Evaluation Date", 
        initial=datetime.date(2016, 7, 26),
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    base_rate = forms.FloatField(
        label="Base Rate (%)", 
        initial=0.15,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    
    # Paramètres de l'obligation
    issue_date = forms.DateField(
        label="Issue Date", 
        initial=datetime.date(2016, 7, 15),
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    maturity_date = forms.DateField(
        label="Maturity Date", 
        initial=datetime.date(2021, 7, 15),
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    coupon_rate = forms.FloatField(
        label="Coupon Rate (%)", 
        initial=3.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
    )

    # Paramètres interactifs principaux
    spread_method = forms.ChoiceField(
        label="Spread Application Method",
        choices=[
            ('direct_shock', 'Direct Shock (on flat curve only)'),
            ('parallel_shift', 'Parallel Shift'),
            ('non_parallel_shift', 'Non-Parallel Shift'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    spread1 = forms.FloatField(
        label="Spread (bps) or Start Spread (bps)", 
        initial=50.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '1'})
    )
    spread2 = forms.FloatField(
        label="End Spread (bps) (for non-parallel)", 
        initial=100.0, 
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '1'})
    )
