from django import forms

class OptimizerChoiceForm(forms.Form):
    OPTIMIZER_CHOICES = [
        ('QL Levenberg-Marquardt', 'QuantLib Levenberg-Marquardt'),
        ('SciPy Levenberg-Marquardt', 'SciPy Levenberg-Marquardt'),
        ('SciPy Least Squares', 'SciPy Least Squares'),
    ]
    optimizer_name = forms.ChoiceField(
        label="Optimization Method", 
        choices=OPTIMIZER_CHOICES,
        help_text="The calibration process can be slow. Please be patient."
    )