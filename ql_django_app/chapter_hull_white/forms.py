# Fichier : ql_web_app/chapter_hull_white/forms.py
from django import forms

# Formulaire pour le labo de calibration
class CalibrationForm(forms.Form):
    MODEL_CHOICES = [
        ('HullWhite', 'Hull-White 1-Factor'),
        ('BlackKarasinski', 'Black-Karasinski'),
        ('G2', 'G2++ 2-Factor'),
    ]
    model_name = forms.ChoiceField(label="Short-Rate Model", choices=MODEL_CHOICES)

# Formulaire pour le labo de simulation
class HullWhiteSimulationForm(forms.Form):
    alpha = forms.FloatField(label="Alpha (Mean Reversion)", initial=0.1)
    sigma = forms.FloatField(label="Sigma (Volatility)", initial=0.01)
    num_paths = forms.IntegerField(label="Number of Paths", initial=5)
    num_years = forms.IntegerField(label="Simulation Length (Years)", initial=10)
    seed = forms.IntegerField(label="Random Seed", initial=42)