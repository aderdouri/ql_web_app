# Fichier : ql_web_app/chapter_calibration/forms.py
from django import forms

class ModelChoiceForm(forms.Form):
    MODEL_CHOICES = [
        ('HullWhite', 'Hull-White 1-Factor'),
        ('BlackKarasinski', 'Black-Karasinski'),
        ('G2', 'G2++ 2-Factor'),
    ]
    model_name = forms.ChoiceField(
        label="Short-Rate Model to Calibrate", 
        choices=MODEL_CHOICES,
        help_text="Select a model to fit to the market data."
    )