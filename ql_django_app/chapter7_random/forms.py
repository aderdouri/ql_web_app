# Fichier : ql_web_app/chapter7_random/forms.py
from django import forms

class RandomGeneratorForm(forms.Form):
    GENERATOR_CHOICES = [
        ('pseudorandom', 'Pseudo-Random (Mersenne Twister)'),
        ('quasirandom', 'Quasi-Random / Low-Discrepancy (Sobol)'),
    ]
    
    generator_type = forms.ChoiceField(
        label='Generator Type', 
        choices=GENERATOR_CHOICES
    )
    num_points = forms.IntegerField(
        label='Number of Points', 
        initial=500, 
        min_value=10, 
        max_value=5000
    )
    seed = forms.IntegerField(label='Seed', initial=42)