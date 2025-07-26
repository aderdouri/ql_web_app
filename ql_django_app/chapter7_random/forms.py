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
        label='Number of Points to Generate', 
        initial=256, 
        min_value=16, 
        max_value=2048,
        help_text="Try powers of 2 for Sobol (e.g., 64, 128, 256, 512...)."
    )
    dimensionality = forms.IntegerField(
        label="Dimensionality",
        initial=2,
        min_value=1,
        max_value=10,
        help_text="The number of dimensions for the random sequence (e.g., 2 for a 2D plot)."
    )
    seed = forms.IntegerField(label='Seed', initial=42)