from django import forms

class HestonCalibrationForm(forms.Form):
    # Paramètres initiaux pour la calibration
    v0 = forms.FloatField(label="Initial v0 (variance)", initial=0.01)
    kappa = forms.FloatField(label="Initial kappa (reversion speed)", initial=0.2)
    theta = forms.FloatField(label="Initial theta (long-term variance)", initial=0.02)
    sigma = forms.FloatField(label="Initial sigma (vol of vol)", initial=0.5)
    rho = forms.FloatField(label="Initial rho (correlation)", initial=-0.75, min_value=-1, max_value=1)
    
    # Paramètres de l'algorithme
    max_iterations = forms.IntegerField(label="Max Iterations", initial=500)