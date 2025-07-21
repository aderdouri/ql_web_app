# Fichier : ql_web_app/chapter5_curves/forms.py
from django import forms
from datetime import date

class CurveBuilderForm(forms.Form):
    evaluation_dt = forms.DateField(
        label='Evaluation Date', 
        initial=date(2014, 10, 3),
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Change this date to see how a relative curve moves."
    )