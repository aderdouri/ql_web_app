from django import forms

class ConvergenceForm(forms.Form):
    EXPERIMENT_CHOICES = [
        ('vary_sigma', 'Impact of Sigma (Volatility)'),
        ('vol_dist', 'Discount Factor Distribution'),
    ]
    
    experiment_type = forms.ChoiceField(label="Experiment to run", choices=EXPERIMENT_CHOICES)
    a = forms.FloatField(label="Alpha (Mean Reversion)", initial=0.1)
    sigma = forms.FloatField(label="Sigma (Volatility)", initial=0.02)
    num_paths = forms.IntegerField(label="Number of Monte Carlo Paths", initial=500, min_value=100, max_value=5000)
    seed = forms.IntegerField(label="Random Seed", initial=42)