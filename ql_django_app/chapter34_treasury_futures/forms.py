# forms.py

from django import forms
import datetime

class TreasuryFuturesForm(forms.Form):
    evaluation_date = forms.DateField(
        label="Evaluation Date",
        initial='2015-11-30',
        help_text="Date on which the futures contract is calculated",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    futures_price = forms.FloatField(
        label="Market Futures Price",
        initial=127.0625,
        min_value=0.0,
        max_value=1000.0,
        help_text="Market price of the futures contract",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.0001'
        })
    )