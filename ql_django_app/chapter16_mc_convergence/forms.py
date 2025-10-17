# forms.py (VERSION FINALE ET COMPLÈTE)

from django import forms
import datetime

class ConvergenceForm(forms.Form):
    experiment_type = forms.ChoiceField(
        label="Experiment Type",
        choices=[
            ('vary_sigma', 'Impact of Sigma (Volatility) - Vary σ with fixed a'),
            ('vary_a', 'Impact of Mean Reversion - Vary a with fixed σ'),
            ('std_dev', 'Discount Factor Standard Deviation'), # <-- NOUVELLE OPTION
        ],
        initial='std_dev'  # Par défaut, commencer avec std_dev
    )
    
    a = forms.FloatField(label="a (Mean Reversion)", initial=0.1)
    sigma = forms.FloatField(label="σ (Volatility)", initial=0.02)
    num_paths = forms.IntegerField(label="Number of Monte Carlo Paths", initial=100)
    time_steps = forms.IntegerField(label="Time Steps", initial=180)
    simulation_length = forms.IntegerField(label="Simulation Length (Years)", initial=15)
    forward_rate = forms.FloatField(label="Forward Rate", initial=0.05)
    random_seed = forms.IntegerField(label="Random Seed", initial=42)
    evaluation_date = forms.DateField(initial=datetime.date(2015, 1, 15), widget=forms.HiddenInput())